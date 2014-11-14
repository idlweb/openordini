from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded

def payment_details(request, id):
    payment = get_object_or_404(get_payment_model(), id=id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'oo_payments/payment.html',
                            {'form': form, 'payment': payment})
