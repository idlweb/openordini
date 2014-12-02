from django import template

register = template.Library()

@register.filter(name='foo')
def foo(value):
    print "cap: %s" % value.capabilities
    print "type: %s" % type(value)
    print "value: %s" % value

