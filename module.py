from math import *
from OpenNero import *
from common import *
from constants import *
from BlocksPlanning.environment import TowerEnvironment
import BlocksPlanning.agent

class TowerMod:
    def __init__(self):
        """constructor"""
        print 'Creating TowerMod'
        self.environment = None
        self.agent_id = None # the ID of the agent
        self.wall_ids = [] # walls on the map

    def __del__(self):
        """destructor"""
        print 'Deleting TowerMod'

    def addAxes(self):
        """Add a set of coordinate axes"""
        getSimContext().addAxes()

    def set_environment(self,env):
        """Set the environment"""
        self.environment = env
        for id in self.wall_ids: # delete the walls
            removeObject(id)
        del self.wall_ids[:] # clear the ids
        set_environment(env)

        self.block_ids = []

    def start_tower(self,n):
        """ start the tower demo """
        self.num_towers = n
        disable_ai()
        if self.environment is None or not isinstance(self.environment, TowerEnvironment):
            self.set_environment(TowerEnvironment())
        self.environment.set_num_towers(n)
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
