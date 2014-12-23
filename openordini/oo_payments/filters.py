import datetime
from django.contrib import admin

from django.utils.translation import ugettext_lazy as _

class PaymentFilter(admin.SimpleListFilter):

    title = _("payed current year")
    parameter_name = "payed_current_year"

    def lookups(self, request, model_admin):
    
        return (
            (1, _('Yes')),
            (0, _('No')),
        )

    def queryset(self, request, queryset):

        flag = self.value()

        today = datetime.date.today()

#        print "flag: %s, today: %s" % (flag, today)

        if flag == "1":
#            print "qs before 1 : %s" % queryset
            queryset = queryset.filter(order__subscriptionorder__date_end__gte=today)
#            print "res 1 : %s" % queryset.all()
        elif flag == "0":
            queryset = queryset.exclude(order__subscriptionorder__date_end__gte=today)
#            print "res 0 : %s" % queryset.all()

        return queryset

