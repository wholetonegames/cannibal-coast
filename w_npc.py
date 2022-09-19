from i_moving_char import GameCharacter
import random
import z_m

class ItemNPC(GameCharacter):
    def __init__(self, this_type, npcIndex, stage, map_boundaries):
        GameCharacter.__init__(self, map_boundaries)
        self.collision_size = (0, 0, 0.2, 1.0)
        self.stage = stage
        self.type = this_type
        self.indexNumber = npcIndex
        self.name = 'item'
        self.modelName = "{}_{}".format(self.name, self.type)
        self.is_touched = False
        self.initActor()

    def initActor(self):
        self.is_in_game = True
        faEmpty = self.stage.find(
            "**/{}_{}_{}".format(self.name, self.type, self.indexNumber))
        self.startPos = faEmpty.getPos()
        self.loadActor(self.startPos)
        self.initCollision()

    def kill(self):
        if self.is_touched:
            return
        self.actor.setPos(self.indexNumber-20, self.indexNumber-20, -200)
        self.actor.hide()
        self.is_touched = True
        self.is_in_game = False
        base.messenger.send(z_m.GOT_ITEM, [self.type])
        base.messenger.send("sfxBullet")

    def updatePos(self, dt):
        pass


class ItemEnemy(GameCharacter):
    def __init__(self, stage, index, map_boundaries, enemy_name):
        GameCharacter.__init__(self, map_boundaries)
        self.collision_size = (0, 0, 0.2, 1.0)
        self.stage = stage
        self.type = enemy_name
        self.name = 'item'
        self.modelName = "{}_{}".format(self.name, self.type)
        self.indexNumber = index
        self.startPos = (self.indexNumber-30, self.indexNumber-30, 200)
        self.is_touched = False
        self.initActor()

    def initActor(self):
        self.loadActor(self.startPos)
        self.initCollision()

    def setPos(self, pos):
        self.is_in_game = True
        self.actor.setPos(pos)

    def kill(self, is_hero_kill):
        if self.is_touched:
            return
        self.actor.setPos(self.indexNumber-30, self.indexNumber-30, 200)
        self.actor.hide()
        self.is_touched = True
        self.is_in_game = False
        if is_hero_kill:
            base.messenger.send(z_m.GOT_ITEM, [self.type])
            base.messenger.send("sfxItem")

    def updatePos(self, dt):
        pass
