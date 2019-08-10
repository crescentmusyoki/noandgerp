from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.compliance import views

router = DefaultRouter()
router.register(r'surveys', views.SurveyViewSet)
router.register(r'create/survey', views.CreateSurveyViewSet)
router.register(r'questions', views.SurveyQuestionViewSet)
router.register(r'answers', views.SurveyQuestionAnswerViewSet)
router.register(r'create/answer', views.CreateSurveyQuestionAnswerViewSet)
router.register(r'help', views.HelpViewSet)
router.register(r'create/help', views.CreateHelpViewSet)

urlpatterns = [

    path('compliance/directory/', views.SurveysView.as_view(), name='surveys_directory'),
    path('compliance/directory/<slug>/overview/', views.SurveyView.as_view(), name='survey_overview'),
    path('compliance/directory/<slug>/delete/', views.SurveyDeleteView.as_view(), name='survey_delete'),
    path('compliance/directory/<slug>/questions/', views.SurveyQuestionsView.as_view(), name='survey_questions'),
    path('compliance/directory/<slug>/delete/<question_slug>/', views.SurveyQuestionDeleteView.as_view(),
         name='survey_question_delete'),

    path('api/v1/compliance/', include(router.urls))
]
