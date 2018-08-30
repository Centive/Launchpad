from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, ButtonHolder, Button
from django import forms


class SessionLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SessionLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-sessionLoginForm'
        self.helper.form_method = 'post'
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            Div('email'),
            Div('password'),
            Div(
                ButtonHolder(
                    Submit('submit', 'Login'),
                    css_class='col-lg-6'
                ),
                HTML('<div class="col-lg-6 text-right text-dark"><small><a href="/accounts/password-reset-request/">Forgot password?</a></small></div>'),
                css_class='row'
            ),
            Div(
                HTML(
                    '<a class="text-dark">Don\'t have a Centive account?</a>&nbsp;&nbsp;&#9654; <a href="/accounts/signup-prelim/"><b>Signup here</b></a>',
                ),
                css_class='mt-5'
            ),
        )

    email = forms.EmailField(label='Your email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
