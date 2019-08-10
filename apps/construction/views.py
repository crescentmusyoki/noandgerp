from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from apps.construction.models import Civil, Commission
from apps.construction.serializers import CivilSerializer, CreateCivilSerializer, CommissionSerializer, \
    CreateCommissionSerializer


class CivilViewSet(viewsets.ModelViewSet):
    queryset = Civil.objects.all()
    serializer_class = CivilSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset


class CreateCivilViewSet(viewsets.ModelViewSet):
    queryset = Civil.objects.all()
    serializer_class = CreateCivilSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class CommissionViewSet(viewsets.ModelViewSet):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset


class CreateCommissionViewSet(viewsets.ModelViewSet):
    queryset = Commission.objects.all()
    serializer_class = CreateCommissionSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'
