from django.contrib import admin
from django.urls import path
from . import views
# from .stkPush import pay  

urlpatterns = [
    path('main/', views.main , name='main'),
    path('accesstoken/', views.find_acesstoken, name='find_acesstoken'),
    path('initiate/', views.initiate_stk_push, name='initiate_stk_push'),
    path('query/', views.query_stk_status, name='query_stk_status'),
    # path('pay/', views.pay, name='pay'),

    # # # path('', views.home, name="home"),
    # # path('token', views.token, name='token'),
 
    # # path('stk', views.stk, name="stk")

]