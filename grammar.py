from typing import Set, List, Dict
from dataclasses import dataclass

@dataclass
class Rule:
	"""
	Class that representsa  single rule in
	a line.

	Example:

	S -> A + int

	Left: S
	Right: [A, +, int]

	"""


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
	"""
	Utility function to read a single
	rule from a string in one line
	"""

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
	"""
	Class to represent a grammar
	aquired from a file.

	It contains fields to store the first,
	follow and methods to generate them
	"""

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
		"""
		For a given key, return the first set
		of such key. It does so recursively until
		it reaches the base case, which is a 
		terminal symbol.

		The first of a termoninal symbol is that terminal symbol.

		The first of a non terminal symbol is
		the first of the leftmost token on the
		right set
		"""

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
		"""
		Returns a list of rules that have
		have a given symbol on the right.

		Brute force search.
		"""

		# Remove the cache in the meantime if it is not working
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

	def follow_of(self, key: str) -> Set[str]:
		"""
		Returns a follow if it already exists,
		otherwise it computes it
		"""
		
		# If it already has stuff, just return it
		if len(self.follows[key]) != 0:
			return self.follows[key]

		# Put stuff otherwise
		follow = set()

		on_right = self.rules_with_this_right(key)

		for rule in on_right:

			right = rule.right_of(key)

			if len(right) == 0:
				# Recursive follows because empty
				follow.update( rule.left )
			else:
				follow.update( self.first_of(right) )


		return follow
	
	def make_follows(self):
		"""
		Function to compute the follows, after
		of course computing the firsts
		"""

		# Add all the non terminals into follows,
		# properly intialized

		for nt in self.non_terminals:
			self.follows[nt] = set()
		
		# Add the initial data set (dollar) to the
		# section of the first symbol

		self.follows[self.start] = { "$" }

		# Iterate thru all the non terminals
		for nt in self.non_terminals:
			current_follows = self.follows[nt]

			with_symbol_on_right = self.rules_with_this_right(nt)

			for rule in with_symbol_on_right:
				right = rule.right_of(nt)

				if len(right) == 0:

					# Update with a recursive follow
					current_follows.update( 
						self.follow_of(rule.left) 
					)
				else:
					# Update with a first, as defined by the
					# algorithm
					current_follows.update(
						self.first_of(right) 
					)
			

			self.follows[nt] = current_follows