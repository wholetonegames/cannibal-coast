import webbrowser
from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from i_menu import IMenu
import z_m
import y_helpers


class StartMenu(IMenu):

    def __init__(self):
        frame = DirectFrame(
            frameSize=(base.a2dLeft, base.a2dRight,
                       base.a2dBottom, base.a2dTop),
            frameColor=y_helpers.YELLOW
        )
        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = [
            {"event": z_m.MENU_START, "text": "New game"},
            {"event": z_m.MENU_LOAD, "text": "Continue game"},
            {"event": z_m.MENU_QUIT, "text": "Quit"}
        ]
        self.addTitle()
        self.createVerticalButtons()

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ACenter,
                                scale=0.07,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(0, 0,
                                     (-.10 - (index * .15))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                boxPlacement="below",
                                text_fg=y_helpers.GREEN,
                                command=self.menuVerticalEvent)

        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def addTitle(self):
        self.title = OnscreenText(
            base.appName, 1,
            fg=y_helpers.GREEN,
            pos=(0, 0.3),
            font=base.font_title,
            align=TextNode.ACenter,
            scale=.3,
            mayChange=True)
        self.title.reparentTo(self.frameMain)

    def cancelCommand(self):
        pass
