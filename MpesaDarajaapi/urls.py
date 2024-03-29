from django.contrib import admin
from django.urls import path
from . import views
# from .stkPush import pay  

urlpatterns = [
    path('main/', views.main , name='main'),
    path('accesstoken/', views.find_acesstoken, name='find_acesstoken'), #Retriving and seeing the current acess token
    path('stk/', views.start, name='start'), #for initiating the process
    path('results/', views.run_query, name='run_query'), # for query running
   

]
