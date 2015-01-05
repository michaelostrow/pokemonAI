import xlrd

# spreadsheet containing data about type weaknesses between pokemon types
# used to determine damage dealt which helps determine value of states
poke_sheet = xlrd.open_workbook('pokemon_data.xls').sheet_by_index(0)

# range over which cells in poke_sheet contain relevant data
type_cells = range(1,18)

# dictionary denoting which rows in the spreadsheet
# are occupied by which types
type_rows = {}
for i in type_cells:
    type_rows[str(poke_sheet.cell(0, i).value)] = i

# takes in two types and returns a dictionary
# representing how effective attacks of certain types
# will be against the given types
def type_effectiveness(t1, t2):
    val = {}
    for i in type_cells:
    	typeName = str(poke_sheet.cell(i, 0).value)
        val[typeName] = poke_sheet.cell(i, type_rows[t1]).value
    if t2:
    	for i in type_cells:
    		typeName = str(poke_sheet.cell(i, 0).value)
    		val[typeName] = poke_sheet.cell(i, type_rows[t2]).value * val[typeName]
    return val

# class representing a pokemon type (can be dual-typed)
class Type:
    def __init__(self, t1, t2=None):
        self.t1 = t1
        self.t2 = t2
        self.typeEffectiveness = type_effectiveness(t1, t2)

    # returns true if the given type is one of these two types
    # used for damage calculation of same-type-attack-bonus attacks
    def gets_stab(self, t):
    	return t == self.t1 or t == self.t2
        

# Class containing information about a pokemon
class Pokemon:
	def __init__(self, name, level, hp, atk, de, spa, spd, types=None, atks=None):
		self.name = name
		self.level = int(level)
		self.currenthp = float(hp)
		self.maxhp = float(hp)
		self.attack = float(atk)
		self.defense = float(de)
		self.specialAttack = float(spa)
		self.specialDefense = float(spd)
		self.types = types
		self.attacks = atks

		

# Class representing an attack that a pokemon may perform
class Attack:
	def __init__(self, name, types, base, kind):
		self.name = name
		self.types = types
		self.base = float(base)
		self.kind = kind


# takes an attack as argument, and applies damage
# to the pokemon
def take_damage(defender, attacker, attack):

	v1 = ((2 * attacker.level)+10)/250.0

	v2 = 0
	if attack.kind == 'physical':
		v2 = attacker.attack/defender.defense
	else:
		v2 = attacker.specialAttack/defender.specialDefense

	mod = defender.types.typeEffectiveness[attack.types]
	if attacker.types.gets_stab(attack.types):
		mod = mod * 1.5

	damage = (v1*v2*attack.base+2)*mod

	defender.currenthp = max(defender.currenthp - damage, 0)

# similar to take_damage, but instead returns the 
# damage dealt rather than performing any mutations
def calculate_damage(defender, attacker, attack):

	v1 = ((2 * attacker.level)+10)/250.0

	v2 = 0
	if attack.kind == 'physical':
		v2 = attacker.attack/defender.defense
	else:
		v2 = attacker.specialAttack/defender.specialDefense

	mod = defender.types.typeEffectiveness[attack.types]
	if attacker.types.gets_stab(attack.types):
		mod = mod * 1.5

	return (v1*v2*attack.base+2)*mod
