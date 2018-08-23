from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, Div, HTML, Field
from django import forms


class BuyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BuyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-buyForm'
        self.helper.form_method = 'post'
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML('<div>How much do you want to purchase for?</div>'),
                    css_class='col-lg-4',
                ),
                Div(
                    css_class='col-lg-1',
                ),
                Div(
                    HTML('<div>You will receive</div>'),
                    css_class='col-lg-4',
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Div(
                        PrependedText('usd_value', '<b>US Dollar ($)</b>', css_class='form-control-lg no-border'),
                        css_class='mr-5'
                    ),
                    css_class='col-lg-4',
                ),
                Div(
                    Div(
                        HTML('<h1 class="text-muted">&#9654;</h1>'),
                    ),
                    css_class='col-lg-1',
                ),
                Div(
                    HTML('<h1><a id="token-receive-estimate">10,000</a> <small><b>XTV</b></small></h1>'),
                    css_class='col-lg-4',
                ),
                css_class='row'
            ),
            Div(
                Div(
                    HTML('<div>How do you want to pay?</div>'),
                    css_class='col-lg-4',
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Div(
                        Field('payment_currency', css_class='form-control-lg no-border'),
                        css_class='mr-5',
                    ),
                    css_class='col-lg-4',
                ),
                css_class='row'
            ),
            Div(
                ButtonHolder(
                    Submit('submit', 'Buy'),
                    css_class='mt-3'
                )
            ),
        )

    usd_value = forms.FloatField(label='', initial=1000, required=True)
    payment_currency = forms.ChoiceField(label='', required=True, choices=(
        ('BTC', "BTC - Bitcoin"),
        ('ETH', "ETH - Ethereum"),
        ('BCH', "BCH - Bitcoin Cash"),
        ('LTC', "LTC - Litecoin"),
        ('XRP', "XRP - Ripple"),
    ))

    def clean(self):
        _usd_value = self.cleaned_data['usd_value']
        _payment_currency = self.cleaned_data['payment_currency']
        _accepted_currencies = ['BTC', 'ETH', 'BCH', 'LTC', 'XRP']

        if _usd_value < 100:
            raise forms.ValidationError("A minimum purchase of US$ 100 is required")

        if _payment_currency not in _accepted_currencies:
            raise forms.ValidationError("Chosen coin cannot be accepted for payment")

        return self.cleaned_data
