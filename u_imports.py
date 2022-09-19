from x_maps import MapsModel
from x_game import GameModel
from u_render import ConfigRender
from u_sound import ConfigSound
import y_md5_check
import my_md5
from panda3d.core import (
    PandaSystem,
    CollisionTraverser,
    CollisionHandlerQueue,
    CollisionHandlerPusher,
    loadPrcFileData,
    VirtualFileSystem)
from panda3d.core import Filename
from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import DirectFrame


class ConfigImports(ConfigRender):
    def __init__(self):
        self.loadingText = None
        self.load_assets()
        base.cTrav = CollisionTraverser()
        # turning on Rapidly-Moving Objects
        base.cTrav.setRespectPrevTransform(True)
        base.pusher = CollisionHandlerPusher()
        ConfigRender.__init__(self)
        self.sound = ConfigSound()
        self.elapsedSeconds = 0
        self.mapData = MapsModel()
        self.gameData = GameModel('./saves/')

        # print(PandaSystem.getVersionString())
        self.load_fonts()

        # this needs to be called only when game starts
        taskMgr.add(self.updateTime, 'updateTime')
        # before starting a new game
        # taskMgr.remove('updateTime')

    def userExit(self):
        quit()

    def updateTime(self, task):
        self.elapsedSeconds = int(globalClock.getFrameTime())
        return task.cont

    def load_assets(self):
        filename = "assets.mf"
        read_md5 = y_md5_check.md5_sum(filename)
        assert read_md5 == my_md5.correct
        vfs = VirtualFileSystem.getGlobalPtr()
        if vfs.mount(filename, ".", VirtualFileSystem.MFReadOnly):
            print('mounted')

    def load_fonts(self):
        self.font_title = base.loader.loadFont('SkullphabetOne.ttf')
        self.font_title.setPixelsPerUnit(80)

    def callLoadingScreen(self):
        self.loadingText = DirectFrame(
            frameSize=(base.a2dLeft, base.a2dRight,
                       base.a2dBottom, base.a2dTop),
            frameColor=(0, 0, 0, 1.0)
        )

        txt = OnscreenText("Loading...", 1, fg=(1, 1, 1, 1), pos=(
            0, 0), align=TextNode.ACenter, scale=.07, mayChange=True)
        txt.reparentTo(self.loadingText)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

    def removeLoadingScreen(self):
        if self.loadingText:
            self.loadingText.removeNode()
        self.loadingText = None
