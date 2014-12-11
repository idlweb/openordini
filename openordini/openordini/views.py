from open_municipio.om.views import HomeView

class OOHomeView(HomeView):

    def get_context_data(self, **kwargs):

        ctx = super(OOHomeView, self).get_context_data(**kwargs)

        print "filter acts header ..."
        return ctx


