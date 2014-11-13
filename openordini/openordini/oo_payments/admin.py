from django.contrib import admin

from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Payment, PaymentAdmin)
