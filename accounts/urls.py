from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetCompleteView, PasswordChangeView, PasswordResetDoneView
from .views import *


urlpatterns=[
    path('signup/',signup, name='signup'),
    path('login/',LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/',)
]