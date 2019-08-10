from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.compliance.models import Survey, SurveyQuestion, SurveyQuestionAnswer
from apps.engineering.forms import ProjectForm, ProjectFileForm, ProjectDesignForm, ProjectEquipmentForm, \
    ProjectFabricationForm
from apps.engineering.models import Project, ProjectFile, ProjectEquipment, ProjectBudget, ProjectBid, ProjectQuote, \
    ProjectQuoteItem, ProjectDesign, ProjectFabrication, ProjectStage
from apps.engineering.serializers import CreateProjectSerializer, ProjectSerializer, CreateProjectFileSerializer, \
    ProjectFileSerializer, CreateProjectEquipmentSerializer, ProjectEquipmentSerializer, CreateProjectBudgetSerializer, \
    ProjectBudgetSerializer, ProjectBidSerializer, CreateProjectBidSerializer, CreateProjectQuoteSerializer, \
    ProjectQuoteSerializer, CreateProjectQuoteItemSerializer, ProjectQuoteItemSerializer, ProjectDesignSerializer, \
    CreateProjectDesignSerializer, ProjectFabricationSerializer, CreateProjectFabricationSerializer, \
    ProjectStageSerializer
from configs import day_min, day_max, daterange, BID_STATUS, SURVEY_TYPE


class ProjectsView(LoginRequiredMixin, View):
    template_name = 'engineering/index.html'
    context = {}

    def get(self, request):
        project_form = ProjectForm

        self.context['projects'] = Project.objects.all()
        self.context['form'] = project_form

        return render(request, self.template_name, self.context)

    def post(self, request):
        project_form = ProjectForm(request.POST)

        if project_form.is_valid():
            project = project_form.save(commit=True)
            messages.success(request, 'Project successfully created.')
            return redirect(reverse('projects_directory'))

        else:
            messages.warning(request, project_form.errors)
            self.context['profile_form'] = project_form
            return render(request, self.template_name, self.context)


class ProjectView(LoginRequiredMixin, View):
    template_name = 'engineering/project.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_form = ProjectForm(instance=project)

        self.context['project'] = project
        self.context['form'] = project_form
        self.context['history'] = project.history.all()

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_form = ProjectForm(request.POST, instance=project)

        if project_form.is_valid():
            project = project_form.save(commit=True)
            messages.success(request, 'Changes successfully saved.')
            return redirect(reverse('project_overview', kwargs={'slug': project.slug}))

        else:
            messages.warning(request, project_form.errors)
            self.context['profile_form'] = project_form
            return render(request, self.template_name, self.context)


class ProjectFilesView(LoginRequiredMixin, View):
    template_name = 'engineering/files/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_files = ProjectFile.objects.filter(project=project)
        project_file_form = ProjectFileForm

        self.context['project'] = project
        self.context['project_files'] = project_files
        self.context['form'] = project_file_form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_file_form = ProjectFileForm(request.POST, request.FILES)

        if project_file_form.is_valid():
            project_data = project_file_form.save(commit=False)
            project_data.project = project
            project_data.save()

            messages.success(request, 'Document successfully uploaded.')
            return redirect(reverse('project_documents', kwargs={'slug': project.slug}))

        else:
            messages.warning(request, project_file_form.errors)
            self.context['form'] = project_file_form
            return render(request, self.template_name, self.context)


class ProjectFileDeleteView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_file = get_object_or_404(ProjectFile, slug=kwargs['file_slug'])
        project_file.delete()

        messages.success(request, 'Document deleted successfully.')

        return redirect(reverse('project_documents', kwargs={'slug': project.slug}))


class ProjectDesignsView(LoginRequiredMixin, View):
    template_name = 'engineering/designs/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_designs = ProjectDesign.objects.filter(project=project)
        project_design_form = ProjectDesignForm

        self.context['project'] = project
        self.context['project_designs'] = project_designs
        self.context['form'] = project_design_form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_design_form = ProjectDesignForm(request.POST, request.FILES)

        if project_design_form.is_valid():
            project_data = project_design_form.save(commit=False)
            project_data.project = project
            project_data.save()

            messages.success(request, 'Design successfully uploaded.')
            return redirect(reverse('project_designs', kwargs={'slug': project.slug}))

        else:
            messages.warning(request, project_design_form.errors)
            self.context['form'] = project_design_form
            return render(request, self.template_name, self.context)


class ProjectDesignDeleteView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_design = get_object_or_404(ProjectDesign, slug=kwargs['file_slug'])
        project_design.delete()

        messages.success(request, 'Design deleted successfully.')

        return redirect(reverse('project_designs', kwargs={'slug': project.slug}))


class ProjectEquipmentsView(LoginRequiredMixin, View):
    template_name = 'engineering/equipments/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_equipments = ProjectEquipment.objects.filter(project=project)
        project_equipment_form = ProjectEquipmentForm

        self.context['project'] = project
        self.context['project_equipments'] = project_equipments
        self.context['form'] = project_equipment_form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_equipment_form = ProjectEquipmentForm(request.POST)

        if project_equipment_form.is_valid():
            project_data = project_equipment_form.save(commit=False)
            project_data.project = project
            project_data.save()

            messages.success(request, 'Equipment successfully created.')
            return redirect(reverse('project_equipments', kwargs={'slug': project.slug}))

        else:
            messages.warning(request, project_equipment_form.errors)
            self.context['form'] = project_equipment_form
            return render(request, self.template_name, self.context)


class ProjectEquipmentDeleteView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_equipment = get_object_or_404(ProjectEquipment, slug=kwargs['file_slug'])
        project_equipment.delete()

        messages.success(request, 'Equipments deleted successfully.')

        return redirect(reverse('project_equipments', kwargs={'slug': project.slug}))


class ProjectEquipmentView(LoginRequiredMixin, View):
    template_name = 'engineering/equipments/edit.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_equipment = get_object_or_404(ProjectEquipment, slug=kwargs['equipment_slug'])
        project_equipment_form = ProjectEquipmentForm(instance=project_equipment)

        self.context['project'] = project
        self.context['project_equipment'] = project_equipment
        self.context['form'] = project_equipment_form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_equipment = get_object_or_404(ProjectEquipment, slug=kwargs['equipment_slug'])
        project_equipment_form = ProjectEquipmentForm(request.POST, instance=project_equipment)

        if project_equipment_form.is_valid():
            project_data = project_equipment_form.save(commit=False)
            project_data.project = project
            project_data.save()

            messages.success(request, 'Changes successfully saved.')
            return redirect(reverse('project_equipment_edit',
                                    kwargs={'slug': project.slug, 'equipment_slug': project_equipment.slug}))

        else:
            messages.warning(request, project_equipment_form.errors)
            self.context['form'] = project_equipment_form

            return render(request, self.template_name, self.context)


class ProjectBiddingView(LoginRequiredMixin, View):
    template_name = 'engineering/bidding/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_bids = ProjectBid.objects.filter(project=project)

        self.context['project'] = project
        self.context['project_bids'] = project_bids

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_bid = ProjectBid()
        project_bid.project = project
        project_bid.vendor = request.user
        project_bid.save()

        messages.success(request, 'Bid successfully submitted.')
        return redirect(reverse('project_bidding', kwargs={'slug': project.slug}))


class ProjectBiddingEditView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project.bidding = not project.bidding
        project.save()

        messages.success(request, 'Project bidding updated successfully.')

        return redirect(reverse('project_bidding', kwargs={'slug': project.slug}))


class ProjectBidStatusView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        bid = get_object_or_404(ProjectBid, slug=kwargs['bid_slug'])
        bid_action = kwargs['bid_action']

        if bid_action == 'accept':
            bid.bid_status = 'Accepted'
            bid.save()
            messages.success(request, 'Bid status updated successfully.')
        elif bid_action == 'deny':
            bid.bid_status = 'Denied'
            bid.save()
            messages.success(request, 'Bid status updated successfully.')
        elif bid_action == 'delete':
            bid.delete()
            messages.success(request, 'Bid deleted successfully.')
        else:
            return redirect(reverse('project_bidding', kwargs={'slug': project.slug}))

        return redirect(reverse('project_bidding', kwargs={'slug': project.slug}))


class ProjectQuotationView(LoginRequiredMixin, View):
    template_name = 'engineering/quotation/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_bid = ProjectBid.objects.filter(project=project, vendor=request.user)
        if project_bid.exists():
            bid_placed = True
            bid = ProjectBid.objects.get(project=project, vendor=request.user)
        else:
            bid_placed = False
            bid = []

        self.context['project'] = project
        self.context['bid_placed'] = bid_placed
        self.context['bid'] = bid
        self.context['project_equipments'] = ProjectQuoteItem.objects.filter(project=project)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])

        project_bids = ProjectBid.objects.filter(project=project, bid_status=BID_STATUS[1][0])

        if ProjectQuote.objects.filter(project=project).exists():
            quote = ProjectQuote.objects.get(project=project)
        else:
            quote = ProjectQuote()
            quote.project = project
            quote.save()

        for project_bid in project_bids:
            equipments = ProjectEquipment.objects.filter(project=project)

            for equipment in equipments:
                if not ProjectQuoteItem.objects.filter(project=project, vendor=project_bid.vendor).exists():
                    quote_item = ProjectQuoteItem()
                    quote_item.project = project
                    quote_item.quote = quote
                    quote_item.vendor = project_bid.vendor
                    quote_item.equipment = equipment
                    quote_item.save()

        messages.success(request, 'Request for quotation successfully updated.')
        return redirect(reverse('project_quotation', kwargs={'slug': project.slug}))


class ProjectQuotationItemNewView(LoginRequiredMixin, View):
    context = {}

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        quote_item = get_object_or_404(ProjectQuoteItem, slug=kwargs['quote_item_slug'])

        price = request.POST.get('price')

        quote_item.project = project
        quote_item.quote_price = price
        quote_item.save()

        messages.success(request, 'Quote updated successfully.')

        return redirect(reverse('project_quotation', kwargs={'slug': project.slug}))


class ProjectQuotationItemStatusView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        quote_item = get_object_or_404(ProjectQuoteItem, slug=kwargs['quote_item_slug'])
        quote_item_action = kwargs['quote_item_action']

        if quote_item_action == 'accept':
            quote_item.quote_status = 'Accepted'
            quote_item.save()
            messages.success(request, 'Quote status updated successfully.')
        elif quote_item_action == 'deny':
            quote_item.quote_status = 'Denied'
            quote_item.save()
            messages.success(request, 'Quote status updated successfully.')
        elif quote_item_action == 'delete':
            quote_item.delete()
            messages.success(request, 'Quote deleted successfully.')
        else:
            return redirect(reverse('project_quotation', kwargs={'slug': project.slug}))

        return redirect(reverse('project_quotation', kwargs={'slug': project.slug}))


class ProjectFabricationView(LoginRequiredMixin, View):
    template_name = 'engineering/fabrication/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_tasks = ProjectFabrication.objects.filter(project=project)
        project_fabrication_form = ProjectFabricationForm

        self.context['project'] = project
        self.context['project_tasks'] = project_tasks
        self.context['form'] = project_fabrication_form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_fabrication_form = ProjectFabricationForm(request.POST)

        if project_fabrication_form.is_valid():
            project_data = project_fabrication_form.save(commit=False)
            project_data.project = project
            project_data.save()

            messages.success(request, 'Task successfully created.')
            return redirect(reverse('project_fabrication', kwargs={'slug': project.slug}))

        else:
            messages.warning(request, project_fabrication_form.errors)
            self.context['form'] = project_fabrication_form
            return render(request, self.template_name, self.context)


class ProjectFabricationClearView(LoginRequiredMixin, View):
    template_name = 'engineering/fabrication/edit.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_task = get_object_or_404(ProjectFabrication, slug=kwargs['task_slug'])
        project_fabrication_form = ProjectFabricationForm

        if Survey.objects.filter(project=project, survey_type=SURVEY_TYPE[1][1]).exists():
            survey = Survey.objects.get(project=project, survey_type=SURVEY_TYPE[1][1])
            survey_questions = SurveyQuestion.objects.filter(survey=survey)
        else:
            survey = None
            survey_questions = None

        survey_complete = True
        for survey_question in survey_questions:
            question_answered = SurveyQuestionAnswer.objects.filter(question=survey_question,
                                                                    task_given=project_task).exists()
            if question_answered:
                pass
            else:
                survey_complete = False

        self.context['project'] = project
        self.context['project_task'] = project_task
        self.context['form'] = project_fabrication_form
        self.context['survey'] = survey
        self.context['survey_questions'] = survey_questions
        self.context['survey_complete'] = survey_complete

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_task = get_object_or_404(ProjectFabrication, slug=kwargs['task_slug'])

        question = request.POST.get('question')
        answer = request.POST.get('answer')

        if question != "" and answer != "":
            survey_answer = SurveyQuestionAnswer()
            survey_answer.task_given = project_task
            survey_answer.question = get_object_or_404(SurveyQuestion, id=question)
            survey_answer.answer = answer
            survey_answer.save()

            messages.success(request, 'Question answered successfully.')
            return redirect(
                reverse('project_fabrication_clear', kwargs={'slug': project.slug, 'task_slug': project_task.slug}))

        else:
            messages.warning(request, 'Check your answer.')
            return render(request, self.template_name, self.context)


class ProjectFabricationStatusView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        fabrication = get_object_or_404(ProjectFabrication, slug=kwargs['fabrication_slug'])
        fabrication_action = kwargs['fabrication_action']

        if fabrication_action == 'complete':
            fabrication.fabrication_status = 'Complete'
            fabrication.save()
            messages.success(request, 'Task marked as complete successfully.')
        elif fabrication_action == 'canceled':
            fabrication.fabrication_status = 'Canceled'
            fabrication.save()
            messages.success(request, 'Task marked as canceled successfully.')
        elif fabrication_action == 'delete':
            fabrication.delete()
            messages.success(request, 'Task deleted successfully.')
        else:
            return redirect(reverse('project_fabrication', kwargs={'slug': project.slug}))

        return redirect(reverse('project_fabrication', kwargs={'slug': project.slug}))


class CreateProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = CreateProjectSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        elif self.request.GET.get('start_date') and self.request.GET.get('end_date'):

            start_date = datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d')

            return self.queryset.filter(
                created_at__range=[day_min(start_date.strftime("%Y-%m-%d")), day_max(end_date.strftime("%Y-%m-%d"))])
        else:
            return self.queryset


class ProjectStageViewSet(viewsets.ModelViewSet):
    queryset = ProjectStage.objects.all()

    def get_queryset(self):
        if self.request.GET.get('project'):
            project = get_object_or_404(Project, slug=self.request.GET.get('project'))
            return ProjectStage.objects.filter(project=project)
        else:
            return self.queryset

    serializer_class = ProjectStageSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectLeadsViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_leads = User.objects.filter(groups__name='Project Lead')

        leads = []
        for lead in all_leads:
            lead_object = {'value': lead.id, 'label': lead.first_name + ' ' + lead.last_name}

            # append groups
            leads.append(lead_object)

        return Response({'results': leads})


class CreateProjectFileViewSet(viewsets.ModelViewSet):
    queryset = ProjectFile.objects.all()
    serializer_class = CreateProjectFileSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectFileViewSet(viewsets.ModelViewSet):
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset


class CreateProjectDesignViewSet(viewsets.ModelViewSet):
    queryset = ProjectDesign.objects.all()
    serializer_class = CreateProjectDesignSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectDesignViewSet(viewsets.ModelViewSet):
    queryset = ProjectDesign.objects.all()
    serializer_class = ProjectDesignSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset


class CreateProjectEquipmentViewSet(viewsets.ModelViewSet):
    queryset = ProjectEquipment.objects.all()
    serializer_class = CreateProjectEquipmentSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectEquipmentViewSet(viewsets.ModelViewSet):
    queryset = ProjectEquipment.objects.all()
    serializer_class = ProjectEquipmentSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        elif self.request.GET.get('start_date') and self.request.GET.get('end_date'):

            start_date = datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d')

            return self.queryset.filter(
                created_at__range=[day_min(start_date.strftime("%Y-%m-%d")), day_max(end_date.strftime("%Y-%m-%d"))])
        else:
            return self.queryset


class CreateProjectBudgetViewSet(viewsets.ModelViewSet):
    queryset = ProjectBudget.objects.all()
    serializer_class = CreateProjectBudgetSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectBudgetViewSet(viewsets.ModelViewSet):
    queryset = ProjectBudget.objects.all()
    serializer_class = ProjectBudgetSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        elif self.request.GET.get('start_date') and self.request.GET.get('end_date'):

            start_date = datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d')

            return self.queryset.filter(
                created_at__range=[day_min(start_date.strftime("%Y-%m-%d")), day_max(end_date.strftime("%Y-%m-%d"))])
        else:
            return self.queryset


class CreateProjectBidViewSet(viewsets.ModelViewSet):
    queryset = ProjectBid.objects.all()
    serializer_class = CreateProjectBidSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectBidViewSet(viewsets.ModelViewSet):
    queryset = ProjectBid.objects.all()
    serializer_class = ProjectBidSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return ProjectBid.objects.filter(vendor=self.request.user, project=project)
        else:
            return self.queryset


class CreateProjectQuoteViewSet(viewsets.ModelViewSet):
    queryset = ProjectQuote.objects.all()
    serializer_class = CreateProjectQuoteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectQuoteViewSet(viewsets.ModelViewSet):
    queryset = ProjectQuote.objects.all()
    serializer_class = ProjectQuoteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return ProjectQuote.objects.filter(vendor=self.request.user, project=project)
        else:
            return self.queryset


class ProjectEquipmentsViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        project = request.GET.get('project')
        project_equipments = ProjectEquipment.objects.filter(project=project)

        equipments = []
        for equipment in project_equipments:
            equipment_object = {'value': equipment.id, 'label': equipment.name}

            equipments.append(equipment_object)

        return Response({'results': equipments})


class ProjectQuoteItemViewSet(viewsets.ModelViewSet):
    queryset = ProjectQuoteItem.objects.all()
    serializer_class = ProjectQuoteItemSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return ProjectQuoteItem.objects.filter(vendor=self.request.user, project=project)
        elif self.request.GET.get('item'):
            if self.request.GET.get('item') == '':
                return []
            else:
                equipment = get_object_or_404(ProjectEquipment, id=self.request.GET.get('item'))
                return ProjectQuoteItem.objects.filter(project=project, equipment=equipment)
        elif self.request.GET.get('vendor'):
            vendor = get_object_or_404(User, id=self.request.GET.get('vendor'))
            return ProjectQuoteItem.objects.filter(project=project, vendor=vendor)
        else:
            return self.queryset


class CreateProjectQuoteItemViewSet(viewsets.ModelViewSet):
    queryset = ProjectQuoteItem.objects.all()
    serializer_class = CreateProjectQuoteItemSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectFabricationViewSet(viewsets.ModelViewSet):
    queryset = ProjectFabrication.objects.all()
    serializer_class = ProjectFabricationSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return ProjectQuoteItem.objects.filter(vendor=self.request.user, project=project)
        elif self.request.GET.get('item'):
            if self.request.GET.get('item') == '':
                return []
            else:
                equipment = get_object_or_404(ProjectEquipment, id=self.request.GET.get('item'))
                return ProjectQuoteItem.objects.filter(project=project, equipment=equipment)
        elif self.request.GET.get('vendor'):
            vendor = get_object_or_404(User, id=self.request.GET.get('vendor'))
            return ProjectQuoteItem.objects.filter(project=project, vendor=vendor)
        else:
            return self.queryset


class CreateProjectFabricationViewSet(viewsets.ModelViewSet):
    queryset = ProjectFabrication.objects.all()
    serializer_class = CreateProjectFabricationSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectTeamViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        all_teams = project.members.all()

        teams = []
        for team in all_teams:
            team_object = {'value': team.id,
                           'label': team.first_name + ' ' + team.last_name}

            # append groups
            teams.append(team_object)

        return Response({'results': teams})


class ProjectFormViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        projects = Project.objects.all()

        projects_obj = []
        for project in projects:
            project_object = {'value': project.id, 'label': project.name}

            projects_obj.append(project_object)

        return Response({'results': projects_obj})
