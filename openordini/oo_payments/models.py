from datetime import datetime
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from open_municipio.people.models import Person, Institution
from openordini.oo_users.models import UserProfile

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
    code = models.CharField(max_length=100, blank=False, verbose_name=_("code"))
    institution_set = models.ManyToManyField(Institution, blank=True, null=True, verbose_name=_("institutions"))
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, verbose_name=_("net amount"), validators=[pos_dec_validator])
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name=_("tax"), validators=[pos_dec_validator])
    currency = models.CharField(max_length=10,choices=CURRENCY_CHOICES, blank=False, verbose_name=_("currency"))

    @property
    def institutions(self):
        return self.institution_set.all()

    @property
    def total_amount(self):
        net = self.net_amount or 0
        tax = self.tax or 0
        return net + tax

    @staticmethod
    def get_for_user(user):
        
#        assert isinstance(user, User)

        filtered_plans = []

        try:

            profile = user.get_profile()
            assert isinstance(profile, UserProfile)
    
            # add the payment form  
            user_charges = profile.committee_charges
            yearly_plans = settings.PAYMENT_DEADLINES.keys()
            today = datetime.today()
    
#            print "user charges: %s" % user_charges
        
            plans = SubscriptionPlan.objects.filter(institution_set__charge_set__person__userprofile=profile).exclude(subscriptionorder__person=profile.person, code__in=yearly_plans, subscriptionorder__date_end__lte=today).distinct()
#            print "user plans: %s" % plans


            for curr_plan in plans:
                dl_text = settings.PAYMENT_DEADLINES.get(curr_plan.code, None)
                dl = None

                if dl_text:
                    dl = datetime.strptime(dl_text % today.year, "%Y-%m-%d")

                if not dl or today <= dl:
                    filtered_plans.append(curr_plan)

        except AttributeError: 
            pass

        return filtered_plans


    class Meta:
        unique_together = ( ('name',), ('code',))
        verbose_name = _("subscription plan")
        verbose_name_plural = _("subscription plans")

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.code)


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

    def __unicode__(self):
        return "%s - %s" % (self.name, self.person)


class SubscriptionOrder(Order):
    
    date_begin = models.DateField(blank=False, verbose_name=_("subscription begin"))
    date_end = models.DateField(blank=False, verbose_name=_("subscription end"))
    plan = models.ForeignKey(SubscriptionPlan, blank=False, verbose_name=_("subscription plan"))

    def save(self, *args, **kwargs):
        self.name =  "test"
        ("%(plan)s - %(person)s - from: %(from)s - to: %(to)s") % {
            "plan": self.plan.name, "from":self.date_begin, "to":self.date_end,
            "person": self.person,
        }
        self.sku = "sku" # self.plan.code
        self.curr = self.plan.currency
        self.quantity = 1
        return super(SubscriptionOrder, self).save(*args, **kwargs)

    @property
    def year(self):
        return self.date_begin.year

    @staticmethod
    def get_for_person(person, year):

        assert isinstance(person, Person)
 
        so = None
        last_day = "%s-12-31" % year # last day of year

        try:
            so = SubscriptionOrder.objects.get(person=person, date_begin__lte=last_day, date_end__gte=last_day)
        except ObjectDoesNotExist:
            pass

        return so

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

class Subscription(Person):

    class Meta:
        proxy = True
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")
