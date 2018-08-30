from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from launchpad.models import TokenOrders, TokenTransactions


@login_required
def stats(request):
    if request.user.is_staff:
        _orders = TokenOrders.objects
        _sales = TokenTransactions.objects
        _users = get_user_model().objects

        return render(request, 'launchpad/stats.html', {
            'orders': {
                'total': _orders.count(),
                'completed': _orders.completed().count(),
                'pending': _orders.pending().count(),
                'cancelled': _orders.cancelled().count(),
                'stats': _orders.completed().stats(),
            },
            'sales': _sales.deposits().holdings(),
            'users': {
                'total': _users.active_users().count(),
            }
        })
    else:
        return redirect('launchpad:home')
