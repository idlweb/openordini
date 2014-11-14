from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Payment, SubscriptionOrder, SubscriptionPlan

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

    list_display = ("name", "code", "currency", "total_amount",)

admin.site.register(Payment, PaymentAdmin)
admin.site.register(SubscriptionOrder, SubscriptionOrderAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
