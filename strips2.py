from copy import copy
from towers3 import *

__doc__ = """This is an example planning algorithm for Towers of Hanoi"""
__author__ = "Igor Karpov <ikarpov@cs.utexas.edu>"
__version__ = "0.1"

DEPTH = 7

def solve(start, goal, actions, depth=DEPTH, plan=[], show_state = None ):
    """
    solve( start, goal, actions, depth=DEPTH )

    A STRIPS-like planner

    Arguments:

    start -- a set of tuples that make up the starting state
    goal -- a set of tuples that make up the goal state
    actions -- a list of (Do, Undo) pairs that operate on the state
        (currently we assume that the signature is
        Do(Disk, Source, Dest) -> {True, False})
    depth -- the maximum depth of recursion to allow the algorithm to search for a plan

    Returns:

    A plan of actions (represented as tuples with function followed by their arguments) which will,
    starting at the start state, reach the goal state
    """
    # if the goal is a subset of the starting state
    if goal.issubset(start):
        # this is already solved!
        if show_state: show_state(start)
        print_plan(plan)
        return plan
    # if we are below depth, stop
    elif depth <= 0:
        return None
    # otherwise we actually need to do some work
    else:
        # we will need to modify the state so we make a copy of it
        state = set(start)
        if state: show_state(state)
        # try all actions with all parameters
        # WARNING: this could get big quickly!
        for (do, undo) in actions:
            for Disk in DISKS:
                for Source in set(LITERALS) - set([Disk]):
                    for Dest in set(LITERALS) - set([Disk, Source]):
                        action = (do, Disk, Source, Dest)
                        if do(state, Disk, Source, Dest):
                            new_state = frozenset(state)
                            # yield all of the states and plans encountered below us
                            sln = solve(new_state, goal, actions, depth = depth - 1, plan = plan + [action], show_state = show_state)
                            if sln is not None:
                                return sln
                            else:
                                # undo the action if it didn't work (backtrack)
                                undo(state, Disk, Source, Dest)
        return None

def print_plan(plan):
    for action in plan:
        print "%s(%s)" % (action[0].__name__, ', '.join(action[1:]))

if __name__ == "__main__":
    def planner(show_state):
        solve(INIT, GOAL, [(Move, UnMove)], show_state=show_state)
    from strips2_show import demo_planner
    demo_planner(planner)
