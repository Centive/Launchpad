import eth_utils
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Div, HTML
from django import forms


class AddressUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddressUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-buyForm'
        self.helper.form_method = 'post'
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            HTML('<div>Your Ethereum Wallet address</div>'),
            Div(
                Div(
                    'withdrawal_address',
                    css_class='col-lg-11 form-control-lg no-border pl-0 text-monospace d-inline-block',
                ),
                Div(
                    HTML('<i id="address-helper-correct" class="fa fa-check-circle fa-lg text-success"></i><i id="address-helper-wrong" class="fa fa-times-circle fa-lg text-danger"></i>'),
                    css_class='d-inline-block'
                ),
                css_class='row ml-0 middle-box-flex'
            ),
            Div(
                ButtonHolder(
                    Submit('submit', 'Update', css_class='btn-encourage'),
                    css_class='mt-3',
                ),
            ),
        )

    withdrawal_address = forms.CharField(label='', required=True)

    def clean(self):
        _withdrawal_address = self.cleaned_data.get('withdrawal_address')

        if not eth_utils.is_address(_withdrawal_address):
            raise forms.ValidationError("Incorrect Ethereum address. Please check again.")

        return self.cleaned_data
