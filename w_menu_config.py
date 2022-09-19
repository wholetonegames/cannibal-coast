from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DGG,
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from i_menu import IMenu
import z_m


class ConfigMenu(IMenu):
    def __init__(self):
        frame = DirectFrame(
            frameSize=(base.a2dLeft, base.a2dRight,
                       base.a2dBottom, base.a2dTop),
            frameColor=(0, 0, 0, 0.5)
        )
        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = [
            {"event": "*", "text": "Sound Effects Volume Level < >"},
            {"event": "*", "text": "Music Volume Level < >"},
            {"event": "*", "text": "Controls"},
            {"event": z_m.BACK_GAME, "text": "Resume Game"},
            {"event": z_m.BACK_START, "text": "Back to Start Menu"}
        ]
        self.menuHorizontalChoices = [
            {"event": z_m.CHARA_SUB, "text": "*"},
            {"event": z_m.CHARA_ADD, "text": "*"}
        ]
        self.statsSheet = None
        self.createVerticalButtons()
        self.addTitle()
        self.config_stats()

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.05,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(base.a2dLeft + 0.7, 0,
                                     (0.5 - (index * .15))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)

        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def addTitle(self):
        self.title = OnscreenText(
            'Configurations', 1,
            fg=(1, 0, 0, 1),
            pos=(base.a2dLeft + 0.7, 0.8),
            font=base.font_title,
            align=TextNode.ALeft,
            scale=.15,
            mayChange=True)
        self.title.reparentTo(self.frameMain)

    def cancelCommand(self):
        pass

    def change_config(self, value):
        index = self.menuVerticalChoice[0]
        stats = [
            self.change_sfx_vol,
            self.change_bgm_vol,
        ]
        if index < len(stats):
            stats[index](value)
            self.config_stats()

    def change_bgm_vol(self, value):
        payload = base.gameData.bgm_vol + (value * 0.1)
        payload = max(payload, 0.0)
        payload = min(payload, 1.0)
        base.gameData.bgm_vol = payload
        base.messenger.send("BGMvolume")

    def change_sfx_vol(self, value):
        payload = base.gameData.sfx_vol + (value * 0.1)
        payload = max(payload, 0.0)
        payload = min(payload, 1.0)
        base.gameData.sfx_vol = payload
        base.messenger.send("SFXvolume")

    def config_stats(self):
        if self.statsSheet:
            self.statsSheet.detachNode()
        self.statsSheet = DirectFrame(
            frameSize=(base.a2dLeft, base.a2dRight,
                       base.a2dBottom, base.a2dTop),
            frameColor=(0, 1, 0, 0)
        )
        stats = [
            '{} %'.format(int(base.gameData.sfx_vol * 100)),
            '{} %'.format(int(base.gameData.bgm_vol * 100)),
        ]
        self.set_controls(stats)
        i = 0
        for stat in stats:
            self.set_stat(stat, i)
            i += 1
        self.statsSheet.reparentTo(self.frameMain)

    def set_controls(self, arr):
        # ["z", self.setCommand,  [base.BUTTON_CANCEL, True], self.TYPE_KEYBOARD, "Z Key"]
        output = ''
        for ctrl in base.controlList:
            if ctrl[3] != base.control_type or not ctrl[4]:
                continue
            output += '{} - {}\n'.format(ctrl[2][0], ctrl[4])
        arr.append(output)

    def set_stat(self, text, index):
        stat = DirectLabel(
            scale=0.05,
            text_align=TextNode.ALeft,
            pos=(0, 0, (0.5 - (index * .15))),
            pad=(0.5, 0.5),
            frameColor=(0, 0, 0, 0.0),
            text=text,
            text_fg=(1, 1, 1, 1))
        stat.reparentTo(self.statsSheet)

    def readKeys(self, task):
        keysPressed = base.getKeysPressedTotal()

        if keysPressed == 0:
            self.isButtonUp = True

            if base.commandMap[base.BUTTON_CONFIRM]:
                self.menuVerticalEvent()
                base.messenger.send(z_m.PLAY_CONFIRM)
            elif base.commandMap[base.BUTTON_CANCEL]:
                self.cancelCommand()
                base.messenger.send(z_m.PLAY_CANCEL)

            base.resetButtons()
            return task.cont

        if not self.isButtonUp:
            return task.cont

        if base.directionMap[base.DIRECTION_UP]:
            self.navigateChoice(-1, self.menuVerticalChoice,
                                self.menuVerticalChoicesList)
            self.isButtonUp = False
        elif base.directionMap[base.DIRECTION_DOWN]:
            self.navigateChoice(1, self.menuVerticalChoice,
                                self.menuVerticalChoicesList)
            self.isButtonUp = False
        elif base.directionMap[base.DIRECTION_LEFT]:
            self.menuHorizontalChoice[0] = 0
            self.isButtonUp = False
            self.menuHorizontalEvent()
        elif base.directionMap[base.DIRECTION_RIGHT]:
            self.menuHorizontalChoice[0] = 1
            self.isButtonUp = False
            self.menuHorizontalEvent()

        base.resetButtons()
        return task.cont
