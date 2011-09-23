from OpenNero import *
from common import *
import BlocksPlanning
import random
from BlocksPlanning.environment import TowerEnvironment
from BlocksPlanning.constants import *
from BlocksPlanning.strips import *

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
    ('Pole1', 'Pole2'): [4, 1, 5], \
    ('Pole1', 'Pole3'): [4, 1, 1, 5], \
    ('Pole2', 'Pole1'): [5, 1, 4], \
    ('Pole2', 'Pole3'): [4, 1, 1, 5], \
    ('Pole3', 'Pole1'): [5, 1, 1, 4], \
    ('Pole3', 'Pole2'): [5, 1, 4] \
}
# move with pick up and put down
CARRY_MOVES = {}
for (source, dest) in MOVES:
    CARRY_MOVES[(source, dest)] = [3] + MOVES[(source, dest)] + [2]

class TowerAgent(AgentBrain):
    """
    An agent that uses a planner to solve a STRIPS planning problem
    """
    def __init__(self):
        AgentBrain.__init__(self) # have to make this call
        self.action_queue = [5] # rotate left to reset state first
    
    def initialize(self,init_info):
        # Create new Agent
        self.action_info = init_info.actions
        return True

    def start(self, time, sensors):
        """
        return first action given the first observations
        """
        w = get_environment().world
        locations = get_environment().locations
        # Did someone start us at the goal?
        already_solved = w.goal_reached()
        if not already_solved:
            print "Solving..."
            solution = solve(w)
            if solution is None:
                print "No solution found :("
            else:
                print "Solved! Plan: {0}".format(" -> ".join([x.simple_str() for x in reversed(solution)]))
                # convert the plan into agent actions
                for action in reversed(solution):
                    print action.simple_str()
                    disk = action.literals[0]
                    source = action.literals[1]
                    dest = action.literals[2]
                    print 'BEFORE:', disk, source, dest, 'disk at:', locations[disk], 'agent at:', locations['Agent']
                    if locations[disk] != locations['Agent']:
                        self.action_queue.extend(MOVES[(locations['Agent'], locations[disk])])
                        locations['Agent'] = locations[disk]
                    self.action_queue.extend(CARRY_MOVES[(locations[source], locations[dest])])
                    locations[disk] = locations[dest]
                    locations['Agent'] = locations[dest]
                #from show_strips import show_solution
                #show_solution(solution)
        if self.action_queue:
            return self.action_queue.pop(0)
        else:
            return 0

    def reset(self):
        pass

    def act(self, time, sensors, reward):
        """
        return an action given the reward for the previous action and the new observations
        """
        if self.action_queue:
            return self.action_queue.pop(0)
        else:
            return 0

    def end(self, time, reward):
        """
        receive the reward for the last observation
        """
        return True

    def destroy(self):
        """
        called when the agent is done
        """
        return True
