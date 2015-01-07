# Create your views here.

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from open_municipio.acts.views import ActDetailView
from .models import Fascicolo

class FascicoloDetailView(ActDetailView):
    model = Fascicolo

    def get_object(self):

        user = self.request.user
        act = super(FascicoloDetailView, self).get_object()

#        print "user: %s, act: %s" % (user, act)

        if user.is_superuser:
            return act

        allowed_persons = map(lambda c: c.person, act.recipient_set.all())

#        print "allowed: %s" % allowed_persons
#        print "user: %s (%s)" % (user, user.is_anonymous())

        if user.is_anonymous():
#            print "it's anonymous..."
            raise PermissionDenied

#        print "non anonymous..."

        try:
            profile = user.get_profile()
#        print "profile: %s" % profile
            person = profile.person if profile else None
#        print "person: %s" % person

            if not person or person not in allowed_persons:
                raise PermissionDenied

        except ObjectDoesNotExist:
            raise PermissionDenied

        return act

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(FascicoloDetailView, self).dispatch(request, *args, **kwargs)
        except PermissionDenied, e:
#            print "error: %s" % e
            messages.warning(request, _("The act you are trying to access is visible only to a subset of the users. You may try to access as a different user, if you have other credentials."))
            base_url = reverse("auth_login")
            full_url = "%s?next=%s" % (base_url, request.path)
            return HttpResponseRedirect(full_url)
