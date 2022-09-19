from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, PandaSystem
from u_fsm import ConfigFSM

appName = "Cannibal Coast"
loadPrcFileData("",
                """
    window-title {}
    win-size 1280 720
    fullscreen 0
    cursor-hidden 0
    show-frame-rate-meter 0
    model-path $MAIN_DIR/assets/
    framebuffer-multisample 1
    multisamples 2
""".format(appName))


class Main(ShowBase, ConfigFSM):
    def __init__(self, appName):
        self.appName = appName
        ShowBase.__init__(self)
        ConfigFSM.__init__(self)
        self.disableMouse()
        self.request('StartMenu')


game = Main(appName)
game.run()
