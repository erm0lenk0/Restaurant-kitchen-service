from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    request = context['request']
    update = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            update[key] = value
        else:
            update.pop(key)
    return update.urlencode()