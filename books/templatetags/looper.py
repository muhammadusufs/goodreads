from django import template

register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter(name='sub')
def sub(number):
    return 5-number