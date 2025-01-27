import random
import math


BOT_NAME =  "NeverFolds"


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
  
    rseed = 1  # change this to a value if you want consistent random choices

    def __init__(self):
        if self.rseed is None:
            self.rstate = None
        else:
            random.seed(self.rseed)
            self.rstate = random.getstate()

    def get_move(self, state):
        if self.rstate is not None:
            random.setstate(self.rstate)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move.  Very slow and not always smart."""

    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Gets called by get_move() to determine the value of each successor state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        #
        # Fill this in!
        #
        # get the max possible value for the state
        v = self.maxVal(state)
        return v
    
    def maxVal(self, state):
        """
        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact max utility value of the state
        """
        #
        # Fill this in!
        #
        # return utility if terminal state
        if state.is_full():
            return state.utility()
        if not state.is_full():                
            v = -math.inf
            # check all successor states
            for succ in state.successors():
                # update max value based on best value of children
                v = max(v, self.minVal(succ[1]))
            return v

    def minVal(self, state):
        """
        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact min utility value of the state
        """
        #
        # Fill this in!
        #
        # return utility if terminal state
        if state.is_full():
            return state.utility()
        if not state.is_full():                
            v = math.inf
            # check all successor states
            for succ in state.successors():
                # update min value based on best value of children
                v = min(v, self.maxVal(succ[1]))
            return v



class MinimaxLookaheadAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move.
 
    Hint: Consider what you did for MinimaxAgent. What do you need to change to get what you want? 
    """

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        Gets called by get_move() to determine the value of successor states.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation(). 

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the (possibly estimated) minimax utility value of the state
        """
        #
        # Fill this in!
        #
        depth = self.depth_limit
        v = self.maxVal(state, depth)
        return v  # Change this line!
    
    def maxVal(self, state, depth):
        """
        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact max utility value of the state
        """
        #
        # Fill this in!
        #
        # return utility if terminal state or max depth 
        if state.is_full() or depth == 0:
            return state.utility()
        if not state.is_full():                
            v = -math.inf
            # check all successor states
            for succ in state.successors():
                # update max value based on best value of children
                v = max(v, self.minVal(succ[1], depth - 1))
            return v

    def minVal(self, state, depth):
        """
        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact min utility value of the state
        """
        #
        # Fill this in!
        #
        # return utility if terminal state or max depth
        if state.is_full() or depth == 0:
            return state.utility()
        if not state.is_full():                
            v = math.inf
            # check all successor states
            for succ in state.successors():
                # update min value based on best value of children
                v = min(v, self.maxVal(succ[1], depth - 1))
            return v

    def minimax_depth(self, state, depth):
        """Determine the depth of the given state.

        This is just a helper method for minimax(). Feel free to use it or not. 

        Args:
            state: a connect383.GameState object representing the current board
            depth: an integer representing the depth of the current node

        Returns: 
        """
        pass

    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        Gets called by minimax() once the depth limit has been reached.  
        N.B.: This method must run in "constant" time for all states!

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heuristic estimate of the utility value of the state
        """

        #
        # Fill this in!
        #

        

        """
        maybe based on how many streaks there are?
        or the streaks that the opponent can make if they play the square 
        """
        # Note: This cannot be "return state.utility() + c", where c is a constant. 
        print("current utility: ", state.utility() + 2)
        return state.utility() + 2  # Change this line!


class AltMinimaxLookaheadAgent(MinimaxAgent):
    """Alternative heursitic agent used for testing."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Gets called by get_move() to determine the value of each successor state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        #
        # Fill this in!
        #
        v = self.maxVal(state)
        return v


class MinimaxPruneAgent(MinimaxAgent):
    """Computer agent that uses minimax with alpha-beta pruning to select the best move.
    
    Hint: Consider what you did for MinimaxAgent.  What do you need to change to prune a
    branch of the state space? 
    """
    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent does not have a depth limit.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to column 1 (we're trading optimality for gradeability here).

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        #
        # Fill this in!
        #
        """
        call minimax with a starting alpha and beta value of -inf, inf
        every time maxVal is called, set beta to the alpha (max) value of minVal
        every time minVal is called, set alpha to the beta (min) value of maxVal
        """ 
        alpha = math.inf
        beta = -math.inf
        v = self.maxVal(state, alpha, beta)
        return v  # Change this line!

    def maxVal(self, state, alpha, beta):
        """
        Args:
            state: a connect383.GameState object representing the current board
            alpha: upper bound on the minimax value of state
            beta: lower bound on the minimax value of state

        Returns: the exact max utility value of the state

        if maxVal
            if alpha (max) of minVal of child <= beta (min) of current (parent) (current.beta)
                prune that branch
            if beta (min) of minVal(child) > alpha (max) of current (parent) (current.alpha)
                update upper limit of parent
        """
        #
        # Fill this in!
        #
        # if terminal state, return it's utility
        if state.is_full():
            return state.utility()
        if not state.is_full():                
            v = -math.inf
            # check all successor states
            for succ in state.successors():
                # update max value if any child node has a higher value 
                v = max(v, self.minVal(succ[1], alpha, beta))
                # return value if child node's value is better than the current max
                if v >= alpha:
                    return v
                # update the min
                beta = max(beta, v)
            return v

    def minVal(self, state, alpha, beta):
        """
        Args:
            state: a connect383.GameState object representing the current board
            alpha: upper bound on the minimax value of state
            beta: lower bound on the minimax value of state

        Returns: the exact min utility value of the state

        if minVal
            if beta (min) of maxVal(child) >= alpha (max) of current (parent) (current.alpha)
                prune that branch
            if alpha (max) of maxVal(child) < beta (min) of current (parent) (current.beta)
                update lower limit of parent
        """
        #
        # Fill this in!
        #
        # if terminal state, return it's utility
        if state.is_full():
            return state.utility()
        if not state.is_full():                
            v = math.inf
            # check all successor states
            for succ in state.successors():
                # update min value if any child node has a lower value
                v = min(v, self.maxVal(succ[1], alpha, beta))
                # return value if child node's value is smaller than the current min
                if v <= beta:
                    return v
                # update the max
                alpha = min(alpha, v)
            return v



    def alphabeta(self, state, alpha, beta):
        """This is just a helper method for minimax(). Feel free to use it or not.

            Returns alpha and beta value of state as a tuple, with alpha first, beta second

            use this to pass the updated alpha and beta values for a state
                basically save the [beta, alpha] pair as an instance variable for the state
            from children, if the bounds of children are better than that of the parent
                update this 
            implementation
                state.alpha = wtv
                state.beta  = wtv
        """
        pass


def get_agent(tag):
    if tag == 'random':
        return RandomAgent()
    elif tag == 'human':
        return HumanAgent()
    elif tag == 'mini':
        return MinimaxAgent()
    elif tag == 'prune':
        return MinimaxPruneAgent()
    elif tag.startswith('look'):
        depth = int(tag[4:])
        return MinimaxLookaheadAgent(depth)
    elif tag.startswith('alt'):
        depth = int(tag[3:])
        return AltMinimaxLookaheadAgent(depth)
    else:
        raise ValueError("bad agent tag: '{}'".format(tag))       
