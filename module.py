from math import *
from OpenNero import *
from common import *
from constants import *
from BlocksPlanning.environment import TowerEnvironment
import BlocksPlanning.agent

class TowerMod:
    # initializer
    def __init__(self):
        print 'Creating TowerMod'
        self.environment = None
        self.agent_id = None # the ID of the agent
        self.marker_map = {} # a map of cells and markers so that we don't have more than one per cell
        self.marker_states = {} # states of the marker agents that run for one cell and stop
        self.agent_map = {} # agents active on the map
        self.wall_ids = [] # walls on the map

    def __del__(self):
        print 'Deleting TowerMod'

    # add a set of coordinate axes
    def addAxes(self):
        getSimContext().addAxes()

    def add_maze(self):
        """Add a randomly generated maze"""
        if self.environment:
            print "ERROR: Environment already created"
            return
        self.set_environment(TowerEnvironment())

    def set_environment(self,env):
        self.environment = env
        for id in self.wall_ids: # delete the walls
            removeObject(id)
        del self.wall_ids[:] # clear the ids
        set_environment(env)

        self.block_ids = []

    def num_towers(self):
        return num_towers

    def start_tower(self,n):
        """ start the tower demo """
        self.num_towers = n
        disable_ai()
        if self.environment.__class__.__name__ != 'TowerEnvironment':
            self.set_environment(TowerEnvironment())
        get_environment().set_num_towers(n)
        if len(self.environment.block_states) == 0:
            self.agent_id = addObject("data/shapes/character/BlocksRobot.xml", \
            Vector3f(GRID_DX, GRID_DY, 2), type=AGENT_MASK,scale=Vector3f(3,3,3))
        else:
            for obj in self.environment.states: self.environment.reset(obj)
        enable_ai()

    def set_speedup(self, speedup):
        print 'Speedup set to', speedup
        # speed up between 0 (delay set to 1 second) and 1 (delay set to 0)
        getSimContext().delay = 1.0 - speedup

gMod = None

def delMod():
    global gMod
    gMod = None

def getMod():
    global gMod
    if not gMod:
        gMod = TowerMod()
    return gMod
