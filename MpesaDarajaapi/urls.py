from django.contrib import admin
from django.urls import path
from . import views
from .views import stk_form_view
from .callback import process_stk_callback 

urlpatterns = [
    # path('main/', views.main , name='main'),
    # path('accesstoken/', views.find_acesstoken, name='find_acesstoken'), #Retriving and seeing the current acess token
    # path('stk/', views.start, name='start'), #for initiating the process
    # path('results/', views.run_query, name='run_query'), # for query running
    path('admin/', admin.site.urls),  
    # path('payments/', payment_list, name='payment_list'), #redirect the list to the template you want
    path('', stk_form_view, name='stk_form'),
    path('payment-success/', views.latest_payment, name='payment-success'),
    path("api/v1/stk/callback/", process_stk_callback, name="stk_callback"),
    
]
