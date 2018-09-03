from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import UserProfile
from launchpad.forms.withdraw_forms import AddressUpdateForm


@login_required
def withdraw(request):
    if request.method == 'POST':
        _address_update_form = AddressUpdateForm(request.POST)

        if _address_update_form.is_valid():
            _withdrawal_address = _address_update_form.cleaned_data.get('withdrawal_address')

            _user_profile = UserProfile.objects.basic_profile(user_id=request.user.id).get()
            _user_profile.withdrawal_address = _withdrawal_address
            _user_profile.save()

            return render(request, 'launchpad/withdraw.html', {
                'update_success': True,
                'address_update_form': _address_update_form,
            })

        else:
            return render(request, 'launchpad/withdraw.html', {
                'address_update_form': _address_update_form,
            })

    else:
        _user_profile = UserProfile.objects.basic_profile(user_id=request.user.id).get()
        _address_update_form = AddressUpdateForm(initial={'withdrawal_address': _user_profile.withdrawal_address})

        return render(request, 'launchpad/withdraw.html', {
            'address_update_form': _address_update_form,
        })
