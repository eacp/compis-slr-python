"""
SLR in Python

A01702948

This is the entrypoint of the program

"""

import grammar
import sys # This has the arguments
import export_html # Module to help with rendering. This is NOT used for computation

# Recursivity-ish queue
from queue import SimpleQueue

# Utility functions for this file

def check_can_be_terminal(candidate: str) -> bool:
	lower = candidate.lower()# Utility functions for this file

def check_can_be_terminal(candidate: str) -> bool:
	lower = candidate.lower()

	# If it was ALL lower, 
	return candidate == lower

	# You CANNOT use islower because it has conflicts with pure non letter text,
	# such as +

	# If it was ALL lower, 
	return candidate == lower

	# You CANNOT use islower because it has conflicts with pure non letter text,
	# such as +
prod = []

def append_dot(a):
	"""
	Appends a dot to the beguining so it is in the read position
	"""
	# Just replace the arrow
	jj = a.replace("->", "->.")
	return jj

def closure(a):
	# Temporal list
    temp = [a]

	# Keep iterating the list
    for it in temp:

		# Next position after the dot
        jj = it[it.index(".") + 1]

		# Check the bounds
        if jj != len(it) - 1:
            for k in prod:

				# COnditionally add thigs to the queue
                if k[0][0] == jj and (append_dot(k)) not in temp:
                    temp.append(append_dot(k))
        else:
            for k in prod:
				# Just make the append option
                if k[0][0] == jj and it not in temp:
                    temp.append(it)

    return temp


if __name__ == "__main__":

	# Get the command line arguments
	if len(sys.argv) < 2:
		exit("Please specify the path of the grammar file")

	filepath = sys.argv[1]

	print("SLR Generator")

	# Make an empty grammar
	gr = grammar.Grammar()

	# Open the file and iterate thru the lines
	with open(filepath, mode='r') as grammar_file:
		for line in grammar_file:
			# Make the rule from the line
			r = grammar.rule_from_line(line)

			gr.rules.append(r)

	# Print the grammar to see if we are right

	

	# Compute the start symbol
	gr.start = gr.rules[0].left

	print("Grammar so far:", gr)

	# Iterate thur the rules (prods)
	# Compute the set of non terminals
	for rule in gr.rules:
		# Add the 'key' of this non terminal
		gr.non_terminals.add(rule.left)

		# Check every token and add it to the set of terminals
		for identifier in rule.right:
			if check_can_be_terminal(identifier):
				gr.terminals.add(identifier)

	# Check the grammar so far
	print("Grammar so far:",gr)
	
	# finish computing prime rule

	# Now compute the first

	# But before that, compute the cache of the full joined rules

	gr.make_group_cache()

	gr.make_first()

	print("Grammar so far WITH FIRST:",gr)

	print("FIRSTs generated, computing follows")

	gr.make_follows()

	print("Grammar with FOLLOWS:", gr)

	print("Computed follows")

	print("Extending with PRIME")

	# I used to think this was before the follow and first


	# Create prime production

	prime_left = gr.start + "'"

	prime_right = [ gr.start ] # a rule with only one symbol: the start


	prime_rule = grammar.Rule(prime_left, prime_right)

	# Add the prime rule to THE begining

	print("Computed prime extension")

	print(gr.rules)

	print("FIRST:", gr.first)

	print("FOLLOWS:", gr.follows)

	# Make the first & follow export

	gr.rules.insert(0, prime_rule)

	export_html.render_first_follow(gr)

	exit(0)
	
	# I had a hard time doing this
	# Start a queue for the closures
	q = SimpleQueue()

	q.put(gr.rules[0])

	cs = []

	# We will use a dictionary, but given the class
	# rule is not hashable, we will use the string instead

	state_numbers = {}
	dfa_prod = {}

	# The counter that gets assigned to each string representation
	i = 0

	# Iterate while not empty
	while not q.empty():
		jk = q.get()

		ker = jk

		cs.append(jk)

		# Increase the couunt
		state_numbers[str(jk)] = i
		i += 1