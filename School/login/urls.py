from django.urls import path
from . import views

urlpatterns = [
    path('', views.Login, name='login'),
    path('type/', views.Type_user, name='type-user'),
    path('form/', views.Form_generic, name='form-generic'),
]