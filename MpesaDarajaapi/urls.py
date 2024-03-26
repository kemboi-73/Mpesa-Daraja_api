from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('main/', views.main , name='main'),
    path('accesstoken/', views.access_token, name='get_access_token'),
    path('initiate/', views.start_stk, name='initiate_stk_push'),
    path('query/', views.query_stk_status, name='query_stk_status'),
    # path('callback/', views.callback_view, name='callback'),
]

