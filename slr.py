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

from closure import make_closures_from_grammar


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
			if grammar.check_can_be_terminal(identifier):
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

	# Make the closure

	states = make_closures_from_grammar(gr)

	print(states)

	 # Export them

	export_html.render_states(states)