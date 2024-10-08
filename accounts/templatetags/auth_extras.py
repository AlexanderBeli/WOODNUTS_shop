from django import template
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_protect

register = template.Library()


@csrf_protect
@register.filter(name="has_group")
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
