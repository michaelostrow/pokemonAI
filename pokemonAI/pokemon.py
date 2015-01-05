from pokemon_classes import Type, Pokemon, Attack, calculate_damage
from poke_gamestate import GameState
import minimax_poke_agent
import sys

# given a text file, parses it and generates
# an initial gamestate
def generate_state(fileName):
	f = open(fileName)

	team1 = generate_team_loop(f)
	team2 = generate_team_loop(f)

	return GameState(team1, team2)

# subroutine for team generation function
def generate_team_loop(openFile):
	team = []

	# ignore first two lines, used only to show team
	openFile.readline()
	openFile.readline()

	for i in range(6):
		attacks = []

		attributes = openFile.readline().split()
		poke = Pokemon(*attributes)

		types = openFile.readline().split()
		poke.types = Type(*types)

		for x in range(4):
			atk = openFile.readline().split()
			attacks.append(Attack(*atk))

		poke.attacks = attacks

		team.append(poke)

		openFile.readline()

	return team

# function that is given an initial gamestate
# and then uses minimax search to run a game,
# displaying actions taken along the way
def run_game(gamestate):
	agent = minimax_poke_agent.MinimaxPokeAgent()
	attacker = None
	defender = None
	player = None
	form_str = '%s attacks with %s for %i damage.'

	while True:

		attacked = False

		if gamestate.is_terminal_state():
			winner = gamestate.get_winner()
			print 'Game over: ' + winner + ' wins!'
			return

		action = agent.alpha_beta_search(gamestate)

		# uncomment the line below to see the nodes expanded to 
		# determine which action to take
		#print agent.NODES_EXPANDED
		agent.NODES_EXPANDED = 0

		if gamestate.turn == 1:
			player = 'Player 1'
			attacker = gamestate.team1
			defender = gamestate.team2
		if gamestate.turn == 2:
			player = 'Player 2'
			attacker = gamestate.team2
			defender = gamestate.team1

		for a in attacker[0].attacks:
			if a.name == action:
				attacked = True
				print form_str % (player, action, calculate_damage(defender[0], attacker[0], a))

		if not attacked:
			print player + ' switches out to ' + action + '.'

		gamestate = gamestate.get_next_state(action)


# main routine for instantiating and then running a game
if sys.argv[1] == 'basic':
	run_game(generate_state('basic.txt'))
if sys.argv[1] == 'intermediate':
	run_game(generate_state('intermediate.txt'))
if sys.argv[1] == 'advanced':
	run_game(generate_state('advanced.txt'))


