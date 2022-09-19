from i_moving_char import FiringCharacter
from panda3d.core import TransparencyAttrib
import random
import z_m
import z_enemy


class EnemyCharacter(FiringCharacter):
    TASK_CHANGE_TIME = 8.5
    TASK_CAN_CHANGE_TIME = 0.2
    TASK_CHANGE_NAME = 'randomStateChange'
    TYPE_SHOOTER = z_enemy.TYPE_SHOOTER
    TYPE_PREDATOR = z_enemy.TYPE_PREDATOR
    TYPE_PREY = z_enemy.TYPE_PREY

    def __init__(self, stage, indexNumber, enemy_level, enemyData, map_boundaries):
        fire_cool_off = 2 / enemy_level
        FiringCharacter.__init__(self, fire_cool_off, map_boundaries)
        self.data = enemyData
        self.is_boss = "isBoss" in self.data
        self.actorName = self.data["model"]
        self.hp = self.data["hp"]
        self.can_fire = False
        self.can_change_direction = True
        self.indexNumber = indexNumber
        self.stage = stage
        self.name = 'enemy'
        self.enemy_type = self.data["type"]
        self.speed = 5 + enemy_level
        self.is_turning_horizontal = False
        self.collision_size = (0, 0, 0.2, 1.0)
        self.taskName = '{}_{}_{}'.format(
            self.TASK_CHANGE_NAME, self.name, self.indexNumber)
        self.initActor()

    def initActor(self):
        self.is_in_game = True
        faEmpty = self.stage.find(
            "**/{}_{}".format(self.name, self.indexNumber))
        faPos = faEmpty.getPos()
        self.loadActor(faPos)
        self.initCollision()

    def initState(self):
        # this prevents enemies from moving before stage is set
        self.can_fire = self.enemy_type == self.TYPE_SHOOTER
        self.randomDirection()
        taskMgr.doMethodLater(self.TASK_CHANGE_TIME,
                              self.taskStateChange, self.taskName)

    def taskStateChange(self, task):
        self.randomDirection()
        return task.again

    def randomDirection(self):
        if not self.can_change_direction:
            return
        previous_direction = self.direction
        while previous_direction == self.direction:
            self.direction = random.choice(self.DIRECTIONS)
        self.can_change_direction = False
        taskMgr.doMethodLater(self.TASK_CAN_CHANGE_TIME,
                              self.canChangeAgain, 'cool-off' + self.taskName)

    def moveAwayFrom(self, normal):
        if not self.can_change_direction:
            return
        x, y, z = normal
        self.is_turning_horizontal = not self.is_turning_horizontal
        if self.is_turning_horizontal:
            self.direction = self.WEST if x > 0 else self.EAST
        else:
            self.direction = self.SOUTH if y > 0 else self.NORTH
        self.can_change_direction = False
        taskMgr.doMethodLater(self.TASK_CAN_CHANGE_TIME,
                              self.canChangeAgain, 'cool-off' + self.taskName)

    def canChangeAgain(self, task):
        self.can_change_direction = True
        return task.done

    def kill(self):
        if self.is_boss:
            base.messenger.send("bossKilled")
        if not self.direction and not self.can_fire:
            return
        self.direction = None
        self.can_fire = False
        self.is_in_game = False
        self.actor.setPos(self.indexNumber-10, self.indexNumber-10, 100)

    def updatePos(self, dt):
        self.updatePosActor(dt)

    def fire(self):
        if self.enemy_type != self.TYPE_SHOOTER:
            return

        self.can_fire = False
        taskMgr.doMethodLater(self.fire_later_time,
                              self.reset_fire, self.name+"_fire")

    def reset_fire(self, task):
        self.can_fire = True
        return task.done

    def chase_player(self, player_pos):
        if not self.can_change_direction:
            return
        px, py, pz = player_pos
        ex, ey, ez = self.getPos()
        x = px - ex
        y = py - ey
        self.is_turning_horizontal = not self.is_turning_horizontal
        if self.is_turning_horizontal:
            self.direction = self.WEST if x < 0 else self.EAST
        else:
            self.direction = self.SOUTH if y < 0 else self.NORTH
        self.can_change_direction = False
        taskMgr.doMethodLater(self.TASK_CAN_CHANGE_TIME,
                              self.canChangeAgain, 'cool-off' + self.taskName)
