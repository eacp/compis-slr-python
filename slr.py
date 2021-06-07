"""
SLR in Python

A01702948

This is the entrypoint of the program

"""

import grammar
import sys # This has the arguments

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


	# Create the Prime nonterminal (S' or Goal' in most cases)
	primeNonTerminal = gr.start + "'"

	# The prime goes directly to the first one, so we create a rule that
	# serves ONLY as the pointer, per the specification
	primeRule = grammar.Rule(primeNonTerminal, [gr.start])

	# Add the prime rules as non terminal

	gr.non_terminals.add(primeNonTerminal)

	print(primeRule)

	# Put the prime rule at the begining

	gr.rules.insert(0, primeRule)

	

	# finish computing prime rule

	# Now compute the first

	# But before that, compute the cache of the full joined rules

	gr.make_group_cache()

	print("Grammar so far WITH PRIME' RULE:",gr)

	



