from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder
from django import forms


class TermsAcceptanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TermsAcceptanceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-termsAcceptanceForm'
        self.helper.form_method = 'post'
        self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            ButtonHolder(
                Submit('submit', 'Agree & Continue', css_class='btn-encourage'),
            )
        )

    term_type = forms.CharField(widget=forms.HiddenInput())
    term_version = forms.CharField(widget=forms.HiddenInput())
