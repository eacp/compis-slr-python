from grammar import Grammar
from jinja2 import Template
from typing import List
from closure import State

# FF means first & follow

with open("templates/first_follow.html", 'r') as ff:
	# Read the entire file into the ff_template
	ff_template: Template = Template(ff.read())

with open("templates/states.html", 'r') as s:
	states_template: Template = Template( s.read() )

g = Grammar()

def render_first_follow(grammar: Grammar, filename="first-follow.out.html"):
	# Render to the file
	ff_template.stream(grammar=grammar).dump(filename)


def render_states(states: List[State], filename="states.out.html"):
	states_template.stream(states=states).dump(filename)