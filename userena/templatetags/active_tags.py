__author__ = 'jbo'

from django import template
register = template.Library()

@register.simple_tag
def active(request, pattern, strict=True, return_value='active'):
    """
    {% load active_tags %}
    {% url 'userena_profile_detail' user.username as profile_detail %}
    <li class="{% active request profile_detail %}"><a href="{{ profile_detail }}">{% trans "View profile" %}</a></li>
    """
    import re
    if strict:
        if pattern == request.path:
          return return_value
    else:
        if re.search(pattern, request.path):
          return return_value
    return ''
