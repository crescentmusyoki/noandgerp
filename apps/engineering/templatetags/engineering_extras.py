from datetime import datetime

from django import template
from django.shortcuts import get_object_or_404

from apps.compliance.models import SurveyQuestionAnswer, SurveyQuestion
from apps.engineering.forms import ProjectEquipmentForm
from apps.engineering.models import ProjectEquipment, ProjectFabrication
from configs import SURVEY_TYPE, QUESTION_TYPE

register = template.Library()


@register.filter(name='task_date_check')
def task_date_check(value):
    task_date = datetime.strptime(str(value), "%Y-%m-%d").date()
    present_date = datetime.now().today()

    d1 = datetime(task_date.year, task_date.month, task_date.day)
    d2 = datetime(present_date.year, present_date.month, present_date.day)

    return d1 < d2


@register.filter(name='question_type')
def question_type(value):
    return QUESTION_TYPE[int(value) - 1][1]


@register.filter(name='question_answered')
def question_answered(value, project_task):
    fabrication_task = get_object_or_404(ProjectFabrication, slug=project_task)
    question_asked = get_object_or_404(SurveyQuestion, id=value)
    question = SurveyQuestionAnswer.objects.filter(question=question_asked, task_given=fabrication_task).exists()
    return question
