from django.template import Template, Context
from django.template.loader import get_template

import os

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

def render(name, data):
    graph = Template(open(os.path.join(path, "graph.html")).read())
    context = { "name": name, "data": data }
    return graph.render(Context(context))