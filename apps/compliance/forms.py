from django import forms

from apps.compliance.models import Survey, SurveyQuestion


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        exclude = ('slug',)

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SurveyQuestionForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestion
        exclude = ('slug', 'survey')

    def __init__(self, *args, **kwargs):
        super(SurveyQuestionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
