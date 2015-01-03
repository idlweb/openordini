from django.contrib.admin.widgets import FilteredSelectMultiple


class AdvancedFilteredSelectMultiple(FilteredSelectMultiple):

    def render(self, *args, **kwargs):

        attrs = kwargs.get("attrs", None)

        if attrs is None:
            attrs = {}

        # self.attrs contains the parameter attrs passed at the constructor __init__
        attrs.update(self.attrs)

        kwargs["attrs"] = attrs

        return super(AdvancedFilteredSelectMultiple, self).render(*args, **kwargs)


