from rest_framework import serializers

from apps.construction.models import Civil, Commission
from apps.engineering.serializers import ProjectSerializer
from apps.users.serializers import UserSerializer


class CivilSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer()
    assigned_by = UserSerializer()
    cleared_by = UserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = Civil
        fields = "__all__"


class CreateCivilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Civil
        fields = "__all__"


class CommissionSerializer(serializers.ModelSerializer):
    client = UserSerializer()
    commissioned_by = UserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = Commission
        fields = "__all__"


class CreateCommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = "__all__"
