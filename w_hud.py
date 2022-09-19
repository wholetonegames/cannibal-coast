from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DGG,
    DirectFrame,
    DirectLabel)


class HUD:
    OFFSET = 0.005
    POS_Y = 0.9

    def __init__(self):
        self.frameMain = DirectFrame(
            frameSize=(base.a2dLeft, base.a2dRight,
                       base.a2dBottom, base.a2dTop),
            frameColor=(0, 0, 0, 0)
        )
        self.heroAmmo = None
        self.heroHP = None
        self.set_lives()
        self.set_ammo()

    def show(self):
        self.frameMain.show()

    def hide(self):
        self.frameMain.hide()

    def add_lives(self):
        self.heroHP = OnscreenText(
            "", 1,
            fg=(1, 1, 1, 1),
            shadow=(0, 0, 0, 1),
            pos=(base.a2dLeft + 0.2, self.POS_Y),
            align=TextNode.ALeft,
            scale=.1,
            mayChange=True)
        self.heroHP.reparentTo(self.frameMain)

    def set_lives(self):
        if not self.heroHP:
            self.add_lives()
        self.heroHP.text = "Level {} / {} - ".format(
            base.gameData.current_board_index + 1, base.mapData.last_index + 1)
        self.heroHP.text += '{} Health: {}%'.format(
            base.gameData.player_name, base.gameData.heroHP)
        self.heroHP.show()

    def add_ammo(self):
        self.heroAmmo = OnscreenText(
            "", 1,
            fg=(1, 1, 1, 1),
            shadow=(0, 0, 0, 1),
            pos=(base.a2dLeft + 2.55, self.POS_Y),
            align=TextNode.ALeft,
            scale=.1,
            mayChange=True)
        self.heroAmmo.reparentTo(self.frameMain)

    def set_ammo(self):
        if not self.heroAmmo:
            self.add_ammo()
        self.heroAmmo.text = 'Bullets x {}'.format(base.gameData.ammo)
        self.heroAmmo.show()
