from django.contrib import admin

from apps.compliance.models import Survey, SurveyQuestion, SurveyQuestionAnswer

admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyQuestionAnswer)
