from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'launchpad'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='launchpad:home', permanent=False)),
    path('home/', views.home.home, name='home'),
    path('terms/', views.terms.terms, name='terms'),
    path('eligibility/', views.eligibility.eligibility, name='eligibility'),
    path('buy/', views.buy.buy, name='buy'),
    path('payment/<slug:order_id>/', views.payment.payment, name='payment'),
    path('orders/', views.orders.orders, name='orders'),
    path('transactions/', views.transactions.transactions, name='transactions'),
    path('verification/', views.verification.verification, name='verification'),
    path('withdraw/', views.withdraw.withdraw, name='withdraw'),
    path('data/payment/update/', views.data.payment.update, name='data-payment-update'),
    path('stats/', views.stats.stats, name='stats'),
]
