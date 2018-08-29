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
                    Div(
                        PrependedText('usd_value', '<b>US Dollar ($)</b>', css_class='form-control-lg no-border'),
                        css_class='mr-lg-5 mr-sm-0',
                    ),
                    css_class='col-lg-4',
                ),
                Div(
                    HTML('<div>You will receive</div>'),
                    Div(
                        HTML('<h1><span class="text-muted">&#9654;</span> <a id="token-receive-estimate">10,000</a> <small><b>XTV</b></small></h1>'),
                    ),
                    Div(
                        HTML('<p id="minimum-message" class="text-danger" style="display:none;">for a minimum purchase of US$100</p>'),
                        style='height: 20px;'
                    ),
                    css_class='col-lg-5',
                ),
                css_class='row'
            ),
            Div(
                Div(
                    HTML('<div>How do you want to pay?</div>'),
                    Div(
                        Field('payment_currency', css_class='form-control-lg no-border'),
                        css_class='mr-lg-5 mr-sm-0',
                    ),
                    css_class='col-lg-4',
                ),
                css_class='mt-2 row'
            ),
            Div(
                ButtonHolder(
                    Submit('submit', 'Buy', css_class='btn-encourage'),
                    css_class='mt-3',
                    css_id='buy-submit-button',
                ),
                HTML('<div id="buy-loading-spinner" class="mt-3" style="display: none;"><button class="btn btn-primary btn-encourage disabled"><i class="fa fa-spinner fa-lg fa-spin text-white"></i></button></div>'),
            ),
        )

    usd_value = forms.FloatField(label='', initial=1000, required=True)
    payment_currency = forms.ChoiceField(label='', required=True, choices=(
        ('BTC', "BTC - Bitcoin"),
        ('BCH', "BCH - Bitcoin Cash"),
        ('ETH', "ETH - Ethereum"),
        ('ETC', "ETC - Ethereum Classic"),
        ('DASH', "DASH - Dash"),
        ('LTC', "LTC - Litecoin"),
        ('TRX', "TRX - Tronix"),
        ('LTCT', "LTCT - Litecoin Testnet"),
    ))

    def clean(self):
        _usd_value = self.cleaned_data.get('usd_value')
        _payment_currency = self.cleaned_data.get('payment_currency')
        _accepted_currencies = [
            'BTC',
            'BCH',
            'ETH',
            'ETC',
            'DASH',
            'LTC',
            'TRX',
            'LTCT',
        ]

        if _usd_value < 100:
            raise forms.ValidationError("A minimum purchase of US$ 100 is required")

        if _payment_currency not in _accepted_currencies:
            raise forms.ValidationError("The coin you chose cannot be accepted for payment")

        return self.cleaned_data
