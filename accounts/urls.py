from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('index/', views.index),
    path('add/', views.add_user),
    path('show/', views.get_users),
]
