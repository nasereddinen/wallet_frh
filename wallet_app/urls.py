from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('create_wallet/', views.create_wallet, name='create_wallet')
]

