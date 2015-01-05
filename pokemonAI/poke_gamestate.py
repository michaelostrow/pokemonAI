import pokemon_classes
import copy

# Class representing the current state of a pokemon game
class GameState(object):
	def __init__(self, team1, team2):
		self.team1 = team1
		self.team2 = team2
		self.turn = 1

	# Function which generates a list of actions 
	# available in the current gamestate
	def get_legal_actions(self):
		actions = []
		team = None
		if self.turn == 1:
			team = self.team1
		if self.turn == 2:
			team = self.team2

		if team[0].currenthp > 0:
			for a in team[0].attacks:
				actions.append(a.name)

		for i in range(1,len(team)):
			if team[i].currenthp > 0:
				actions.append(team[i].name)

		return actions

	# Function which takes an action and returns the
	# state that results from taking that action
	def get_next_state(self, action):
		newstate = copy.deepcopy(self)

		if self.turn == 1:
			newstate.turn = 2

			for a in newstate.team1[0].attacks:
				if action == a.name:
					pokemon_classes.take_damage(newstate.team2[0], newstate.team1[0], a)

			for i in range(1, len(newstate.team1)):
				if newstate.team1[i].name == action:
					newstate.team1[0], newstate.team1[i] = newstate.team1[i], newstate.team1[0]

		if self.turn == 2:
			newstate.turn = 1

			for a in newstate.team2[0].attacks:
				if action == a.name:
					pokemon_classes.take_damage(newstate.team1[0], newstate.team2[0], a)

			for i in range(1, len(newstate.team2)):
				if newstate.team2[i].name == action:
					newstate.team2[0], newstate.team2[i] = newstate.team2[i], newstate.team2[0]

		return newstate

	# Function which calculates the value of a gamestate
	#
	# Currently calculates using the % of HP the opponent 
	# has remaining on their team, with bonus value given
	# for the opponent having 0 HP pokemon and for having
	# an advantageous type matchup currently
	def get_state_value(self):

		currenthp = 0
		totalhp = 0
		for p in self.team1:
			currenthp += p.currenthp
			totalhp += p.maxhp

		percenthpp1 = currenthp/totalhp

		currenthp = 0
		totalhp = 0
		for p in self.team2:
			currenthp += p.currenthp
			totalhp += p.maxhp

		percenthpp2 = currenthp/totalhp

		matchupScore = 10

		# change matchup score depending on types of both defender
		# and attacker, as some types may be effective against themselves
		te = self.team2[0].types.typeEffectiveness
		matchupScore *= te[self.team1[0].types.t1]
		if self.team1[0].types.t2:
			matchupScore *= te[self.team1[0].types.t2]

		te = self.team1[0].types.typeEffectiveness
		x = te[self.team2[0].types.t1]
		if x == 0:
			matchupScore /= .15
		else:
			matchupScore /= x
		if self.team2[0].types.t2:
			x = te[self.team2[0].types.t1]
			if x == 0:
				matchupScore /= .15
			else:
				matchupScore /= x

		if percenthpp2 == 0:
			percenthpp2 = .0001

		return (200*(percenthpp1/percenthpp2))+matchupScore


	# function for determining whether or not this gamestate
	# is a terminal state. A terminal state here is one where
	# one of the two teams has 0 total HP remaining
	def is_terminal_state(self):
		totalhp = 0

		for p in self.team1:
			totalhp += p.currenthp

		if totalhp == 0:
			return True

		totalhp = 0

		for p in self.team2:
			totalhp += p.currenthp

		if totalhp == 0:
			return True

		return False

	# this function is called when the game ends, returns
	# a string showing which player won the game
	def get_winner(self):
		totalhp = 0

		for x in self.team1:
			totalhp += x.currenthp

		if totalhp == 0:
			return 'player 2'
		else:
			return 'player 1'
