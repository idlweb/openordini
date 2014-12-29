from django import template

register = template.Library()

@register.filter
def fieldset_error(form, fieldset_name):
    
    if not hasattr(form, "fieldsets") or fieldset_name not in form.fieldsets:
        return False

    fields = form.fieldsets[fieldset_name]

    for curr_field in fields:
        if curr_field in form.errors:
            return True

    return False
