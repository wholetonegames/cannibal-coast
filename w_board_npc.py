from i_stage import IStage
from w_npc import ItemNPC
import z_m


class BoardNPC(IStage):
    def __init__(self):
        IStage.__init__(self, "npc")
        self.setup()
        self.setCollision()
        self.stop()

    def init_charas_items(self):
        self.initNPCItem()

    def initNPCItem(self):
        itemNumber = self.this_map["itemNumber"]
        self.itemActors = []
        for itemIndex in list(range(0, itemNumber)):
            i_type = self.stage_grid.itemBlockKeys[itemIndex]
            i = ItemNPC(i_type, itemIndex, self.stage,
                        self.stage_grid.map_boundaries)
            self.itemActors.append(i)

    def aiUpdate(self, task):
        dt = globalClock.getDt()
        self.update_hero(dt)
        for n in self.npcActors:
            n.updatePos(dt)
        return task.cont

    def intoEvent(self, entry):
        if not self.canEnemiesMove or not entry.hasInto():
            return

        intoName, fromName = self.getIntoFromNames(entry)

        if self.NAME_EXIT in intoName and self.NAME_HERO in fromName:
            self.requestBoardChange()
            return

        if self.NAME_ITEM in intoName and self.NAME_HERO in fromName:
            self.intoItem(intoName)
            return

    def requestBoardChange(self):
        base.messenger.send(z_m.MENU_GAMEOVER)

    def againEvent(self, entry):
        pass

    def cancelCommand(self):
        base.messenger.send(z_m.MENU_PAUSE)

    def readCommand(self, p):
        if base.commandMap[base.BUTTON_CANCEL]:
            self.cancelCommand()
