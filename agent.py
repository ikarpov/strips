from OpenNero import *
from common import *
import BlocksPlanning
import random
from BlocksPlanning.environment import TowerEnvironment
from BlocksPlanning.constants import *
from strips2 import solve, print_plan
from towers3 import *

def get_action_index(move):
    if move in TowerEnvironment.MOVES:
        action = TowerEnvironment.MOVES.index(move)
        print 'Picking action', action, 'for move', move
        return action
    else:
        return None

class Cell:
    def __init__(self, h, r, c):
        self.h = h
        self.r = r
        self.c = c
    def __cmp__(self, other):
        return cmp(self.h, other.h)

###
#
# Action definitions:
# 0 Jump
# 1 Move Forward
# 2 Put Down
# 3 Pick Up
# 4 Rotate Right
# 5 Rotate Left
#
###

# action primitives
# move without getting stuff
MOVES = { \
    (Pole1, Pole2): [4, 1, 5], \
    (Pole1, Pole3): [4, 1, 1, 5], \
    (Pole2, Pole1): [5, 1, 4], \
    (Pole2, Pole3): [4, 1, 1, 5], \
    (Pole3, Pole1): [5, 1, 1, 4], \
    (Pole3, Pole2): [5, 1, 4] \
}

# move with pick up and put down
CARRY_MOVES = {}
for (source, dest) in MOVES:
    CARRY_MOVES[(source, dest)] = [3] + MOVES[(source, dest)] + [2]

class TowerAgent(AgentBrain):
    """
    An agent that uses a STRIPS-like planner to solve the Towers of Hanoi problem
    """
    def __init__(self):
        AgentBrain.__init__(self) # have to make this call
        self.action_queue = [5] # rotate left to reset state first

    def initialize(self,init_info):
        """
        Create the agent.
        init_info -- AgentInitInfo that describes the observation space (.sensors),
                     the action space (.actions) and the reward space (.rewards)
        """
        self.action_info = init_info.actions
        return True

    def start(self, time, observations):
        """
        return first action given the first observations
        """
        def planner(viewer):
            solve(INIT, GOAL, ACTIONS, viewer=viewer)
        from strips2_show import demo_planner
        plan = demo_planner(planner)
        if plan is not None:
            print_plan(plan)
        return 0

    def act(self, time, observations, reward):
        """
        return an action given the reward for the previous
        action and the new observations
        """
        return 0

    def end(self, time, reward):
        """
        receive the reward for the last observation
        """
        return True

    def reset(self):
        return True

    def destroy(self):
        """
        called when the agent is done
        """
        return True
