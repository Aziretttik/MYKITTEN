from django.urls import path
from . import views

urlpatterns = [
    path('user_register/', views.user_register, name='user_register' ),
    path('user_login/', views.user_login, name='user_login'),
    path('verify/', views.verify_code, name='verify_code'),
    path('user_logout/', views.user_logout, name='user_logout'),
]
