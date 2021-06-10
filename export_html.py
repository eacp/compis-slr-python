from grammar import Grammar
from jinja2 import Template

# FF means first & follow

with open("templates/first_follow.html", 'r') as ff:
	# Read the entire file into the ff_template
	ff_template: Template = Template(ff.read())

g = Grammar()

def render_first_follow(grammar: Grammar, filename="first-follow.out.html"):
	# Render to the file
	ff_template.stream(grammar=grammar).dump(filename)
