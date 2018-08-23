from django.urls import path

from . import views

app_name = 'launchpad'
urlpatterns = [
    path('home/', views.home.home, name='home'),
    path('terms/', views.terms.terms, name='terms'),
    path('eligibility/', views.eligibility.eligibility, name='eligibility'),
    path('buy/', views.buy.buy, name='buy'),
    path('payment/<slug:order_id>/', views.payment.payment, name='payment'),
    path('orders/', views.orders.orders, name='orders'),
]
