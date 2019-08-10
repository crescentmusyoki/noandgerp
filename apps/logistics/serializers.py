from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.engineering.models import Project, ProjectFile, ProjectEquipment, ProjectBudget, ProjectBid, ProjectQuote, \
    ProjectQuoteItem, ProjectDesign, ProjectFabrication
from apps.logistics.models import LogisticsBid, LogisticsQuote, LogisticsQuoteItem
from apps.users.serializers import UserSerializer
from configs import BID_STATUS, QUOTE_STATUS


class ProjectSerializer(serializers.ModelSerializer):
    lead = UserSerializer()
    members = UserSerializer(many=True)

    class Meta:
        model = Project
        fields = "__all__"


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectEquipmentSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = ProjectEquipment
        fields = "__all__"


class CreateProjectEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEquipment
        fields = "__all__"


class ProjectBudgetSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = ProjectBudget
        fields = "__all__"


class CreateProjectBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBudget
        fields = "__all__"


class ProjectBidSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    vendor = UserSerializer()

    class Meta:
        model = LogisticsBid
        fields = "__all__"


class CreateProjectBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsBid
        fields = "__all__"

    def validate(self, data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        project = data.get('project')

        if LogisticsBid.objects.filter(vendor=user, project=project).exists():
            raise ValidationError('You have already submitted your bid.')

        valid_data = {
            'project': data.get('project'),
            'vendor': data.get('vendor'),
            'bid_status': data.get('bid_status'),
            'rfq': data.get('rfq')
        }

        return valid_data


class ProjectQuoteSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = LogisticsQuote
        fields = "__all__"


class CreateProjectQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsQuote
        fields = "__all__"

    def validate(self, data):

        # if ProjectQuote.objects.filter(project=data.get('project')).exists():
        #     raise ValidationError('RFQ already submitted for this project.')

        valid_data = {
            'project': data.get('project')
        }

        return valid_data

    def create(self, validated_data):
        project = validated_data['project']
        project_bids = LogisticsBid.objects.filter(project=project, bid_status=BID_STATUS[1][0])

        if LogisticsQuote.objects.filter(project=project).exists():
            quote = LogisticsQuote.objects.get(project=project)
        else:
            quote = super().create(validated_data)

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

        return quote

    def update(self, instance, validated_data):
        instance.save()

        return instance


class ProjectQuoteItemSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    quote = ProjectQuoteSerializer()
    vendor = UserSerializer()
    equipment = ProjectEquipmentSerializer()

    class Meta:
        model = LogisticsQuoteItem
        fields = "__all__"


class CreateProjectQuoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsQuoteItem
        fields = "__all__"

    def validate(self, data):
        if not LogisticsQuoteItem.objects.filter(project=data.get('project'), quote=data.get('quote'),
                                                 vendor=data.get('vendor'), equipment=data.get('equipment'),
                                                 quote_status=QUOTE_STATUS[0][0]).exists():
            raise ValidationError('You are not allowed to edit your quote at this time.')

        return data
