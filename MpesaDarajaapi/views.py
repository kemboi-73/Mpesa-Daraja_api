from django.shortcuts import render


def stk_form_view(request):
    return render(request, 'stkform.html')

from .models import Payment

def latest_payment(request):
    payment = Payment.objects.last()
    return render(request, 'payment_success.html', {'payment': payment})
