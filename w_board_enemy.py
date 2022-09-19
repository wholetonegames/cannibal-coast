from i_stage import IStage
import z_m
from w_moving_enemy import EnemyCharacter
from w_bullet import BulletEnemy, BulletHero, Smoke
from w_npc import ItemEnemy


class AnonymousDamage:
    def __init__(self):
        self.data = {'attack': 20}


class BoardEnemy(IStage):
    DAMAGE_OBJ = AnonymousDamage()

    def __init__(self):
        IStage.__init__(self, "enemy")
        self.isEnemiesInitialized = False
        self.setup()
        self.setCollision()
        self.stop()

    def init_charas_items(self):
        self.initEnemy()

    def initEnemy(self):
        enemyNumber = self.this_map["enemyNumber"]
        enemyActors = self.this_map["enemyModels"]
        self.enemyActors = []
        self.itemActors = []
        for enemyIndex in list(range(0, enemyNumber)):
            enemy_struct = enemyActors[enemyIndex]
            e = EnemyCharacter(self.stage,
                               enemyIndex,
                               base.gameData.enemy_level,
                               enemy_struct,
                               self.stage_grid.map_boundaries)
            self.enemyActors.append(e)
            i = ItemEnemy(
                self.stage,
                enemyIndex,
                self.stage_grid.map_boundaries,
                e.actorName
            )
            self.itemActors.append(i)
        # only have bullets if there are enemies present
        self.initBulletSmoke()

    def initBulletSmoke(self):
        # create an object pool here
        for i in list(range(0, self.MAX_BULLET)):
            b = BulletHero(
                self.stage, i, self.this_map["BulletHero"], self.stage_grid.map_boundaries)
            self.hero_bullets.append(b)
            b = BulletEnemy(
                self.stage, i, self.this_map["BulletEnemy"], self.stage_grid.map_boundaries)
            self.enemy_bullets.append(b)
        arr_len = len(self.enemyActors)
        for i in list(range(0, arr_len)):
            s = Smoke(self.stage, i)
            self.smokes.append(s)

    def add_enemy_item(self, pos, index):
        i = self.itemActors[index]
        i.setPos(pos)

    def moveEnemies(self, dt):
        for e in self.enemyActors:
            if e.is_ko:
                continue
            if e.enemy_type == e.TYPE_PREDATOR:
                e.chase_player(self.player.getPos())
            e.updatePos(dt)
            if e.can_fire:
                self.enemy_fire(e)

    def enemy_fire(self, e):
        g = e.gunPos()
        e.fire()
        if self.enemy_bullet_index >= self.MAX_BULLET:
            self.enemy_bullet_index = 0
        self.enemy_bullets[self.enemy_bullet_index].fire(
            g, e.getHeading(), e.speed, 5)
        self.enemy_bullet_index += 1

    def aiUpdate(self, task):
        dt = globalClock.getDt()
        self.update_hero(dt)
        if self.canEnemiesMove and not self.isEnemiesInitialized:
            self.initEnemyMovement()
        if not self.canEnemiesMove:
            return task.cont
        self.moveEnemies(dt)
        for b in (self.hero_bullets + self.enemy_bullets):
            if not b.direction:
                continue
            b.updatePos(dt)
        for i in self.itemActors:
            i.clamp_to_ground()
        return task.cont

    def intoEvent(self, entry):
        if not entry.hasInto():
            return

        intoName, fromName = self.getIntoFromNames(entry)

        if self.NAME_EXIT in intoName and self.NAME_HERO in fromName:
            self.requestBoardChange()
            return

        if self.NAME_ENEMY in fromName:
            if self.NAME_HERO in intoName or self.NAME_WALL in intoName or \
                    self.NAME_ENEMY in intoName:
                index = self.getIndexFromEvent(fromName)
                e = self.enemyActors[index]
                normal = entry.getSurfaceNormal(entry.getIntoNodePath())
                e.moveAwayFrom(normal)
            if self.NAME_HERO in intoName:
                index = self.getIndexFromEvent(fromName)
                e = self.enemyActors[index]
                self.harmPlayer(e)
            if self.NAME_ENEMY in intoName:
                self.solve_prey_and_predator(intoName, fromName)
            return

        if self.NAME_HERO_BULLET in fromName:
            if self.NAME_HERO in intoName:
                return
            self.kill_bullet(fromName, False)
            if self.NAME_ITEM in intoName:
                itemIndex = self.getIndexFromEvent(intoName)
                item = self.itemActors[itemIndex]
                item.kill(False)
            if self.NAME_ENEMY in intoName:
                index = self.getIndexFromEvent(intoName)
                e = self.enemyActors[index]
                if e.direction:
                    self.setSmoke(e.getPos(), e.indexNumber)
                    e.decrement_hp(self.DAMAGE_OBJ)
                    base.messenger.send("sfxEnemyHurt")
            return

        if self.NAME_ENEMY_BULLET in fromName:
            self.kill_bullet(fromName)
            if self.NAME_HERO in intoName:
                self.harmPlayer(self.DAMAGE_OBJ)
            if self.NAME_ENEMY in intoName:
                into_index = self.getIndexFromEvent(intoName)
                into_e = self.enemyActors[into_index]
                # only prey should be killed by enemy bullets because it's bad for the player
                if into_e.enemy_type != into_e.TYPE_PREY:
                    return
                into_e.decrement_hp(self.DAMAGE_OBJ)
            return

        if self.NAME_ITEM in intoName and self.NAME_HERO in fromName:
            itemIndex = self.getIndexFromEvent(intoName)
            item = self.itemActors[itemIndex]
            item.kill(True)
            return

        

    def kill_bullet(self, fromName, is_enemy=True):
        index = self.getIndexFromEvent(fromName)
        if is_enemy:
            b = self.enemy_bullets[index]
            b.reset()
        else:
            b = self.hero_bullets[index]
            b.reset()

    def harmPlayer(self, enemy):
        self.player.decrement_hp(enemy)
        base.messenger.send("sfxHeroHurt")
        if self.player.is_ko:
            self.requestBoardChange()

    def againEvent(self, entry):
        if not entry.hasInto():
            return

        intoName, fromName = self.getIntoFromNames(entry)

        if not self.NAME_ENEMY in fromName:
            return
        if not self.NAME_HERO in intoName and not self.NAME_WALL in intoName and not self.NAME_ENEMY in intoName:
            return

        index = self.getIndexFromEvent(fromName)
        if index < 0 or index >= len(self.enemyActors):
            return
        e = self.enemyActors[index]
        e.randomDirection()

    def cancelCommand(self):
        base.messenger.send(z_m.MENU_PAUSE)

    def readCommand(self, p):
        if base.commandMap[base.BUTTON_CONFIRM] and p.can_fire:
            self.heroFire(p)
            return

        if not base.commandMap[base.BUTTON_CONFIRM]:
            p.reset_fire()

        if base.commandMap[base.BUTTON_CANCEL]:
            self.cancelCommand()

    def heroFire(self, p):
        if base.gameData.ammo <= 0:
            return
        base.gameData.add_bullets(-1)
        g = p.gunPos()
        p.fire()
        if self.hero_bullet_index >= self.MAX_BULLET:
            self.hero_bullet_index = 0
        self.hero_bullets[self.hero_bullet_index].fire(
            g, p.getHeading(), p.speed, base.gameData.bullet_timer)
        self.hero_bullet_index += 1
        base.messenger.send("sfxHeroShoot")

    def requestBoardChange(self):
        base.messenger.send(z_m.MENU_GAMEOVER)

    def initEnemyMovement(self):
        for e in self.enemyActors:
            e.initState()
        self.isEnemiesInitialized = True
        self.canEnemiesMove = True

    def setSmoke(self, pos, e_index):
        self.smokes[e_index].set_pos(pos)

    def solve_prey_and_predator(self, intoName, fromName):
        from_index = self.getIndexFromEvent(fromName)
        from_e = self.enemyActors[from_index]
        into_index = self.getIndexFromEvent(intoName)
        into_e = self.enemyActors[into_index]

        if from_e.enemy_type != from_e.TYPE_PREY and \
                into_e.enemy_type == into_e.TYPE_PREY:
            into_e.decrement_hp(self.DAMAGE_OBJ)
