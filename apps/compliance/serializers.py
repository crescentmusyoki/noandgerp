from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.compliance.models import Survey, SurveyQuestion, SurveyQuestionAnswer, HelpIssue
from apps.engineering.serializers import ProjectSerializer
from apps.users.serializers import UserSerializer


class SurveySerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Survey
        fields = "__all__"


class CreateSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = "__all__"


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = "__all__"


class SurveyQuestionAnswerSerializer(serializers.ModelSerializer):
    question = SurveyQuestionSerializer()

    class Meta:
        model = SurveyQuestionAnswer
        fields = "__all__"


class CreateSurveyQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestionAnswer
        fields = "__all__"

    def validate(self, data):
        return data

    def create(self, validated_data):
        question = validated_data['question']
        # question = get_object_or_404(SurveyQuestion, id=question_id)
        question.status = True
        question.save()

        print(question)

        answer = super().create(validated_data)

        return answer


class HelpSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer()
    assigned_by = UserSerializer()
    created_by = UserSerializer()

    class Meta:
        model = HelpIssue
        fields = "__all__"


class CreateHelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpIssue
        fields = "__all__"
