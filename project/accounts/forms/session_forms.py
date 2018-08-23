from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, ButtonHolder
from django import forms
from django.urls import reverse


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
                ),
            ),
            Div(
                HTML(
                    'Don\'t have an investor account? <a href="/accounts/signup-prelim/">Signup here</a>',
                ),
                css_class='mt-5'
            ),
        )

    email = forms.EmailField(label='Your email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
