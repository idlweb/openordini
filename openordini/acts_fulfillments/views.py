# Create your views here.

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from open_municipio.acts.views import ActDetailView
from .models import Fascicolo

class FascicoloDetailView(ActDetailView):
    model = Fascicolo

    def get_object(self):

        user = self.request.user
        act = super(FascicoloDetailView, self).get_object()

        print "user: %s, act: %s" % (user, act)

        if user.is_anonymous or user not in act.recipient_set:
            raise PermissionDenied("foo")

        return act

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(FascicoloDetailView, self).dispatch(request, *args, **kwargs)
        except PermissionDenied, e:
            messages.warning(request, _("The act you are trying to access is visible only to a subset of the users. You may try to access as a different user, if you have other credentials."))
            return redirect("auth_login")
