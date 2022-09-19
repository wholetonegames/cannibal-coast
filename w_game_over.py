from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DGG,
    DirectFrame,
    DirectLabel)
import z_m


class GameOverScreen:
    def __init__(self, is_player_ko, is_last_stage, is_save_stage):
        self.message = 'Game Over' if is_player_ko else 'Thank You\nFor Playing'
        self.frameMain = DirectFrame(
            frameSize=(base.a2dLeft, base.a2dRight,
                       base.a2dBottom, base.a2dTop),
            frameColor=(0, 0, 0, 0.5)
        )
        if is_player_ko:
            self.addTitle()
            taskMgr.doMethodLater(3.0, base.messenger.send,
                                  'callStartMenu', extraArgs=[z_m.BACK_START])
        elif is_last_stage:
            taskMgr.doMethodLater(0.1, base.messenger.send,
                                  'callCutscene', extraArgs=[z_m.BACK_CUTSCENE])
        else:
            base.messenger.send(z_m.CHANGE_BOARD_HP)
            if is_save_stage:
                base.messenger.send(z_m.SAVE_GAME)
            base.callLoadingScreen()
            base.next_map()
            taskMgr.doMethodLater(1.0, base.messenger.send,
                                  'callGameLoop', extraArgs=[z_m.BACK_GAME])

    def addTitle(self):
        self.title = OnscreenText(
            self.message, 1,
            fg=(1, 0, 0, 1),
            shadow=(0,0,0,0.8),
            pos=(0.0, 0.0),
            font=base.font_title,
            align=TextNode.ACenter,
            scale=.35,
            mayChange=True)
        self.title.reparentTo(self.frameMain)

    def quit(self):
        self.frameMain.removeNode()
