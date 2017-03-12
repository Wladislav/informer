import re

from django.utils.functional import allow_lazy
from django.utils.encoding import force_text
from django.template import Node, Library

register = Library()

def strip_empty_lines(value):
    """Return the given HTML with empty and all-whitespace lines removed."""
    return re.sub(r'\n[ \t]*(?=\n)', '', force_text(value))
strip_empty_lines = allow_lazy(strip_empty_lines, 'utf-8')

class GaplessNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return strip_empty_lines(self.nodelist.render(context).strip())

def gapless(parser, token):
    """
    Remove empty and whitespace-only lines.  Useful for getting rid of those
    empty lines caused by template lines with only template tags and possibly
    whitespace.

    Example usage::

        <p>{% gapless %}
          {% if yepp %}
            <a href="foo/">Foo</a>
          {% endif %}
        {% endgapless %}</p>

    This example would return this HTML::

        <p>
            <a href="foo/">Foo</a>
        </p>

    """
    nodelist = parser.parse(('endgapless',))
    parser.delete_first_token()
    return GaplessNode(nodelist)
gapless = register.tag(gapless)