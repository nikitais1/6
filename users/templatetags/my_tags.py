from django import template

register = template.Library()


@register.filter()
@register.simple_tag()
def mediapath(val):
    if val:
        return f'/media/{val}'
    return ''
