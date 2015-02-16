from django.contrib.admin.widgets import FilteredSelectMultiple, Select


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
    (e.g. through a jquery plugin named chainselect)
    """
    
    def __init__(self, chained_field=None, *args, **kwargs):

        self.chained_field = chained_field
    
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
        return format_html('<option value="{0}"{1}>{2}</option>',
                           option_value,
                           selected_html,
                           force_text(option_label))

