from django import template
register = template.Library()

@register.filter
def widget_name(value):
    return value.field.widget.__class__.__name__   
