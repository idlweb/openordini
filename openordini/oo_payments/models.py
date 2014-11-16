from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from open_municipio.people.models import Person

# Create your models here.

from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment

pos_dec_validator = MinValueValidator(Decimal('0'))

CURRENCY_CHOICES = (
    ('EURO', _("Euro")),
    ('USD', _("US Dollar"))
)


class SubscriptionPlan(models.Model):

    name = models.CharField(max_length=100, blank=False, verbose_name=_("name"))
    code = models.CharField(max_length=4, blank=False, verbose_name=_("code"))
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, verbose_name=_("net amount"), validators=[pos_dec_validator])
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name=_("tax"), validators=[pos_dec_validator])
    currency = models.CharField(max_length=10,choices=CURRENCY_CHOICES, blank=False, verbose_name=_("currency"))

    @property
    def total_amount(self):
        return self.net_amount + self.tax

    class Meta:
        unique_together = ( ('name',), ('code',))
        verbose_name = _("subscription plan")
        verbose_name_plural = _("subscription plans")


class Order(models.Model):

    person = models.ForeignKey(Person, verbose_name=_("person"))

    name = models.CharField(max_length=500, blank=False, verbose_name=_("order"))
    sku = models.CharField(max_length=10, blank=False, verbose_name=_("sku"))
    quantity = models.DecimalField(max_digits=5, decimal_places=2,blank=False, 
                default=1, 
                verbose_name=_("quantity"), validators=[pos_dec_validator])
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, 
                blank=True, verbose_name=_("currency"))
    

    @property
    def price(self):
        return Decimal(10)

    @property
    def purchased_item(self):
        return PurchasedItem(name=self.name, sku=self.sku, quantity=self.quantity,
                    price=self.price, currency=self.currency)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")


class SubscriptionOrder(Order):
    
    date_begin = models.DateField(blank=False, verbose_name=_("subscription begin"))
    date_end = models.DateField(blank=False, verbose_name=_("subscription end"))
    plan = models.ForeignKey(SubscriptionPlan, blank=False, 
                    verbose_name=_("subscription plan"))

    def save(self, *args, **kwargs):
        self.name = _("%(plan)s - %(person)s - from: %(from)s - to: %(to)s") % {
            "plan": self.plan.name, "from":self.date_begin, "to":self.date_end,
            "person": self.person,
        }
        self.sku = self.plan.code
        self.curr = self.plan.currency
        self.quantity = 1
        return super(SubscriptionOrder, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("subscription order")
        verbose_name_plural = _("subscription orders")


    def __unicode__(self):
        return u"subscription from %(from)s to %(to)s" % { "from":self.date_begin, "to":self.date_end }

class Payment(BasePayment):

    order = models.ForeignKey(Order, blank=True, verbose_name=_("order"))

    def get_failure_url(self):
        return reverse('oo_payment_error')

    def get_success_url(self):
        return reverse('oo_payment_succeed')

    def get_purchased_items(self):
        # you'll probably want to retrieve these from an associated order
        return self.order.purchased_item

    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")
