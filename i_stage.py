import abc
from panda3d.core import (
    CollisionHandlerPusher,
    CollisionNode,
    CollisionSphere,
    CollisionBox)
from w_grid import StageGrid
from w_moving_hero import PlayerCharacter
from w_hud import HUD


class IStage(metaclass=abc.ABCMeta):
    MAX_BULLET = 45
    NAME_HERO = 'hero'
    NAME_ENEMY = 'enemy'
    NAME_ITEM = 'item'
    NAME_WALL = 'wall'
    NAME_EXIT = 'exit'
    NAME_ENEMY_BULLET = 'bullet_e'
    NAME_HERO_BULLET = 'bullet_h'

    def __init__(self, stage_stype):
        self.stage_stype = stage_stype
        self.init_vars()

    def init_vars(self):
        self.stage = None
        self.hud = None
        self.camFocus = None
        self.enemyActors = []
        self.itemActors = []
        self.npcActors = []
        self.hero_bullets = []
        self.enemy_bullets = []
        self.smokes = []
        self.hero_bullet_index = 0
        self.enemy_bullet_index = 0
        self.canEnemiesMove = False

    def initStage(self):
        self.this_map = None
        if self.stage:
            self.stage.removeNode()
            del self.stage
        index = base.gameData.current_board_index
        self.this_map = base.mapData.maps[index]
        self.stage = loader.loadModel(self.this_map['model'])
        self.stage_grid = StageGrid(
            self.this_map['pattern'], self.stage, self.this_map['blockTypes'])
        self.stage.reparentTo(render)
        self.controlCamera()
        self.stage.hide()

    def controlCamera(self):
        camPos = self.stage.find(
            '**/camPos').getPos()
        self.camFocus = self.stage.find('**/camFocus').getPos()
        base.cam.setPos(camPos)
        base.cam.lookAt(self.camFocus)

        base.sunNp.setPos(-4, -34, 50)
        base.sunNp.lookAt(self.camFocus)

    def initPlayer(self):
        startPos = self.stage_grid.startPosList[0]
        self.player = PlayerCharacter(
            startPos,
            self.stage,
            base.gameData.heroHP,
            "hero_explorer",
            self.stage_grid.map_boundaries
        )

    def init_HUD(self):
        if self.hud:
            self.hud = None
            del self.hud
        self.hud = HUD()
        self.hud.hide()

    def setup(self):
        self.init_vars()
        self.initStage()
        self.initPlayer()
        self.init_charas_items()
        self.init_HUD()

    def setCollision(self):
        inEvent = "into"
        base.pusher.addInPattern(inEvent)
        base.accept(inEvent, self.intoEvent)

        againEvent = "again"
        base.pusher.addAgainPattern(againEvent)
        base.accept(againEvent, self.againEvent)

    def resetMap(self):
        self.setup()
        self.start()
        base.initController()

    def readDirection(self, p):
        if base.directionMap[base.DIRECTION_LEFT]:
            p.direction = p.WEST
        elif base.directionMap[base.DIRECTION_RIGHT]:
            p.direction = p.EAST
        elif base.directionMap[base.DIRECTION_UP]:
            p.direction = p.NORTH
        elif base.directionMap[base.DIRECTION_DOWN]:
            p.direction = p.SOUTH

        if not self.canEnemiesMove and p.direction:
            self.canEnemiesMove = True
        self.readCommand(self.player)

    def update_hero(self, dt):
        if self.player.is_ko:
            return
        self.readDirection(self.player)
        self.player.updatePos(dt)
        self.player.direction = None

    def start(self):
        render.setLight(base.alnp)
        render.setLight(base.sunNp)
        self.stage.show()
        self.hud.show()
        taskMgr.add(self.aiUpdate, "AIUpdate")

    def stop(self):
        self.hud.hide()
        # self.stage.hide()
        # render.clearLight()
        taskMgr.remove("AIUpdate")

    def quit(self):
        self.stage.removeNode()
        del self.stage

    def getIntoFromNames(self, entry):
        intoName = entry.getIntoNode().getName()
        fromName = entry.getFromNode().getName()
        return (intoName, fromName)

    def getIndexFromEvent(self, eventName):
        l = eventName.split("_")
        # -1 is the last part of the name
        return int(l[-1])

    def intoItem(self, intoName):
        itemIndex = self.getIndexFromEvent(intoName)
        item = self.itemActors[itemIndex]
        item.kill()

    @abc.abstractmethod
    def cancelCommand(self):
        raise NotImplementedError('subclass must define this method')

    @abc.abstractmethod
    def intoEvent(self, entry):
        raise NotImplementedError('subclass must define this method')

    @abc.abstractmethod
    def againEvent(self, entry):
        raise NotImplementedError('subclass must define this method')

    @abc.abstractmethod
    def aiUpdate(self, task):
        raise NotImplementedError('subclass must define this method')

    @abc.abstractmethod
    def readCommand(self, p):
        raise NotImplementedError('subclass must define this method')

    @abc.abstractmethod
    def requestBoardChange(self):
        raise NotImplementedError('subclass must define this method')

    @abc.abstractmethod
    def init_charas_items(self):
        raise NotImplementedError('subclass must define this method')
