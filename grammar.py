from typing import Set, List, Dict
from dataclasses import dataclass

@dataclass
class Rule:
	left: str
	right: List[str]

# Utility function
def rule_from_line(line: str) -> Rule:

	# Split the line based on the 'spaces' operator

	elements = line.split()

	# Ok, so the left part should be the 0 element, 
	# the arrow should be the 1 element and the rest
	# should be on the right

	left = elements[0]

	right = elements[2:]

	return Rule(left, right)

@dataclass()
class Grammar:

	# The list of rules. The rule class has been defined above
	rules: List[Rule]


	# The sets of terminal(literals) and non terminal(variables) 
	terminals: Set[str]
	non_terminals: Set[str]

	# I will put the first and follows here, one for each non terminal
	first: Dict[str, Set[str]]

	# Custom (null) start symbol that we'll set later
	start: str

	# This is a space to group the different rules that have the same
	# thing on the left side, in order to unify them
	groups: Dict[str, List[Rule]]

	def __init__(self):
		"""
		Constructor for this more complex class

		We need this custom cons to start the class with empty params

		We still use type hints so I dont die
		"""
		self.rules = []
		self.non_terminals = set() # empty set
		self.terminals = set()
		self.first = {} # Empty dict to be filled later

		self.groups = {} # Empty dict

	
	def make_group_cache(self):
		"""
		A method to UNIFY the different rules that share the same non terminal
		on the left

		This must be called once ALL the non terminals are identified
		"""
		for nt in self.non_terminals:
			# Init the set
			self.groups[nt] = []

		# Now iterate over every rule and add a copy to its corresponiding set

		for r in self.rules:
			# Use the left side as key
			self.groups[r.left].append(r)

	

		
