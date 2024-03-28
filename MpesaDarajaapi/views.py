from django.shortcuts import render


# Create your views here.
from .main import main
from .acesstokener import find_acesstoken
from .stkPush import start
from .query import query_stk_status

# views.py

# def pay(request):
#     return render(request, 'Mpesa/pay.html')