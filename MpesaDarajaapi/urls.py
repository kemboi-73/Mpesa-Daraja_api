from django.contrib import admin
from django.urls import path
from . import views
# from .stkPush import pay  

urlpatterns = [
    path('main/', views.main , name='main'),
    path('accesstoken/', views.find_acesstoken, name='find_acesstoken'),
    path('initiate/', views.start, name='start'),
    path('query/', views.run_query, name='query_stk_status'),
    # path('pay/', views.pay, name='pay'),

    # # # path('', views.home, name="home"),
    # # path('token', views.token, name='token'),
 
    # # path('stk', views.stk, name="stk")

]