from django.shortcuts import render


# Create your views here.
from .main import main
from .generateAcesstoken import get_access_token
from .stkPush import initiate_stk_push
from .query import query_stk_status

# views.py

# def pay(request):
#     return render(request, 'Mpesa/pay.html')