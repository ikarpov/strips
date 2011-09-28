from OpenNero import *
from random import seed, randint

# add the key and mouse bindings
from inputConfig import createInputMapping

from common import *
import common.gui as gui

from BlocksPlanning.module import getMod, delMod
from BlocksPlanning.constants import *
from BlocksPlanning.environment import TowerEnvironment

#########################################################

def CreateGui(guiMan):
    print 'CreateGui'
    guiMan.setTransparency(1.0)
    guiMan.setFont("data/gui/fonthaettenschweiler.bmp")

    towerButton3 = gui.create_button(guiMan, 'tower3', Pos2i(0,0), Pos2i(150,30), '')
    towerButton3.text = '3 Layer Towers of Hanoi'
    towerButton3.OnMouseLeftClick = lambda: getMod().start_tower(3)

    agentWindow = gui.create_window(guiMan, 'agentWindow', Pos2i(20, 20), Pos2i(150, 120), 'Agent')
    agentWindow.addChild(towerButton3)

    speedupValue = gui.create_text(guiMan, 'speedupEditBox', Pos2i(260, 30), Pos2i(100, 30), str(0))

    speedupLabel = gui.create_text(guiMan, 'speedupLabel', Pos2i(10, 30), Pos2i(100, 30), 'Speedup:')

    speedupScroll = gui.create_scroll_bar(guiMan, 'speedupScroll', Pos2i(100, 30), Pos2i(150,20), True)
    speedupScroll.setMax(100)
    speedupScroll.setLargeStep(10)
    speedupScroll.setSmallStep(1)
    speedupScroll.setPos(0)
    getMod().set_speedup(0)
    speedupScroll.OnScrollBarChange = speedup_adjusted(speedupScroll, speedupValue)

    paramWindow = gui.create_window(guiMan, 'paramWindow', Pos2i(20, 500), Pos2i(300,100), 'Parameters')
    paramWindow.addChild(speedupLabel)
    paramWindow.addChild(speedupScroll)
    paramWindow.addChild(speedupValue)

def speedup_adjusted(scroll, value):
    # generate a closure that will be called whenever the speedup slider is adjusted
    value.text = str(scroll.getPos())
    getMod().set_speedup(float(scroll.getPos())/100)
    def closure():
        value.text = str(scroll.getPos())
        getMod().set_speedup(float(scroll.getPos())/100)
    return closure

def recenter(cam):
    def closure():
        cam.setPosition(Vector3f(NUDGE_X, NUDGE_Y, 30))
        cam.setTarget(Vector3f(NUDGE_X + GRID_DX * ROWS / 2, NUDGE_Y + GRID_DY * COLS / 2, 5))
    return closure

def ClientMain():
    # create fog effect
    getSimContext().setFog()

    # add a camera
    camRotateSpeed = 100
    camMoveSpeed   = 3000
    camZoomSpeed   = 100
    cam = getSimContext().addCamera(camRotateSpeed, camMoveSpeed, camZoomSpeed)
    cam.setFarPlane(5000)
    cam.setEdgeScroll(False)
    recenter_cam = recenter(cam) # create a closure to avoid having a global variable
    recenter_cam() # call the recenter function

    # load the background
    #addObject("data/terrain/Sea.xml", Vector3f(-3000 + NUDGE_X,-3000 + NUDGE_Y,-20))
    addObject("data/terrain/FlatTerrain.xml", Vector3f(-500,-500,0), Vector3f(0,0,0)) #Vector3f(-1100 + NUDGE_X, -2400 + NUDGE_Y, -17), Vector3f(0,0,-45))
    addSkyBox("data/sky/irrlicht2")

    # load the environment
    getSimContext().addLightSource(Vector3f(-500,-500,1000), 1500)
    getMod().set_environment(TowerEnvironment())

    # load the GUI
    CreateGui(getGuiManager())

    # create the key binding
    ioMap = createInputMapping()
    ioMap.BindKey( "KEY_SPACE", "onPress", recenter_cam )
    getSimContext().setInputMapping(ioMap)
