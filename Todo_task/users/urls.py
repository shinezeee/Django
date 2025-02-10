from enum import verify

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.cb_views import SignUpView, verify_email

urlpatterns = [
    path('signup/',SignUpView.as_view(), name='cbv_signup'),
    path('login/',LoginView.as_view(template_name='registration/login.html'), name='cbv_login'),
    path('logout/',LogoutView.as_view(), name='cbv_logout'),
    path('verify/',verify_email,name='verify_email'),
]