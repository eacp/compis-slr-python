from grammar import Grammar, Rule, check_can_be_terminal
from typing import List, Set
from dataclasses import dataclass

import copy # For making clones

# A class that has a rule and some extra things

class AutomataRule(Rule):
	"""
	This class represents a rule but with added
	capabilities for detecting and moving the dot.

	Naturally, it inherits from the basic Rule class
	"""
	
	def index_of_dot(self) -> int:
		"""
		Inside a rule, finds the index of the dot
		"""

		if "." in self.right:
			return self.right.index(".")

		return -1

	def dot_is_last(self) -> bool:
		"""
		Inside a given rule, check if we are done.

		We are done if the dot is the last thing
		"""
		return self.right[-1] == "."

	def next_symbol(self) -> str:
		"""
		Returs the next inmediate symbol
		(the one immediatly after the dot)
		"""
		if self.dot_is_last():
			return ""
		
		return self.right[self.index_of_dot() + 1]
	
	def shift_period(self):
		"""
		Creates a copy of this Rule with the dot
		moved one position
		"""

		other = copy.deepcopy(self)

		if other.dot_is_last():
			return other

		# Get the index of the current dot
		idx = other.index_of_dot()

		# Insert the dot in a new place
		other.right.insert(idx + 2, ".") # Add two cuz we want the one after after (after the symbol after)

		return other
		

@dataclass(init=False)
class State:
	n: int = 0
	accepted: bool = False
	kernel: Set[AutomataRule]
	closure: Set[AutomataRule]

	def __init__(self) -> None:
		self.kernel = set()
		self.closure = set()

@dataclass
class GoTo:
	from_state: int
	to_state: int
	symbol: str
	goes_to_prev: bool


# Global is dirty but more or less works

count = -1

state = -1
states: List[State] = []
prods: List[AutomataRule]  = []
gotos: List[GoTo] = []
rem: List[GoTo] = []

def state_closure(state: State, g: Grammar):
	# Copy the kernel into the closure to begin
	closure: Set[AutomataRule] = state.kernel.copy()

	curr_size = len(closure)

	prev_size = 0

	# Iterate until the sizes are equal, according to youtube

	while curr_size != prev_size:
		# Copy the current size
		prev_size = curr_size

		# Uodate the curr size
		data: Set[AutomataRule] = set()

		for rule in closure:
			# Filter the ones that are have  dot before,
			# and check it is a non terminal

			has_next = not rule.dot_is_last()

			is_non_terminal = not check_can_be_terminal( rule.next_symbol() )

			# This is only for NT
			if has_next and is_non_terminal:
				next_sym = rule.next_symbol()

				right_of = g.groups[ next_sym ]

				for rule in right_of:
					clone = copy.copy(rule)

					data.add( AutomataRule(clone.left, clone.right) )
		

		# We have constructed all the automatonrules we needed
		closure.update( data )

		curr_size = len(closure)

	
	state.closure = closure



def make_closures_from_grammar(g: Grammar) -> List[State]:	
	# Here convert the existing rules into 
	# rules that have the dot in the front
	for rule in g.rules:

		# Create it with the dot in the front
		extended = AutomataRule(rule.left,  ["."]  + rule.right)

		prods.append(extended)

	# Create the initial state

	init_state = State()

	# Initialize the first kernel
	

	init_state.kernel = { prods[0] } 


	# This will alter the state
	state_closure(init_state, g)

	# Insert the state in the array
	states.append(init_state)

	print("Initial state with closure computed")

	return states






	
	

