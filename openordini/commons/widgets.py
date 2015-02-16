from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import Select
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class AdvancedFilteredSelectMultiple(FilteredSelectMultiple):

    def render(self, *args, **kwargs):

        attrs = kwargs.get("attrs", None)

        if attrs is None:
            attrs = {}

        # self.attrs contains the parameter attrs passed at the constructor __init__
        attrs.update(self.attrs)

        kwargs["attrs"] = attrs

        return super(AdvancedFilteredSelectMultiple, self).render(*args, **kwargs)


class ChainedSelect(Select):
    """
    This select renders a select whose options are linked to a previous one
    (e.g. through a jquery plugin named chainselect).

    See: http://www.appelsiini.net/projects/chained
    for a tutorial on how to use chained select and this widget
    """
    
    def __init__(self, chained_values=None, *args, **kwargs):
        """
        chained_values must be a dictionary:
        { "value" : "chained value" }
        where "value" is a value of the current select, and "chained value" is
        a value (or a list of values) on the chained select
        """
        
        self.chained_values = chained_values
    
        super(ChainedSelect, self).__init__(*args, **kwargs)


    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        parent_values = self.chained_values.get(option_value, None)

        if parent_values:
            parent_values = (" class='%s'" % " ".join(parent_values))

        return format_html('<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           mark_safe(parent_values),
                           selected_html,
                           force_text(option_label))

