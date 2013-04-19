
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def message_css_class(message_tags):
    css_classes = []
    tag_constants = ['debug', 'info', 'success', 'warning', 'error']

    for tag in message_tags.split():
        if tag in tag_constants:
            css_classes.append('alert-%s' % tag)
        else:
            css_classes.append(tag)

    return ' '.join(css_classes)
