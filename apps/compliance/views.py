from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from apps.compliance.forms import SurveyForm, SurveyQuestionForm
from apps.compliance.models import Survey, SurveyQuestion, SurveyQuestionAnswer, HelpIssue
from apps.compliance.serializers import SurveySerializer, CreateSurveySerializer, SurveyQuestionSerializer, \
    SurveyQuestionAnswerSerializer, CreateSurveyQuestionAnswerSerializer, HelpSerializer, CreateHelpSerializer
from apps.engineering.models import Project


class SurveysView(LoginRequiredMixin, View):
    template_name = 'compliance/index.html'
    context = {}

    def get(self, request):
        self.context['surveys'] = Survey.objects.all()
        self.context['form'] = SurveyForm

        return render(request, self.template_name, self.context)

    def post(self, request):
        survey_form = SurveyForm(request.POST)

        if survey_form.is_valid():
            survey = survey_form.save(commit=True)
            messages.success(request, 'Survey successfully created.')
            return redirect(reverse('surveys_directory'))

        else:
            messages.warning(request, survey_form.errors)
            self.context['form'] = survey_form
            return render(request, self.template_name, self.context)


class SurveyView(LoginRequiredMixin, View):
    template_name = 'compliance/edit.html'
    context = {}

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, slug=kwargs['slug'])
        self.context['survey'] = survey
        self.context['form'] = SurveyForm(instance=survey)
        self.context['question_form'] = SurveyQuestionForm
        self.context['survey_questions'] = SurveyQuestion.objects.filter(survey=survey)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, slug=kwargs['slug'])
        survey_form = SurveyForm(request.POST, instance=survey)

        if survey_form.is_valid():
            survey = survey_form.save()
            messages.success(request, 'Survey successfully updated.')
            return redirect(reverse('survey_overview', kwargs={'slug': survey.slug}))

        else:
            messages.warning(request, survey_form.errors)
            self.context['form'] = survey_form
            return render(request, self.template_name, self.context)


class SurveyQuestionsView(LoginRequiredMixin, View):
    template_name = 'compliance/edit.html'
    context = {}

    def get(self, request, **kwargs):
        survey = get_object_or_404(Survey, slug=kwargs['slug'])
        self.context['survey'] = survey
        self.context['question_form'] = SurveyQuestionForm

        return render(request, self.template_name, self.context)

    def post(self, request, **kwargs):
        survey = get_object_or_404(Survey, slug=kwargs['slug'])
        survey_question_form = SurveyQuestionForm(request.POST)

        if survey_question_form.is_valid():
            survey_question = survey_question_form.save(commit=False)
            survey_question.survey = survey
            survey_question.save()
            messages.success(request, 'Survey successfully updated.')
            return redirect(reverse('survey_overview', kwargs={'slug': survey.slug}))

        else:
            messages.warning(request, survey_question_form.errors)
            self.context['form'] = survey_question_form
            return render(request, self.template_name, self.context)


class SurveyDeleteView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, slug=kwargs['slug'])
        survey.delete()

        messages.success(request, 'Survey deleted successfully.')

        return redirect(reverse('surveys_directory'))


class SurveyQuestionDeleteView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, slug=kwargs['slug'])
        survey_question = get_object_or_404(SurveyQuestion, slug=kwargs['question_slug'])
        survey_question.delete()

        messages.success(request, 'Survey question deleted successfully.')

        return redirect(reverse('survey_overview', kwargs={'slug': survey.slug}))


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()

    def get_queryset(self):
        if self.request.GET.get('type'):
            return Survey.objects.filter(survey_type=self.request.GET.get('type'))
        else:
            return self.queryset

    serializer_class = SurveySerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class CreateSurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = CreateSurveySerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.all()

    def get_queryset(self):
        if self.request.GET.get('survey'):
            survey = get_object_or_404(Survey, slug=self.request.GET.get('survey'))
            return SurveyQuestion.objects.filter(survey=survey)
        else:
            return self.queryset

    serializer_class = SurveyQuestionSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class SurveyQuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestionAnswer.objects.all()
    serializer_class = SurveyQuestionAnswerSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class CreateSurveyQuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestionAnswer.objects.all()
    serializer_class = CreateSurveyQuestionAnswerSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class HelpViewSet(viewsets.ModelViewSet):
    queryset = HelpIssue.objects.all()
    serializer_class = HelpSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class CreateHelpViewSet(viewsets.ModelViewSet):
    queryset = HelpIssue.objects.all()
    serializer_class = CreateHelpSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'
