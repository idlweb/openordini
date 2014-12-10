from django import template

from openordini.cas_integration.models import GroupCapability

register = template.Library()

@register.filter(name='get_capabilities')
def get_capabilities(user):

    user_caps = user.capabilities.all()
    print "orig user caps: %s" % user_caps
    group_caps = GroupCapability.objects.filter(group__in=user.groups.all())
    print "orig group caps: %s" % group_caps

    user_caps_replaced = map(lambda c: ( c.name, c.link.replace("<USER>", c.user.username)), user_caps)
    print "dict user caps: %s" % user_caps_replaced
    group_caps_replaced = map(lambda c: ( c.name, c.link.replace("<GROUP>", c.group.name)), group_caps)
    print "dict group caps: %s" % group_caps_replaced

    return user_caps_replaced + group_caps_replaced
