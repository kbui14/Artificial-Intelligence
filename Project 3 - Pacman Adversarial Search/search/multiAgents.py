# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from Tkconstants import CURRENT

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        from util import manhattanDistance
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        oldFood = currentGameState.getFood()
        oldFoodList = oldFood.asList()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()
        # find the closest food from the current list
        closestFood = 1000000.0
        for food in foodList:
            dist = float(manhattanDistance(newPos, food))
            if dist < closestFood:
                closestFood = float(dist)
                
        # find the closest food from the old state
        closestFoodOld = 1000000.0
        for food in oldFoodList:
            dist = float(manhattanDistance(newPos, food))
            if dist < closestFoodOld:
                closestFoodOld = float(dist)
        
        # find which ghost is closest
        closestGhost = 1000000.0
        for ghost in newGhostStates:
            ghostDist = float(manhattanDistance(newPos, ghost.getPosition()))
            if ghostDist < closestGhost:
                closestGhost = float(ghostDist)
                
        # This score method greatly encourages pacman to stay away from ghosts 
        # while bringing him ever closer to food
        # A living pacman is a scoring pacman
        score = ((1/(closestFood)) + (closestGhost))
        
        # We want to encourage PacMan to live in a world with less food pellets, so we will add score for that
        # The value added is rather arbitrary,
        if (len(foodList) < len(currentGameState.getFood().asList())):
            score += 15.0
            
        # We want pacman to seek out food, even if it isn't right next to him
        if (closestFood < closestFoodOld):
            score += 30.0
                
        # if the ghost is too close, pacman should abandon prospects of food and prefer life
        # this idea here is to negate the previous addition and generally stay as safe as possible
        if (closestGhost < 2.0):
            score -=30.0
        
        return score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
            
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        # recursively calls value and finds the maximum
        def maxValue(gameState, depth):
            v = -9999999
            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                v = max(v, value(successor, 1, depth))
            return v
        # recursively calls value and finds the minimum
        def minValue(gameState, agentIndex, depth):
            v = 99999999
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                v = min(v, value(successor, (agentIndex+1), depth))
            return v
        # value runs through the agents and the desired depth to return the final utility of the state after each move
        def value(state, agentIndex, depth):
            # If we are to pacman, lower depth since we have taken a
            # whole turn
            if agentIndex == state.getNumAgents():
                agentIndex = 0
                depth -= 1
            # If the state is terminal
            if (state.isWin() or state.isLose()) or depth == 0:
                return self.evaluationFunction(state) 
            # If it is pacmans turn we maximize
            elif agentIndex == 0:
                return maxValue(state, depth)
            # If it isn't pacman's turn we minimize
            else:
                return minValue(state, agentIndex, depth)
            
        # Sometimes the best thing to do is nothing,
        # but hopefully always do something
        bestAction = 'Stop'
        # Max start arb small 
        maxScore = -10000000
        
        # We loop over pacman's possible actions 
        for action in gameState.getLegalActions(0):
            sucessor = gameState.generateSuccessor(0, action)
            # this call is recursive for depth and agents but 
            # will eventually return the final state utility
            score = value(sucessor, 1, self.depth)
            # if this score is the best we encountered,
            # then we record that action
            if score > maxScore:
                maxScore = score
                bestAction = action
            
        # finally, we return the best action that we found for pacman
        return bestAction
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"        
        # recursively calls value and finds the maximum
        def maxValue(gameState, alpha, beta, depth):
            v = -9999999.9
            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                v = max(v, value(successor, alpha, beta, 1, depth))
                # if this node should we pruned then we return now
                if v > beta:
                    return v
                # we update alpha
                alpha = max(alpha, v)
            return v
        # recursively calls value and finds the minimum
        def minValue(gameState, alpha, beta, agentIndex, depth):
            v = 99999999.9
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                v = min(v, value(successor, alpha, beta, (agentIndex+1), depth))
                # if this node should be pruned then we don't keep going
                if v < alpha:
                    return v
                # we update beta
                beta = min(beta, v)
            return v
        # value runs through the agents and the desired depth to return the final utility of the state after each move
        def value(state, alpha, beta, agentIndex, depth):
            # If we are to pacman, lower depth since we have taken a
            # whole turn
            if agentIndex == state.getNumAgents():
                agentIndex = 0
                depth -= 1
            # If the state is terminal
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            # If it is pacmans turn we maximize
            elif agentIndex == 0:
                return maxValue(state, alpha, beta, depth)
            # If it isn't pacman's turn we minimize
            else:
                return minValue(state, alpha, beta, agentIndex, depth)
            
        # Sometimes the best thing to do is nothing,
        # but hopefully always do something
        bestAction = 'Stop'
        # Max start arb small 
        maxScore = -10000000.0
        
        # Alpha and beta for minimax
        alpha = -9999999.9
        beta = 9999999.9
        # We loop over pacman's possible actions 
        for action in gameState.getLegalActions(0):
            sucessor = gameState.generateSuccessor(0, action)
            # this call is recursive for depth and agents but 
            # will eventually return the final state utility
            score = value(sucessor, alpha, beta, 1, self.depth)
            # if this score is the best we encountered,
            # then we record that action
            if score > maxScore:
                maxScore = score
                bestAction = action
            if score > beta:
                return bestAction
            alpha = max(alpha,score)
        # finally, we return the best action that we found for pacman
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # Calcs the prob of a given action
        def probability(gameState, successor, agentIndex):
            # find the number of possible moves
            possibleMoves = len(gameState.getLegalActions(agentIndex))
            # find the probabilty of any given move by dividing it by the number of possible moves
            prob = 1.0/possibleMoves
            return prob
        
        # recursively calls value and finds the maximum
        def maxValue(gameState, depth):
            v = -9999999
            for action in gameState.getLegalActions(0):
                successor = gameState.generateSuccessor(0, action)
                v = max(v, value(successor, 1, depth))
            return v
        # recursively calls value and finds the expected
        def expValue(gameState, agentIndex, depth):
            v = 0
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                # calc the probability then use it to calculate v
                p = probability(gameState, successor, agentIndex)
                v += p * value(successor, (agentIndex+1), depth)
            return v
        # value runs through the agents and the desired depth to return the final utility of the state after each move
        def value(state, agentIndex, depth):
            # If we are to pacman, lower depth since we have taken a
            # whole turn
            if agentIndex == state.getNumAgents():
                agentIndex = 0
                depth -= 1
            # If the state is terminal
            if (state.isWin() or state.isLose()) or depth == 0:
                return self.evaluationFunction(state) 
            # If it is pacmans turn we maximize
            elif agentIndex == 0:
                return maxValue(state, depth)
            # If it isn't pacman's turn we minimize
            else:
                return expValue(state, agentIndex, depth)
            
        # Sometimes the best thing to do is nothing,
        # but hopefully always do something
        bestAction = 'Stop'
        # Max start arb small 
        maxScore = -10000000
        
        # We loop over pacman's possible actions 
        for action in gameState.getLegalActions(0):
            sucessor = gameState.generateSuccessor(0, action)
            # this call is recursive for depth and agents but 
            # will eventually return the final state utility
            score = value(sucessor, 1, self.depth)
            # if this score is the best we encountered,
            # then we record that action
            if score > maxScore:
                maxScore = score
                bestAction = action
        # finally, we return the best action that we found for pacman
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***" 
    
    # Game stuff we need to use relative to Pacman's position
    from util import manhattanDistance                                          # Import Manhattan Distance because it's the best herustic
    food = currentGameState.getFood()                                           # Getting the Food booleans on the board
    foodList = food.asList()                                                    # Making Food booleans into coordinates
    pacmanPos = currentGameState.getPacmanPosition()                            # Get Pacman's coordinates
    powerCapsules = currentGameState.getCapsules()                              # Get Capsule's coordinates
    newGhostStates = currentGameState.getGhostStates()                          # Get Ghost coordinate
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]  # Get scare Timer
    score = scoreEvaluationFunction(currentGameState)                           # keeps track, we start with the original eval since it's close to good
    
    # This calculates the closest Food pellet to Pacman using Manhattan Distance
    closestFood = 99999999.9
    for pellet in foodList:
        pDist = manhattanDistance(pacmanPos, pellet)
        closestFood = min(closestFood, pDist)
        
    # This calculates the closest Ghost to Pacman using Manhattan Distance
    closestGhost = 99999999.9
    for ghost in newGhostStates:
        gDist = manhattanDistance(pacmanPos, ghost.getPosition())
        closestGhost = min(closestGhost, gDist)
        
    # This calculates the closest Capsule relative to Pacman's position using Manhattan Distance    
    closestCapsule = 99999999.9
    for cap in powerCapsules:
        cDist = manhattanDistance(pacmanPos, cap)
        closestCapsule = min(closestCapsule, cDist)
    
    # This uses the scare times and makes ghost more desirable to eat
    for time in newScaredTimes:
        if time > 0:
            closestGhost = (1.0/closestGhost)
            break
    
    # Ok. Here's where it gets real weird.
    # I choose the max between the closest Ghost and a distance of 4, so if the ghost is farther it won't consider it.
    # I multiply that by 1.5 to make it more scary when the ghost comes real close.
    # Now the weird part is that I substract all of this from the score, so that Pacman follows the ghost at a distance.
    # However, because of the 1.5 it makes backs off immediately once the Ghost moves towards Pacman's position.
    # Made the closest Food a fraction so the closer it is the more desirable it is.
    # Multiply it by 5 to increase its desirability.
    # In conclusion, I made our Pacman edgy.
    score -= max(closestGhost, 4.0) * 1.5
    score += 1/closestFood * 5 # Then we add to make food desirable, mult by 5 because food is really important
    
    # Return the score
    return score

# Abbreviation
better = betterEvaluationFunction