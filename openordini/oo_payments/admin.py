from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Payment, SubscriptionOrder, SubscriptionPlan, Subscription

from open_municipio.people.models import municipality

class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order_name", "order_person", "status", )
    list_filter = ("status", )

    raw_id_fields = ["order",]

    def order_name(self, obj):
        return obj.order.name
    order_name.short_description = _("name")
    order_name.admin_order_field = "order__name"

    def order_person(self, obj):
        return obj.order.person
    order_person.short_description = _("person")
    order_person.admin_order_field = "order__person__last_name"


class SubscriptionOrderAdmin(admin.ModelAdmin):
    pass


class SubscriptionPlanAdmin(admin.ModelAdmin):
    
    readonly_fields = [ "total_amount", ]

    list_display = ("name", "code", "currency", "total_amount", )


class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ("last_name", "first_name", "username", "order_label",)

    def username(self, object):
        return object.userprofile.user.username

    def curr_year_subscription_order(self, object):
        """
        Return the subscription order for the current year, or None if not payed
        """

        last_order = None

        all_orders = object.order_set.order_by("-subscriptionorder__date_end")

        if len(all_orders) > 0:
            last_order = all_orders[0]

        return last_order

    def order_label(self, object):
        label = ""
        curr_order = self.curr_year_subscription_order(object)

        if curr_order:
            label = "%s" % curr_order.name

        return label
        

    def queryset(self, request):

        all_comm = municipality.committees.as_institution()

        return self.model.objects.filter(institutioncharge__institution__in=all_comm).distinct()


admin.site.register(Payment, PaymentAdmin)
admin.site.register(SubscriptionOrder, SubscriptionOrderAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
