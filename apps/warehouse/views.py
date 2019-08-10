from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.engineering.models import Project
from apps.warehouse.models import Warehouse, Stock, StockRelease
from apps.warehouse.serializers import WarehouseSerializer, StockSerializer, CreateStockSerializer, \
    CreateStockReleaseSerializer, StockReleaseSerializer


class StockItemsView(LoginRequiredMixin, View):
    template_name = 'logistics/warehouse/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])

        self.context['project'] = project
        return render(request, self.template_name, self.context)


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()

    def get_queryset(self):
        warehouse = get_object_or_404(Warehouse, slug=self.request.GET.get('warehouse'))
        return Stock.objects.filter(warehouse=warehouse)

    serializer_class = StockSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class CreateStockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = CreateStockSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class StockReleaseViewSet(viewsets.ModelViewSet):
    queryset = StockRelease.objects.all()

    def get_queryset(self):
        warehouse = get_object_or_404(Warehouse, slug=self.request.GET.get('warehouse'))
        return StockRelease.objects.filter(warehouse=warehouse)

    serializer_class = StockReleaseSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class CreateStockReleaseViewSet(viewsets.ModelViewSet):
    queryset = StockRelease.objects.all()
    serializer_class = CreateStockReleaseSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class StockFormViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        warehouse = get_object_or_404(Warehouse, slug=self.request.GET.get('warehouse'))
        stocks = Stock.objects.filter(warehouse=warehouse)

        stocks_obj = []
        for stock in stocks:
            stock_object = {'value': stock.id, 'label': stock.name}
            stocks_obj.append(stock_object)

        return Response({'results': stocks_obj})
