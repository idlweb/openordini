from open_municipio.om.views import HomeView
from open_municipio.acts.models import Act
from ..commons.mixins import FilterActsByUser

class OOHomeView(FilterActsByUser, HomeView):

    def get_context_data(self, **kwargs):

        ctx = super(OOHomeView, self).get_context_data(**kwargs)

        last_presented_acts = Act.objects.filter(presentation_date__isnull=False).distinct()
        filtered_presented_acts = self.filter_acts(last_presented_acts, self.request.user).order_by('-presentation_date')[0:3]
        ctx["last_presented_acts"] = filtered_presented_acts

        return ctx


