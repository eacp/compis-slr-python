from typing import Set, List, Dict
from dataclasses import dataclass

@dataclass
class Rule:
	left: str
	right: List[str]

	# An util method to get the righmost element of a symbol

	def right_of(self, symbol: str) -> str:
		# Find the index.
		# Complexity O(n)
		idx = self.right.index(symbol)

		# Avoid overflow
		if idx+1 == len(self.right):
			# This is the last one and there is nothing right

			return ""
		
		return self.right[idx+1]

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

	# The same
	follows: Dict[str, Set[str]]

	# Custom (null) start symbol that we'll set later
	start: str

	# This is a space to group the different rules that have the same
	# thing on the left side, in order to unify them
	groups: Dict[str, List[Rule]]

	# A cache for the function that looks up rules with a certain symbol 
	# on the right

	cache_symbols_right: Dict[str, List[Rule]]

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
		self.follows = {}

		self.groups = {} # Empty dict
		self.cache_symbols_right = {}

	
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

	
	def first_of(self, key: str) -> Set[str]:

		# Check if this is a non terminal
		if key in self.non_terminals:
			# We should go recursive
			if len(self.first[key]) != 0:
				return self.first[key]
			else:
				data = set()

				for r in self.groups[key]:
					# Recursive call
					data.update( self.first_of( r.right[0]) )
				
				return data
		
		else:
			# It is a terminal because it wasnt a non terminal
			data = set()

			data.add(key)

			return data

	def make_first(self):
		"""
		Computes the first set of the non terminal
		symbols
		"""


		# This is IMPORTANT. It is important something is there
		# EVEN IF empty. Otherwise weird errors happen, given the order
		# of the sets is not deterministic

		for nt in self.non_terminals:
			# Init the set as per the algorithm from india
			self.first[nt] = set()

		for nt in self.non_terminals:
			data = set()

			for rule in self.groups[nt]:
				if rule.right[0] != nt:
					# Use leftmost [0]

					leftmost = rule.right[0]

					data.update( self.first_of( leftmost )  )
			

			self.first[nt] = data
	

	# All things follow go here

	def rules_with_this_right(self, thing: str) -> List[Rule]:
		if thing in self.cache_symbols_right.keys():
			return self.cache_symbols_right[thing]

		# No cache

		ls = []

		for rule in self.rules:
			if thing in rule.right:
				ls.append(rule)
		

		# Save LS for later purposes, courtesy of
		# dynamic programming and memoization
		self.cache_symbols_right[thing] = ls

		return ls

	# Just like above

	def follows_of(self, key: str) -> Set[str]:
		"""
		Get the follows of a single element using recursion
		"""

		# Base case: We already have it yay
		if key in self.follows.keys():
			return self.follows[key]

		# Otherwise recursion

		f = set()

		for rule in self.groups[key]:
			# Base case: it has it
			right = rule.right_of(key)
			if right:
				# Call the follow recursion
				f.update( self.first_of(right)  )
			else:
				# Recursion
				f.update(self.follows_of(rule.left))
		
		return f



	def make_follows(self):
		for nt in self.non_terminals:
			self.follows[nt] = set() # empty
		

		dollar = { "$" }

		# Put the dollar as a follow of the start

		self.follows[self.start] = dollar

		for nt in self.non_terminals:
			data = set()

			# If empty
			if len(self.follows[nt]) == 0:
				data = data
			else:
				data = self.follows[nt]
			
			for rule in self.rules_with_this_right(nt):
				# Using cache
				right = rule.right_of(nt)

				# base case
				if len(right) != 0:
					# We have something
					data.update( self.first_of(right) )
				else:
					# recursion
					data.update( self.follows_of(rule.left) )
			
			self.follows[nt] = data
