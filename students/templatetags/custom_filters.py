from django import template

register = template.Library()

@register.filter(name='length_is')
def length_is(value, arg):
    """Check if the length of the value is equal to the given argument."""
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False