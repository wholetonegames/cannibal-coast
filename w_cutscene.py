from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from direct.gui.DirectGui import DirectFrame
import z_m
import y_helpers


class Cutscene:
    def __init__(self, text, img):
        self.frameMain = DirectFrame(
            frameSize=(base.a2dLeft, base.a2dRight,
                       base.a2dBottom, base.a2dTop),
            frameColor=y_helpers.GREEN
        )

        self.myImage = OnscreenImage(image=img, pos=(0, 0, 0))
        self.myImage.setTransparency(TransparencyAttrib.MAlpha)
        self.myImage.reparentTo(self.frameMain)

        self.textNode = OnscreenText(text, 1, fg=y_helpers.YELLOW, pos=(
            0, 0), align=TextNode.ABoxedCenter, scale=.07, mayChange=False)
        self.textNode.reparentTo(self.frameMain)

    def quit(self):
        self.frameMain.removeNode()

    def readKeys(self, task):
        if base.commandMap[base.BUTTON_CANCEL]:
            base.messenger.send(z_m.PLAY_CANCEL)

        return task.cont
