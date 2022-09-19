from panda3d.core import (
    AntialiasAttrib,
    NodePath,
    ClockObject,
    PerspectiveLens,
    DirectionalLight,
    AmbientLight,
    Spotlight,
    PandaNode,
    LightRampAttrib)
from direct.gui.DirectGui import DGG
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.Transitions import Transitions
from direct.interval.IntervalGlobal import Sequence, Func, Wait
import z_m


class ConfigRender:
    def __init__(self):
        render.setAntialias(AntialiasAttrib.MMultisample)
        # render.setRenderModeWireframe()
        DGG.getDefaultFont().setPixelsPerUnit(100)
        self.setShaders()
        self.initLights()
        self.initTransitions()
        self.setFPS()
        self.setCam()

    def setCam(self):
        base.camLens.setNearFar(10, 500)
        # base.camLens.setFov(40)

    def setShaders(self):
        if not base.win.getGsg().getSupportsBasicShaders():
            print("Toon Shader: Video driver reports that Cg shaders are not supported.")
            return

        tempnode = NodePath(PandaNode("temp node"))

        tempnode.setAttrib(LightRampAttrib.makeHdr0())
        self.filters = CommonFilters(base.win, base.cam)

        # GLOW
        self.filters.setBloom(blend=(0.3, 0.4, 0.3, 0.0), mintrigger=0.6,
                              maxtrigger=1.0, desat=0.6, intensity=1.0, size="medium")

        tempnode.setShaderAuto()
        base.cam.node().setInitialState(tempnode.getState())

    def initLights(self):
        ambientLight = AmbientLight("ambient_light")
        ambientLight.setColor((0.2, 0.2, 0.2, 1))
        self.alnp = render.attachNewNode(ambientLight)
        sunLens = PerspectiveLens()
        sunLens.setFilmSize(50)
        sun = DirectionalLight("sun")
        sun.setColor((1, 1, 1, 1))
        # sun.setShadowCaster(True, 4096, 4096)  # highest working value
        sun.setScene(render)
        # sun.showFrustum()
        sunLens.setFov(120, 40)
        sunLens.setNearFar(2, 100)
        sun.setLens(sunLens)
        self.sunNp = render.attachNewNode(sun)

    def setFPS(self):
        FPS = 30
        globalClock = ClockObject.getGlobalClock()
        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(FPS)

    def initTransitions(self):
        self.transitions = Transitions(loader)
        self.transitions.setFadeColor(0, 0, 0)
        self.transitionTime = 0.2
        base.accept(z_m.FADE_OUT, self.transitions.fadeOut,
                    [self.transitionTime])
        base.accept(z_m.FADE_IN, self.transitions.fadeIn,
                    [self.transitionTime])
        base.accept(z_m.FADE_NO, self.transitions.noFade)
