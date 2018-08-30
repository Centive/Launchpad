from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, ButtonHolder
from django import forms
from zxcvbn_password import PasswordField, PasswordConfirmationField


class PasswordResetPrelimForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PasswordResetPrelimForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-passwordResetPrelimForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div('email'),
            Div(
                ButtonHolder(
                    Submit('submit', 'Reset Password'),
                ),
            ),
            Div(
                HTML(
                    '<a class="text-dark">Want to use the old password?</a>&nbsp;&nbsp;&#9654; <a href="/accounts/login/"><b>Login here</b></a>',
                ),
                css_class='mt-5'
            ),
        )

    email = forms.EmailField(label='Your email address')


class PasswordResetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-passwordResetForm'
        self.helper.form_method = 'post'
        self.helper.render_hidden_fields = True
        self.helper.include_media = False
        self.helper.layout = Layout(
            Div(
                Div('password', css_class='col-md-5'),
                Div('password_confirm', css_class='col-md-5'),
                css_class='row'
            ),
            Div(
                HTML(
                    '<p class="col-md-6"><small>A password should contain at least 9 characters.</small></p>',
                ),
                css_class='row'
            ),
            ButtonHolder(
                Submit('submit', 'Change password'),
                css_class='mt-3'
            )
        )

    signed_email = forms.CharField(widget=forms.HiddenInput())
    password = PasswordField(label='Create new password')
    password_confirm = PasswordConfirmationField(label='Confirm password', confirm_with='password')

    def clean(self):
        _password_confirm = self.cleaned_data.get('password_confirm')
        _password = self.cleaned_data.get('password')

        if _password and _password_confirm != _password:
            raise forms.ValidationError("Passwords do not match")

        return self.cleaned_data
