from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument
    is an object of GameState class. Following are a few of the helper methods that you
    can use to query a GameState object to gather information about the present state
    of Pac-Man, the ghosts and the maze.

    gameState.getLegalActions():
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action):
        Returns the successor state after the specified agent takes the action.
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.configuration.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    gameState.getScore():
        Returns the score corresponding to the current state of the game


    The GameState class is defined in pacman.py and you might want to look into that for
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best


    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()


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

######################################################################################


class MinimaxAgent(MultiAgentSearchAgent):

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following:
      pacman won, pacman lost or there are no legal moves.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game

      gameState.getScore():
        Returns the score corresponding to the current state of the game

      gameState.isWin():
        Returns True if it's a winning state

      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue

    """

    
    # returns value of state, optimal action
    currentDepth = self.depth
    agentIndex = self.index
    # returns (minimax value of state, optimal action)
    def recurse(gameState, currentDepth, agentIndex):
        if gameState.isWin() or gameState.isLose() or len(gameState.getLegalActions(agentIndex)) == 0:
            return (gameState.getScore(), None)

        if currentDepth == 0:
            return (self.evaluationFunction(gameState), None)

        #Pacman's Turn
        if agentIndex == 0:
            legalActions = gameState.getLegalActions(agentIndex)
            #legalActions.remove(Directions.STOP)
            maxChoices = []
            for action in legalActions:
                newAgentIndex = agentIndex + 1
                maxChoices.append((recurse(gameState.generateSuccessor(agentIndex,action),currentDepth,newAgentIndex)[0],action))
            #return max(maxChoices)
            currentMax = max(maxChoices)
            tiebreakList = [x for x in maxChoices if x[0] == currentMax[0]]
            return random.choice(tiebreakList)

        #Ghost's Turn
        if agentIndex != 0:
            legalActions = gameState.getLegalActions(agentIndex)
            #legalActions.remove(Directions.STOP)
            minChoices = []
            for action in legalActions:
                if agentIndex == gameState.getNumAgents() - 1:
                    newAgentIndex = 0 #go to Pacman turn
                    newDepth = currentDepth - 1
                    minChoices.append((recurse(gameState.generateSuccessor(agentIndex,action),newDepth,newAgentIndex)[0],action))
                else:
                    newAgentIndex = agentIndex + 1
                    minChoices.append((recurse(gameState.generateSuccessor(agentIndex,action),currentDepth,newAgentIndex)[0],action))
            currentMin = min(minChoices)
            tiebreakList = [x for x in minChoices if x[0] == currentMin[0]]
            return random.choice(tiebreakList)

    value, action = recurse(gameState,currentDepth,self.index)
 
    return action



######################################################################################


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    currentDepth = self.depth
    agentIndex = self.index
    # returns (minimax value of state, optimal action, alpha, beta)
    def recurse(gameState, currentDepth, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose() or len(gameState.getLegalActions(agentIndex)) == 0:
            return (gameState.getScore(), None)

        if currentDepth == 0:
            return (self.evaluationFunction(gameState), None)

        #Pacman's Turn
        if agentIndex == 0:
            legalActions = gameState.getLegalActions(agentIndex)
            value = (-(float("inf")),None)
            maxChoices = []
            for action in legalActions:
                newAgentIndex = agentIndex + 1
                valueSucc = (recurse(gameState.generateSuccessor(agentIndex,action),currentDepth,newAgentIndex,value,beta)[0],action)
                if value[0] == valueSucc[0]:
                    value = random.choice([value,valueSucc])
                else:
                    value =  max(value,valueSucc)
                if value[0] >= beta:
                    return value
                alpha = max(alpha,value[0])
            return value

        #Ghost's Turn
        if agentIndex != 0:
            legalActions = gameState.getLegalActions(agentIndex)
            value = (float("inf"),None)
            minChoices = []
            for action in legalActions:
                bestaction = action
                if agentIndex == gameState.getNumAgents() - 1:
                    newAgentIndex = 0 #go to Pacman turn
                    newDepth = currentDepth - 1
                    valueSucc = (recurse(gameState.generateSuccessor(agentIndex,action),newDepth,newAgentIndex,alpha,value)[0],action)
                    if value[0] == valueSucc[0]:
                        value = random.choice([value,valueSucc])
                    else:
                        value =  min(value,valueSucc)
                    if value[0] <= alpha:
                        return value
                    beta = min(beta,value[0])
                else:
                    newAgentIndex = agentIndex + 1
                    valueSucc = (recurse(gameState.generateSuccessor(agentIndex,action),currentDepth,newAgentIndex,alpha,value)[0],action)
                    if value[0] == valueSucc[0]:
                        value = random.choice([value,valueSucc])
                    else:
                        value =  min(value,valueSucc)
                    if value[0] <= alpha:
                        return value
                    beta = min(beta,value[0])
            return value

    alpha = -(float("inf"))
    beta = float("inf")
    value, action = recurse(gameState,currentDepth,self.index,alpha,beta)

    return action

######################################################################################

class ExpectimaxAgent(MultiAgentSearchAgent):  

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    currentDepth = self.depth
    agentIndex = self.index
    # returns (minimax value of state, optimal action)
    def recurse(gameState, currentDepth, agentIndex):
        if gameState.isWin() or gameState.isLose() or len(gameState.getLegalActions(agentIndex)) == 0:
            return (gameState.getScore(), None)

        if currentDepth == 0:
            return (self.evaluationFunction(gameState), None)

        #Pacman's Turn
        if agentIndex == 0:
            legalActions = gameState.getLegalActions(agentIndex)
            maxChoices = []
            for action in legalActions:
                newAgentIndex = agentIndex + 1
                maxChoices.append((recurse(gameState.generateSuccessor(agentIndex,action),currentDepth,newAgentIndex)[0],action))
            #return max(maxChoices)
            currentMax = max(maxChoices)
            tiebreakList = [x for x in maxChoices if x[0] == currentMax[0]]
            return random.choice(tiebreakList)

        #Ghost's Turn
        if agentIndex != 0:
            legalActions = gameState.getLegalActions(agentIndex)
            minChoices = []
            for action in legalActions:
                if agentIndex == gameState.getNumAgents() - 1:
                    newAgentIndex = 0 #go to Pacman turn
                    newDepth = currentDepth - 1
                    probAction = 1/len(legalActions)
                    minChoices.append((probAction*(recurse(gameState.generateSuccessor(agentIndex,action),newDepth,newAgentIndex)[0]),action))
                else:
                    newAgentIndex = agentIndex + 1
                    probAction = 1/len(legalActions)
                    minChoices.append((probAction*(recurse(gameState.generateSuccessor(agentIndex,action),currentDepth,newAgentIndex)[0]),action))
            sumValue = 0
            actionList = []
            for value, action in minChoices:
                sumValue += value
                actionList.append(action)
            return sumValue, actionList[random.randint(0,len(actionList)-1)]

    value, action = recurse(gameState,currentDepth,self.index)
    #print value
    return action
    # END_YOUR_CODE

######################################################################################

def betterEvaluationFunction(currentGameState):
  """

  """

  raise Exception("Not implemented yet")

# Abbreviation
better = betterEvaluationFunction
