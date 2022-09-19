from panda3d.core import (
    NodePath,
    PandaNode)
import z_grid
import random


class StageGrid:
    START_POS = '*'
    ENEMY = 'e'
    EXIT = 'x'
    WALL = '#'
    ITEMS = z_grid.ITEMS

    def __init__(self, map_str, stage, blockTypes):
        self.stage = stage
        self.enemy_index = 0
        self.item_index = 0
        self.rawList = map_str
        self.map_boundaries = {
            "xMin": 0, "xMax": 0, "yMin": 0, "yMax": 0,
        }
        self.startPosList = []
        self.itemBlockKeys = []
        self.optimize = NodePath(PandaNode("optimization node"))
        self.blockTypes = blockTypes
        self.loadBlocks()
        self.optimizeGeometry()

    def loadBlocks(self):
        index = 0
        for blockKey in self.rawList:
            index_str = str(index).zfill(5)
            blockName = self.stage.find(
                '**/block.{}'.format(index_str))
            blockPos = blockName.getPos()

            if index == 0 or index == len(self.rawList) - 1:
                self.setBoundaries(index, blockPos)

            block = self.blockTypes[blockKey]
            if not block:
                index += 1
                continue
            if blockKey == self.WALL:
                # wall will have more than one choice to be selected randomly
                blockModel = base.loader.loadModel("{}".format(random.choice(block)))
            else:
                blockModel = base.loader.loadModel("{}".format(block))
            blockModel.setPos(blockPos)
            if blockKey == self.START_POS:
                self.startPosList.append(blockPos)
            elif blockKey == self.ENEMY:
                self.addEnemy(blockName)
            elif blockKey in self.ITEMS:
                self.addItem(blockName, blockKey)
            else:
                blockModel.reparentTo(self.optimize)
                index += 1
                continue

            blockModel.reparentTo(self.stage)
            index += 1

    def addEnemy(self, blockName):
        blockName.setName('enemy_{}'.format(self.enemy_index))
        self.enemy_index += 1

    def addItem(self, blockName, blockKey):
        blockName.setName('item_{}_{}'.format(blockKey, self.item_index))
        self.itemBlockKeys.append(blockKey)
        self.item_index += 1

    def optimizeGeometry(self):
        self.optimize.flattenMedium()
        self.optimize.reparentTo(self.stage)

    def setBoundaries(self, index, blockPos):
        x, y, z = blockPos
        if index == 0:
            self.map_boundaries["xMin"] = x
            self.map_boundaries["yMax"] = y
        else:
            self.map_boundaries["xMax"] = x
            self.map_boundaries["yMin"] = y
