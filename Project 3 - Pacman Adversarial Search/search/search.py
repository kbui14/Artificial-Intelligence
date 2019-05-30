# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from asyncore import loop
from Tkconstants import CURRENT


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).

Project 1: Path-based Location Search (Chapter 3)
Course: CS430
Name: Kevin Bui & Joshua Wood
Instructor: Dr. Daniel Grissom
Date: 9/27/17
etc.

This file contains the search functions for 4 different methods. 
These methods are Breath First Search, Depth First Search, Uniform Cost Search, and A* Search
The methods find paths using their specific queuing strategies and return the result to a 
pacman game. 


"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    
    # First we define our stack data structure and instantiate it with the start state
    stack = util.Stack()
    for successor in problem.getSuccessors(problem.getStartState()):
        # The empty list after successor will contain the solution path
        stack.push((successor, []))
        
    # The visited set starts as a empty set
    visitedSet = set()
    
    # This method checks if a given stack contains a given node 
    def stackContainsNode(stack, coord):
        for item in stack.list:
            if item[0][0] == coord:
                return True
        return False
    
    # Infinite loop that is just broken by returns
    while True:
        
        # If the fringe is empty the search has failed
        if stack.isEmpty():
            return False
        
        # We pop the current node, with its corresponding path off the fringe 
        currentNode, currentPath = stack.pop()
        
        # If the problem is solved 
        if problem.isGoalState(currentNode[0]):
            # We calculate the path to the solution and return it
            solution = currentPath + [currentNode[1]]
            return solution
        
        # If the node we are on is not in the stack and not visited
        if not(stackContainsNode(stack, currentNode[0])) and not(setContainsNode(visitedSet, currentNode[0])):
            # We add it to our visited
            visitedSet.add(currentNode[0])
            # We calculate the new path 
            path = currentPath + [currentNode[1]]
            # We then put the successors of this node into the fringe by pushing
            for successor in problem.getSuccessors(currentNode[0]):
                stack.push((successor, path))
    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    
    # We first define the data structure of our queue and then give it the initial problem
    queue = util.Queue()
    for successor in problem.getSuccessors(problem.getStartState()):
        queue.push([successor, []])
        
    # Start with an empty set for visited set
    visitedSet = set()
    
    # This method checks if a 
    def queueContainsNode(queue, coord):
        for item in queue.list:
            if item[0][0] == coord:
                return True
        return False
    
    # We set up an infinite loop to search through the problem, it will be broken by return statements 
    while True:
        
        # If our fringe is empty, we quit, the search has failed to find solution
        if queue.isEmpty():
            print "Failed"
            return False
        
        # We pop the next thing off the queue, including the node and the path to that node 
        currentNode, currentPath = queue.pop()
                
        # If the current node is our goal
        if problem.isGoalState(currentNode[0]):
            # We must find the path including the path to the node we are on
            solution = currentPath + [currentNode[1]]
            # Then we return the solution, which is the path to get to the goal state
            return solution
        
        # If the fringe doesn't contain the node and it hasn't been visited
        if not(queueContainsNode(queue, currentNode[0])) and not(setContainsNode(visitedSet, (currentNode[0]))):
            # We add the current node to our visited set
            visitedSet.add(currentNode[0])
            # We calculate the new path adding the direction from the current node 
            path = currentPath + [currentNode[1]]
            # We add the successors of the current node to the fringe by pushing
            for successor in problem.getSuccessors(currentNode[0]):
                queue.push((successor, path))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    
    # We create a priority queue and fill it with the start state
    PriorityQueue = util.PriorityQueue()
    for successor in problem.getSuccessors(problem.getStartState()):
        # We use a priority queue and use the cost as our priority
        PriorityQueue.push((successor, []), successor[2])
        
    # Once again, empty visited set
    visitedSet = set()
    
    # This checks if a given priority queue contains a given coord
    def pQueueContainsNode(PriorityQueue, coord):
        for item in PriorityQueue.heap:
            if item[0] == coord:
                return True
        return False
    
    # This is our infinite loop
    while True:
        
        # If empty we failed (or the problem was impossible)
        if PriorityQueue.isEmpty():
            return False
        
        # Pop the node and path from the priority queue 
        currentNode, currentPath = PriorityQueue.pop()
        
        # Yay we won
        if problem.isGoalState(currentNode[0]):
            solution = currentPath + [currentNode[1]]
            # Return the spoils of our search victory
            return solution
        
        # If the node is not on the fringe and not visited 
        if not(pQueueContainsNode(PriorityQueue, currentNode[0])) and not(setContainsNode(visitedSet, currentNode[0])):
            # We mark it as visited
            visitedSet.add(currentNode[0])
            path = currentPath + [currentNode[1]]
            # Once again, we find the successors and use the cost as our priority
            for successor in problem.getSuccessors(currentNode[0]):
                PriorityQueue.push((successor, path), successor[2])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    # Once again we use a priority queue, we instead use estimated cost as our priority 
    pQueue = util.PriorityQueue()
    for successor in problem.getSuccessors(problem.getStartState()):
        # We calculate the estimated cost by adding our heuristic to the cost
        estCost = heuristic(successor[0], problem) + successor[2]
        pQueue.push((successor, []), estCost)

    # another searching strategy, another empty visited set
    visitedSet = set()

    # Much like before, this checks if a given priority queue contains a given coord
    def pQueueContainsNode(PriorityQueue, node):
        for item in PriorityQueue.heap:
            if item[2][0] == node:
                return True
        return False

    # this loop doesn't end unless we return
    while True:

        # The queue is empty, as are our hopes of finding a solution
        if pQueue.isEmpty():
            return False

        # Pop out that node and path
        currentNode, currentPath = pQueue.pop()

        # We found the way
        if problem.isGoalState(currentNode[0]):
            solution = currentPath + [currentNode[1]]
            # We tell pacman the way
            return solution

        # If we have never been there and it isn't on our fringe
        if not(pQueueContainsNode(pQueue, currentNode)) and not(setContainsNode(visitedSet, currentNode[0])):
            # Now we been there
            visitedSet.add(currentNode[0])
            path = currentPath + [currentNode[1]]
            # Now we add the successors to the fringe, once again calculating estimated cost and using that as our priority
            for successor in problem.getSuccessors(currentNode[0]):
                estCost = heuristic(successor[0], problem) + successor[2]
                pQueue.push((successor, path), estCost)

# This method checks if a given set contains a given node
def setContainsNode(set, node):
    for item in set:
        if item == node:
            return True
    return False

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
