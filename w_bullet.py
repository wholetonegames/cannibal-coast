from i_moving_char import GameCharacter
import z_m


class Bullet(GameCharacter):
    def __init__(self, stage, indexNumber, name,  INIT_POS, modelName, map_boundaries):
        GameCharacter.__init__(self, map_boundaries)
        self.name = name
        self.modelName = modelName
        self.indexNumber = indexNumber
        self.INIT_POS = INIT_POS
        self.stage = stage
        self.speed = 10
        self.timer = 0
        self.max_duration = 1  # when the bullet should stop flying
        self.collision_size = (0, 0, 0, 0.6)
        self.initActor()

    def initActor(self):
        self.loadActor(self.INIT_POS)
        self.initCollision()

    def fire(self, pos, heading, speed, max_duration):
        self.max_duration = max_duration
        if heading == 90:
            self.direction = self.EAST
        elif heading == -90:
            self.direction = self.WEST
        elif heading == 180:
            self.direction = self.NORTH
        elif heading == 0:
            self.direction = self.SOUTH
        self.speed += speed
        self.actor.setPos(pos)

    def reset(self):
        self.timer = 0
        self.direction = None
        self.speed = 10
        self.actor.setPos(self.INIT_POS)

    def updatePos(self, dt):
        self.timer += dt
        if self.timer >= self.max_duration:
            self.reset()
            return
        self.updatePosModel(dt)


class BulletHero(Bullet):
    def __init__(self, stage, indexNumber, modelName, map_boundaries):
        INIT_POS = (indexNumber * 5, 0, 100)
        Bullet.__init__(self, stage, indexNumber,
                        'bullet_h', INIT_POS, modelName, map_boundaries)


class BulletEnemy(Bullet):
    def __init__(self, stage, indexNumber, modelName, map_boundaries):
        INIT_POS = (indexNumber * 5, -2, 100)
        Bullet.__init__(self, stage, indexNumber,
                        'bullet_e', INIT_POS, modelName, map_boundaries)


class Smoke:
    def __init__(self, stage, indexNumber):
        self.isMessageSent = False
        self.indexNumber = indexNumber
        self.actor = loader.loadModel("z_smoke")
        self.actor.setPos(self.indexNumber * 5, -2, 300)
        self.actor.reparentTo(stage)
        self.itemPos = None

    def set_pos(self, pos):
        self.itemPos = pos
        self.actor.setPos(pos)
        self.actor.setAlphaScale(0.5)
        self.actor.setScale(0.1)
        taskMgr.add(self.blow_up, 'blow_up_{}'.format(self.indexNumber))

    def blow_up(self, task):
        if task.time < 0.5:
            self.actor.setScale(task.time + 1.5)
            return task.cont
        if not self.isMessageSent:
            base.messenger.send(z_m.GRUNT_KILLED, [
                                self.itemPos, self.indexNumber])
            self.isMessageSent = True
        self.set_pos((self.indexNumber * 5, -2, 300))
        return task.done
