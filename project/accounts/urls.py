from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='accounts:login', permanent=False)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup-prelim/', views.signup_prelim, name='signup-prelim'),
    path('signup-prelim-success/', views.signup_prelim_success, name='signup-prelim-success'),
    path('finish-setup/<str:signed_email>/', views.signup_finish_setup, name='signup-finish-setup'),
]
