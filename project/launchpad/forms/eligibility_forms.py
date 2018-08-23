from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, ButtonHolder, HTML, Field
from django import forms


class EligibilityConfirmationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EligibilityConfirmationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-eligibilityConfirmationForm'
        self.helper.form_method = 'post'
        self.helper.render_hidden_fields = True
        self.helper.include_media = False
        self.helper.layout = Layout(
            ButtonHolder(
                Submit('submit', 'Continue', css_id='eligibility-check-submit'),
            ),
        )
