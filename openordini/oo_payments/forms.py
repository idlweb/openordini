from django import forms
from django.utils.translation import ugettext_lazy as _

class PaymentForm(forms.Form):

    payment_type = forms.ChoiceField(choices=[], required=True, label=_("payment"))

    def __init__(self, choices, *args, **kwargs):

        super(PaymentForm, self).__init__(*args, **kwargs)

        self.fields["payment_type"].choices = choices


    
