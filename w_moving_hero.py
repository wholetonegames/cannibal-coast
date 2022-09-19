from i_moving_char import FiringCharacter
from panda3d.core import TransparencyAttrib
import random
import z_m
import math


class PlayerCharacter(FiringCharacter):
    def __init__(self, startPos, stage, heroHP, actorName, map_boundaries):
        FiringCharacter.__init__(
            self, 0, map_boundaries)
        self.actorName = actorName
        self.hp = heroHP
        self.indexNumber = 0  # if multiplayer, this will need to be passed on creation
        self.stage = stage
        self.startPos = startPos
        self.name = 'hero'
        self.speed= 9
        self.collision_size = (0, 0, 0.2, 1.0)
        self.initActor()

    def initActor(self):
        self.loadActor(self.startPos)
        self.actor.setTransparency(TransparencyAttrib.MAlpha)
        self.actor.setAlphaScale(1.0)
        self.initCollision()
        self.direction = None

    def flash(self):
        base.messenger.send(z_m.PLAYER_HURT)
        self.can_hurt = False
        taskMgr.add(self.flashing_colour, 'hero_flash')

    def flashing_colour(self, task):
        if task.time < 1.0:
            self.actor.setAlphaScale(task.time % 1.0)
            return task.cont
        self.actor.setAlphaScale(1.0)
        self.can_hurt = True
        return task.done

    def kill(self):
        self.direction = None
        self.can_fire = False
        self.actor.setPos(self.indexNumber-15, self.indexNumber-15, 100)
        base.messenger.send(z_m.PLAYER_HURT)

    def updatePos(self, dt):
        self.updatePosActor(dt)

    def fire(self):
        self.can_fire = False

    def reset_fire(self):
        self.can_fire = True
