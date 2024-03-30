from django.shortcuts import render


# Create your views here.
from .main import main
from .acesstokener import find_acesstoken
from .stkPush import start
from .query import run_query


#Update for frontend payment list 
# from .models import Payment

# def payment_list(request):
#     payments = Payment.objects.all()
#     return render(request, 'payment_list.html', {'payments': payments})
