from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit

class ComparisonCreateForm(forms.Form):
    title = forms.CharField(required = True)
    description = forms.CharField(required = False, widget=forms.Textarea)
    date_starting = forms.DateField(required = False)
    date_ending = forms.DateField(required = False)

    def __init__(self, *args, **kwargs):
        super(ComparisonCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'comparisons:create'
        self.helper.layout = Layout(
            Fieldset(
                None,
                'title',
                'description',
                Field('date_starting', css_class="date-picker"),
                Field('date_ending', css_class="date-picker"),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))
