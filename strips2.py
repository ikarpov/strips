from copy import copy
from pprint import pprint
#from towers2 import *
from towers3 import *
from strips2_show import show_state

def solve(start, goal, actions, depth=5, states_seen = set([frozenset(GOAL)]) ):
    """
    A STRIPS-like planner algorithm

    Parameters:
     - start: a set of tuples that make up the starting state
     - goal: a set of tuples that make up the goal state
     - actions: a list of (Do, Undo) pairs that operate on the state (currently we assume that the signature is Do(Disk, Source, Dest) -> {True, False})
    """
    if goal.issubset(start):
        return [] # already solved!
    elif depth == 0:
        return None
    else:
        NEXT_STATES = []
        # unfreeze our state
        state = set(start)
        show_state(state)
        # try all actions
        for (do, undo) in actions:
            for Disk in DISKS:
                for Source in set(LITERALS) - set([Disk]):
                    for Dest in set(LITERALS) - set([Disk, Source]):
                        action = (do, Disk, Source, Dest)
                        if do(state, Disk, Source, Dest):
                            if goal.issubset(state):
                                # this is a solution!
                                show_state(state)
                                undo(state, Disk, Source, Dest)
                                return [action]
                            else:
                                new_state = frozenset(state)
                                if new_state not in states_seen:
                                    # we should try this action followed by some other actions
                                    NEXT_STATES.append((action, new_state))
                                    states_seen.add(new_state)
                                # back track - action did not lead to a solution
                                undo(state, Disk, Source, Dest)
        for (action, state) in NEXT_STATES:
            sln = solve(state, goal, actions, depth - 1)
            if sln is not None:
                return [action] + sln
        return None

if __name__ == "__main__":
    solution = solve(INIT, GOAL, [(Move, UnMove)], depth=7)
    if solution:
        print 'Solution found! Here is the plan:'
        for action in solution:
            print "%s(%s)" % (action[0].__name__, ', '.join(action[1:]))
    else:
        print 'Solution not found!'
