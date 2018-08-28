from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, ButtonHolder
from django import forms
from zxcvbn_password import PasswordField, PasswordConfirmationField


class SignupPrelimForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SignupPrelimForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-signupPrelimForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div('email'),
            Div(
                ButtonHolder(
                    Submit('submit', 'Create account'),
                ),
            ),
            Div(
                HTML(
                    'Already have an account?&nbsp;&nbsp;&#9654; <a href="/accounts/login/"><b>Login here</b></a>',
                ),
                css_class='mt-5'
            ),
        )

    email = forms.EmailField(label='Your email address')


class SignupFinishSetupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SignupFinishSetupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-signupFinishSetupForm'
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
                    '<p class="col-md-6"><small>A password should contain at least 9 characters and should not use common phrases.</small></p>',
                ),
                css_class='row'
            ),
            # Div('first_name'),
            # Div('last_name'),
            # Div(
            #     Div('country', css_class='col-md-6'),
            #     Div('phone', css_class='col-md-6'),
            #     css_class='row'
            # ),
            ButtonHolder(
                Submit('submit', 'Finish setup'),
                css_class='mt-3'
            )
        )

    signed_email = forms.CharField(widget=forms.HiddenInput())
    # password = forms.CharField(label='Create a password')
    # password_confirm = forms.CharField(label='Confirm password')
    password = PasswordField(label='Create a password')
    password_confirm = PasswordConfirmationField(label='Confirm password', confirm_with='password')

    # first_name = forms.CharField(label='First name', min_length=2, max_length=128)
    # last_name = forms.CharField(label='Last name', min_length=2, max_length=128)
    # country = forms.ModelChoiceField(label='Residing country',
    #                                  queryset=PresenceCountry.objects.filter(is_active=True), empty_label=None)
    # phone = forms.IntegerField(label='Local phone number')

    def clean(self):
        _password_confirm = self.cleaned_data.get('password_confirm')
        _password = self.cleaned_data.get('password')

        if _password and _password_confirm != _password:
            raise forms.ValidationError("Passwords do not match")

        return self.cleaned_data
