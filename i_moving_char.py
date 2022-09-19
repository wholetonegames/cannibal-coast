import abc
from panda3d.core import (
    CollisionNode,
    CollisionSphere)
from direct.actor.Actor import Actor


class GameCharacter(metaclass=abc.ABCMeta):
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    DIRECTIONS = (NORTH, EAST, SOUTH, WEST)

    def __init__(self, map_boundaries):
        self.map_boundaries = map_boundaries
        self.direction = None
        self.previous_direction = True  # hacky way to start with idle position
        self.actor = None
        self.indexNumber = None
        self.modelName = None
        self.actorName = None
        self.name = None
        self.stage = None
        self.speed = None
        self.is_in_game = False
        self.collision_size = [0, 0, 0, 0]

    def change_animation(self):
        if not self.direction:
            self.actor.loop('idle')
        else:
            self.actor.loop('walk')

    def updatePosActor(self, dt):
        x, y, z = self.actor.getPos(render)

        if self.previous_direction != self.direction:
            self.change_animation()
        self.previous_direction = self.direction

        if not self.speed:
            return
        x, y = self.set_speed_hpr(x, y, dt)
        self.clamp_to_map(x, y)
        self.actor.setZ(0)

    def updatePosModel(self, dt):
        if not self.speed:
            return
        x, y, z = self.actor.getPos(render)
        x, y = self.set_speed_hpr(x, y, dt)
        self.actor.setPos(x, y, 1) # bullets need to be off the ground

    def set_speed_hpr(self, x, y, dt):
        speed = self.speed * dt
        if self.direction == self.NORTH:
            y += speed
            self.actor.setHpr(180, 0, 0)
        elif self.direction == self.SOUTH:
            y -= speed
            self.actor.setHpr(0, 0, 0)
        elif self.direction == self.EAST:
            x += speed
            self.actor.setHpr(90, 0, 0)
        elif self.direction == self.WEST:
            x -= speed
            self.actor.setHpr(-90, 0, 0)
        return x, y

    @abc.abstractmethod
    def updatePos(self, dt):
        raise NotImplementedError('subclass must define this method')

    def clamp_to_map(self, x, y):
        x = min(x, self.map_boundaries["xMax"])
        x = max(x, self.map_boundaries["xMin"])
        self.actor.setX(x)
        y = min(y, self.map_boundaries["yMax"])
        y = max(y, self.map_boundaries["yMin"])
        self.actor.setY(y)

    def clamp_to_ground(self):
        if self.is_in_game:
            self.actor.setZ(0)

    def getPos(self):
        return self.actor.getPos(render)

    def getHeading(self):
        h, p, r = self.actor.getHpr()
        return h

    def loadActor(self, pos):
        if self.modelName:
            self.actor = loader.loadModel(self.modelName)
        elif self.actorName:
            self.actor = Actor("{}".format(self.actorName), {
                "idle": "{}-idle".format(self.actorName),
                "walk": "{}-walk".format(self.actorName)
            })
            self.actor.loop('idle')
        else:
            self.actor = loader.loadModel(self.name)
        self.actor.reparentTo(self.stage)
        self.actor.setPos(pos)

    def initCollision(self):
        cNode = CollisionNode("{}_{}".format(self.name, self.indexNumber))
        (x, y, z, s) = self.collision_size
        cNode.addSolid(CollisionSphere(x, y, z, s))
        faCollision = self.actor.attachNewNode(cNode)
        #####################################################
        # faCollision.show()
        #####################################################
        base.pusher.addCollider(
            faCollision, self.actor, base.drive.node())
        base.cTrav.addCollider(faCollision, base.pusher)


class HealthCharacter(GameCharacter):
    def __init__(self, map_boundaries):
        GameCharacter.__init__(self, map_boundaries)
        self.hp = 1
        self.can_hurt = True

    def decrement_hp(self, enemy):
        if not self.can_hurt:
            return
        self.hp -= enemy.data['attack']
        if self.is_ko:
            self.kill()
        else:
            self.flash()

    @property
    def is_ko(self):
        return self.hp <= 0

    def kill(self):
        pass

    def flash(self):
        pass


class FiringCharacter(HealthCharacter, metaclass=abc.ABCMeta):
    def __init__(self, fire_later_time, map_boundaries):
        HealthCharacter.__init__(self, map_boundaries)
        self.can_fire = True
        self.fire_later_time = fire_later_time

    def gunPos(self):
        # to get global position, call render
        x, y, z = self.actor.getPos(render)
        h = self.getHeading()
        if h == 90:  # EAST
            x += 1
        elif h == -90:  # WEST
            x -= 1
        elif h == 180:  # NORTH
            y += 1
        elif h == 0:  # SOUTH
            y -= 1
        return (x, y, z)

    @abc.abstractmethod
    def fire(self):
        raise NotImplementedError('subclass must define this method')
