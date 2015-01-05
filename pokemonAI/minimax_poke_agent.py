import sys
import poke_gamestate

# default value for number of iterations of minimax
# search to perform
DEFAULT_MAX_DEPTH = 5

# class used for performing minimax search (w/ alpha
# beta pruning) given a pokemon gamestate
class MinimaxPokeAgent:

	# used to gather data for my project report
	NODES_EXPANDED = 0

	# given a game state, starts an alpha-beta search
	# to determine the correct action to take
	def alpha_beta_search(self, state, maxdepth=DEFAULT_MAX_DEPTH):

		action_vals = []

		if state.turn == 1:

			for a in state.get_legal_actions():
				self.NODES_EXPANDED += 1
				val = self.min_val_search(state.get_next_state(a), -sys.maxint-1, sys.maxint, maxdepth-1)
				action_vals.append((val, a))

			return max(action_vals)[1]

		else:

			for a in state.get_legal_actions():
				self.NODES_EXPANDED += 1
				val = self.max_val_search(state.get_next_state(a), -sys.maxint-1, sys.maxint, maxdepth-1)
				action_vals.append((val, a))

			return min(action_vals)[1]

	# the maximizer component of this minimax search agent
	def max_val_search(self, state, alpha, beta, remainingdepth):

		if state.is_terminal_state() or remainingdepth == 0:
			return state.get_state_value()

		val = -sys.maxint-1

		for a in state.get_legal_actions():
			self.NODES_EXPANDED += 1
			val = max(val, self.min_val_search(state.get_next_state(a), alpha, beta, remainingdepth-1))
			if val >= beta:
				return val
			alpha = max(alpha, val)

		return val

	# the minimizer component of this minimax search agent
	def min_val_search(self, state, alpha, beta, remainingdepth):

		if state.is_terminal_state() or remainingdepth == 0:
			return state.get_state_value()

		val = sys.maxint

		for a in state.get_legal_actions():
			self.NODES_EXPANDED += 1
			val = min(val, self.max_val_search(state.get_next_state(a), alpha, beta, remainingdepth-1))
			if val <= alpha:
				return val
			beta = min(beta, val)

		return val


