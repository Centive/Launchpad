from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from launchpad.models import TokenOrders


@login_required
def orders(request):
    _user_id_external = request.user.id_external

    _orders = TokenOrders.objects.token_orders(customer_external_id=_user_id_external)
    return render(request, 'launchpad/orders.html', {'orders': _orders})
