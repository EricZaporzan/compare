from django import forms
from django.utils import timezone

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit


class ComparisonCreateForm(forms.Form):
    title = forms.CharField(required=True, label="What should it be called?")
    description = forms.CharField(required=False, widget=forms.Textarea, label="Outline the rules, guidelines, and anything else important about this comparison.")
    date_starting = forms.DateField(required=True, label="When should we start?", initial=timezone.now().strftime("%m/%d/%Y"))
    date_ending = forms.DateField(required=False, label="When should we finish?")

    def __init__(self, *args, **kwargs):
        super(ComparisonCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'comparisons:create'
        self.helper.layout = Layout(
            Fieldset(
                None,
                'title',
                'description',
                Field('date_starting', css_class="date-picker", placeholder="Pick a start date"),
                Field('date_ending', css_class="date-picker", placeholder="Pick an end date (optional)"),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))


class ComparisonUpdateForm(forms.Form):
    title = forms.CharField(required=True, label="What should it be called?")
    description = forms.CharField(required=False, widget=forms.Textarea, label="Outline the rules, guidelines, and anything else important about this comparison.")
    date_starting = forms.DateField(required=True, label="When should we start?")
    date_ending = forms.DateField(required=False, label="When should we finish?")

    def __init__(self, *args, **kwargs):
        super(ComparisonUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                None,
                'title',
                'description',
                Field('date_starting', css_class="date-picker", placeholder="Pick a start date"),
                Field('date_ending', css_class="date-picker", placeholder="Pick an end date (optional)"),
            )
        )
        self.helper.add_input(Submit('submit', 'Update'))
