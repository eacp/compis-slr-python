from os import stat
from grammar import Grammar, Rule, check_can_be_terminal
from typing import List, Set
from dataclasses import dataclass

from queue import Queue

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

		other.right.remove(".") # Remove first occurence of ., essentially removing it


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

	def all_that_have_dot_before(self, s: str) -> Set[AutomataRule]:
		"""
		This funct iterates thru all the rules in this state
		to see in which ones the next element is equal to a given string.

		This is equivalent of doing so visually in a notebook
		"""
		the_set: Set[AutomataRule] = set( 
			filter(
				# Disc funtion: all that have s in the nexts
				lambda r: (r.next_symbol() == s ),
				# Look in the closure
				self.closure 
				) 
			)
		
		print(the_set)
		
		# Return a copy to avoid making accidental modifications
		return the_set.copy()
		




@dataclass(init=False)
class GoTo:
	"""
	This class represents a Go To
	"""
	from_state: int
	to_state: int
	symbol: str = ""
	goes_to_prev: bool = False

	def __init__(self, fs: int, sym: str) -> None:
		"""
		Short constructor: Receives the symbol to go to and
		the from
		"""
		self.from_state = fs
		self.symbol = sym


# Global is dirty but more or less works

# From the algo

states: List[State] = []
prods: List[AutomataRule]  = []
gotos: List[GoTo] = []
rem: "Queue[GoTo]" = Queue()

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

					# Add the . in case it is not here
					if "." not in clone.right:
						clone.right = ["."] + clone.right

					data.add( AutomataRule(clone.left, clone.right) )
		

		# We have constructed all the automatonrules we needed
		closure.update( data )

		curr_size = len(closure)

	
	state.closure = closure



def make_closures_from_grammar(gr: Grammar) -> List[State]:
	for rule in gr.rules:
		# Create an augmented version of the rule and insert it
		augmented = AutomataRule(rule.left, ["."] + rule.right.copy())
		prods.append(augmented)

	print("Prods with dot", prods)

	# A new state to be used for later purposess
	initial_s = State()

	# Create the first kernel

	kernel0 = { prods[0] }

	initial_s.kernel = kernel0

	state_closure(initial_s, gr)

	# Save the computed state
	states.append(initial_s)


	for rule in states[0].closure:
		if not rule.dot_is_last():
			# Make a goto from scratch
			got = GoTo(0, rule.next_symbol() )
			gotos.append(got)

			rem.put(got)

			states[0].accepted = False
		else:
			# Only accept
			states[0].accepted = True


	# SLR Construction---------------------

	while not rem.empty():
		g = rem.get()

		
		new_state = State()

		s = states[g.from_state]

		# Get all that have a dot before a symbol
		k = s.all_that_have_dot_before(g.symbol)

		k2: Set[AutomataRule] = set()

		for rule in k:
			k2.add( rule.shift_period() )

		# Get all kernels
		kernels = [xs.kernel for xs in states]


		# Check if at least one is the same, and save its index
		pos = -1

		for key, v in enumerate(kernels):
			# Check if the current one (v) matches what we are looking for
			if v == k2:
				pos = key
				break
		

		if pos != -1:
			g.to_state = pos
			g.goes_to_prev = True


			#update
			index = gotos.index(g)

			gotos[index].to_state = pos
		else:
			new_state.kernel = k2

			state_closure(new_state, gr)

			states.append(new_state)

			# Index of the last one added
			g.to_state = len(states) - 1

			index = gotos.index(g)

			gotos[index].to_state = len(states) - 1

			N = len(states) - 1

			for rule in states[N].closure:
				if not rule.dot_is_last():

					# Add them to the list of gotos
					go = GoTo(N, rule.next_symbol() )

					gotos.append(go)

					rem.put(go)
				else:
					# Just accept
					states[N].accepted = True






	return states
