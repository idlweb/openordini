from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import Http404
from open_municipio.users.models import User
from open_municipio.users.views import UserProfileDetailView, UserProfileListView, \
                                        extract_top_monitored_objects
from open_municipio.people.models import municipality
from open_municipio.newscache.models import News
from open_municipio.acts.models import Deliberation, Interpellation, Interrogation, Agenda, Motion, Amendment

from ..oo_payments.forms import PaymentForm
from ..oo_payments.models import SubscriptionPlan, SubscriptionOrder
from ..acts_fulfillments.models import Fascicolo
from .models import UserProfile

from ..commons.mixins import FilterNewsByUser

class OOUserProfileDetailView(FilterNewsByUser, UserProfileDetailView):

    model = UserProfile
 
    def get_object(self, queryset=None):

        profile = None
        user = self.request.user

        url_username = self.kwargs.get("username", None)

        try:
            if url_username:
                user = User.objects.get(username=url_username)
            
            profile = user.get_profile()
        except (ObjectDoesNotExist, AttributeError):
#            pass
            raise Http404

        return profile
   
    def get_context_data(self, **kwargs):

        ctx = super(OOUserProfileDetailView, self).get_context_data(**kwargs)

        curr_person = None
        ctx["acts_facicoli"] = None

        try:
            curr_person = self.object.person

#            print "person: %s" % curr_person
            ctx["acts_fascicoli"]  = Fascicolo.objects.filter(recipient_set__person=curr_person) 

            curr_year = datetime.today().year

            ctx["curr_subscription"] = SubscriptionOrder.get_for_person(curr_person, curr_year)

        except (ObjectDoesNotExist, AttributeError), err:
            print "error: %s" % err


        """ 
        map: data una funzione ed una sequenza 
        applica quella funzione ad agni elemento 
        della sequenza 
        """
        plans = SubscriptionPlan.get_for_user(self.request.user)
        plan_choices = []

        if plans:
            plan_choices = map(lambda p: (p.pk, p.name), plans)

#        print "plan choices: %s" % plan_choices
        ctx["form_payment"] = PaymentForm(choices=plan_choices)


        all_news = self.object.related_news
        filtered_news = self.filter_news(all_news, self.request.user)

#        print "all news: %s" % all_news
#        print "filtered news: %s" % filtered_news

        ctx["profile_news"] = sorted(filtered_news, key=lambda n: n.news_date, reverse=True)[0:3]


        return ctx


class OOUserProfileListView(FilterNewsByUser, UserProfileListView):
    
    def get_context_data(self, **kwargs):



#        print "in custom view ..."

        ctx = super(OOUserProfileListView, self).get_context_data(**kwargs)
    
        news = News.objects.filter(news_type=News.NEWS_TYPE.community, priority=1)
        filtered_news = self.filter_news(news, self.request.user)

        ctx["news_community"] = sorted(filtered_news, key=lambda n: n.news_date,
                                reverse=True)[0:3]

        # below it is not possible to use the mixin method filter_acts because
        # extract_top_monitored_objects does not return a QuerySet

        all_acts = extract_top_monitored_objects(Deliberation, Motion, 
                        Interpellation, Agenda, Interrogation, Amendment, Fascicolo, qnt=5)

        ctx["top_monitored_acts"] = self.filter_monitored_acts(all_acts)

        return ctx



    def filter_monitored_acts(self, all_acts):

        person = None

        try:
            person = self.request.user.get_profile().person
        except Exception:
            pass

        filtered_acts = []
        for curr_row in all_acts:


            if isinstance(curr_row["object"], Fascicolo):
                if not person:
                    # user has no associated person: don't show the Fascicolo
                    continue

                # otherwise check against recipients
                recipient_people = map(lambda c: c.person, curr_row["object"].recipients)
#                print "recipient people: %s" % recipient_people
#                print "person: %s" % person
                if person not in recipient_people:                
                    # person not in Fascicolo recipients
#                    print "person not found ..."
                    continue    

            filtered_acts.append(curr_row)

        return filtered_acts


