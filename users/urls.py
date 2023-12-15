from django.urls import path
from .views import sign_in, sign_up, logout_user
from common.ip_filter import ip_filter

app_name = 'users'

urlpatterns = [
    path('signin/', ip_filter(sign_in), name='login'),
    path('signup/', ip_filter(sign_up), name='reg'),
    path('logout/', ip_filter(logout_user), name='logout'),
]
