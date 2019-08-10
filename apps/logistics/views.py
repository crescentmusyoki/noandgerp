from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.engineering.models import Project, ProjectEquipment
from apps.engineering.serializers import CreateProjectSerializer, ProjectSerializer
from apps.logistics.models import LogisticsBid, LogisticsQuote, LogisticsQuoteItem
from apps.logistics.serializers import CreateProjectBidSerializer, ProjectBidSerializer, CreateProjectQuoteSerializer, \
    ProjectQuoteSerializer, ProjectQuoteItemSerializer, CreateProjectQuoteItemSerializer
from apps.warehouse.models import Stock
from configs import BID_STATUS


class LogisticsView(LoginRequiredMixin, View):
    template_name = 'logistics/index.html'
    context = {}

    @method_decorator(permission_required('logistics.view_project'))
    def get(self, request):
        self.context['projects'] = Project.objects.all()

        return render(request, self.template_name, self.context)


class LogisticView(LoginRequiredMixin, View):
    template_name = 'logistics/project.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])

        self.context['project'] = project

        #  return render(request, self.template_name, self.context)
        return redirect(reverse('logistic_bidding', kwargs={'slug': project.slug}))


class LogisticsBiddingView(LoginRequiredMixin, View):
    template_name = 'logistics/bidding/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_bids = LogisticsBid.objects.filter(project=project)

        self.context['project'] = project
        self.context['project_bids'] = project_bids

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_bid = LogisticsBid()
        project_bid.project = project
        project_bid.vendor = request.user
        project_bid.save()

        messages.success(request, 'Bid successfully submitted.')
        return redirect(reverse('logistic_bidding', kwargs={'slug': project.slug}))


class LogisticsBiddingEditView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project.logistics_bidding = not project.logistics_bidding
        project.save()

        messages.success(request, 'Project logistics bidding updated successfully.')

        return redirect(reverse('logistic_bidding', kwargs={'slug': project.slug}))


class LogisticsBidStatusView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        bid = get_object_or_404(LogisticsBid, slug=kwargs['bid_slug'])
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
            return redirect(reverse('logistics_bidding', kwargs={'slug': project.slug}))

        return redirect(reverse('logistic_bidding', kwargs={'slug': project.slug}))


class LogisticsQuotationView(LoginRequiredMixin, View):
    template_name = 'logistics/quotation/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_bid = LogisticsBid.objects.filter(project=project, vendor=request.user)
        if project_bid.exists():
            bid_placed = True
            bid = LogisticsBid.objects.get(project=project, vendor=request.user)
        else:
            bid_placed = False
            bid = []

        self.context['project'] = project
        self.context['bid_placed'] = bid_placed
        self.context['bid'] = bid
        self.context['project_equipments'] = LogisticsQuoteItem.objects.filter(project=project)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])

        project_bids = LogisticsBid.objects.filter(project=project, bid_status=BID_STATUS[1][0])

        if LogisticsQuote.objects.filter(project=project).exists():
            quote = LogisticsQuote.objects.get(project=project)
        else:
            quote = LogisticsQuote()
            quote.project = project
            quote.save()

        for project_bid in project_bids:
            equipments = ProjectEquipment.objects.filter(project=project)

            for equipment in equipments:
                if not LogisticsQuoteItem.objects.filter(project=project, vendor=project_bid.vendor).exists():
                    quote_item = LogisticsQuoteItem()
                    quote_item.project = project
                    quote_item.quote = quote
                    quote_item.vendor = project_bid.vendor
                    quote_item.equipment = equipment
                    quote_item.save()

        messages.success(request, 'Request for quotation successfully updated.')
        return redirect(reverse('logistic_quotation', kwargs={'slug': project.slug}))


class LogisticsQuotationItemNewView(LoginRequiredMixin, View):
    context = {}

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        quote_item = get_object_or_404(LogisticsQuoteItem, slug=kwargs['quote_item_slug'])

        price = request.POST.get('price')

        quote_item.project = project
        quote_item.quote_price = price
        quote_item.save()

        messages.success(request, 'Quote updated successfully.')

        return redirect(reverse('logistic_quotation', kwargs={'slug': project.slug}))


class LogisticsQuotationItemStatusView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        quote_item = get_object_or_404(LogisticsQuoteItem, slug=kwargs['quote_item_slug'])
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
            return redirect(reverse('logistic_quotation', kwargs={'slug': project.slug}))

        return redirect(reverse('logistic_quotation', kwargs={'slug': project.slug}))


class LogisticsWarehouseView(LoginRequiredMixin, View):
    template_name = 'logistics/warehouse/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_stock = Stock.objects.filter(project=project)

        self.context['project'] = project
        self.context['project_stocks'] = project_stock

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_bid = LogisticsBid()
        project_bid.project = project
        project_bid.vendor = request.user
        project_bid.save()

        messages.success(request, 'Bid successfully submitted.')
        return redirect(reverse('logistic_bidding', kwargs={'slug': project.slug}))


class UsersView(LoginRequiredMixin, View):
    template_name = 'users/index.html'
    context = {}

    def get(self, request):
        self.context['users'] = User.objects.all()
        return render(request, self.template_name, self.context)


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
        else:
            return self.queryset


class CreateProjectBidViewSet(viewsets.ModelViewSet):
    queryset = LogisticsBid.objects.all()
    serializer_class = CreateProjectBidSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectBidViewSet(viewsets.ModelViewSet):
    queryset = LogisticsBid.objects.all()
    serializer_class = ProjectBidSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return LogisticsBid.objects.filter(vendor=self.request.user, project=project)
        else:
            return self.queryset


class CreateProjectQuoteViewSet(viewsets.ModelViewSet):
    queryset = LogisticsQuote.objects.all()
    serializer_class = CreateProjectQuoteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectQuoteViewSet(viewsets.ModelViewSet):
    queryset = LogisticsQuote.objects.all()
    serializer_class = ProjectQuoteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return LogisticsQuote.objects.filter(vendor=self.request.user, project=project)
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
    queryset = LogisticsQuoteItem.objects.all()
    serializer_class = ProjectQuoteItemSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return LogisticsQuoteItem.objects.filter(vendor=self.request.user, project=project)
        elif self.request.GET.get('item'):
            if self.request.GET.get('item') == '':
                return []
            else:
                equipment = get_object_or_404(ProjectEquipment, id=self.request.GET.get('item'))
                return LogisticsQuoteItem.objects.filter(project=project, equipment=equipment)
        elif self.request.GET.get('vendor'):
            vendor = get_object_or_404(User, id=self.request.GET.get('vendor'))
            return LogisticsQuoteItem.objects.filter(project=project, vendor=vendor)
        else:
            return self.queryset


class CreateProjectQuoteItemViewSet(viewsets.ModelViewSet):
    queryset = LogisticsQuoteItem.objects.all()
    serializer_class = CreateProjectQuoteItemSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'
