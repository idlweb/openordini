from django import forms
from django.utils.translation import ugettext_lazy as _

class PaymentForm(forms.Form):

    payment_type = forms.ChoiceField(choices=[], required=True, label=_("payment"))

    def __init__(self, choices, *args, **kwargs):

        super(PaymentForm, self).__init__(*args, **kwargs)

        self.fields["payment_type"].choices = choices


class PaymentInfoForm(forms.Form):
 
    payment_type = forms.CharField(required=True, widget=forms.HiddenInput())   
    billing_address = forms.CharField(max_length=500, required=True, label=_("billing address"))   
    city = forms.CharField(max_length=100, required=True, label=_("city"))
    postcode = forms.CharField(max_length=5, required=True, label=_("postcode"))
    
