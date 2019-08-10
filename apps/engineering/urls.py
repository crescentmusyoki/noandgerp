from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.engineering import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'create/project', views.CreateProjectViewSet)
router.register(r'projectstage', views.ProjectStageViewSet)
router.register(r'files', views.ProjectFileViewSet)
router.register(r'create/file', views.CreateProjectFileViewSet)
router.register(r'equipments', views.ProjectEquipmentViewSet)
router.register(r'create/equipment', views.CreateProjectEquipmentViewSet)
router.register(r'budgets', views.ProjectBudgetViewSet)
router.register(r'create/budget', views.CreateProjectBudgetViewSet)
router.register(r'bids', views.ProjectBidViewSet)
router.register(r'create/bid', views.CreateProjectBidViewSet)
router.register(r'quotes', views.ProjectQuoteViewSet)
router.register(r'create/quote', views.CreateProjectQuoteViewSet)
router.register(r'quoteitems', views.ProjectQuoteItemViewSet)
router.register(r'create/quoteitem', views.CreateProjectQuoteItemViewSet)
router.register(r'designs', views.ProjectDesignViewSet)
router.register(r'create/design', views.CreateProjectDesignViewSet)
router.register(r'fabrications', views.ProjectFabricationViewSet)
router.register(r'create/fabrication', views.CreateProjectFabricationViewSet)

urlpatterns = [
    path('engineering/directory/', views.ProjectsView.as_view(), name='projects_directory'),
    path('engineering/project/<slug>/overview/', views.ProjectView.as_view(), name='project_overview'),
    path('engineering/project/<slug>/documents/', views.ProjectFilesView.as_view(), name='project_documents'),
    path('engineering/project/<slug>/documents/<file_slug>/delete/', views.ProjectFileDeleteView.as_view(),
         name='project_document_delete'),
    path('engineering/project/<slug>/designs/', views.ProjectDesignsView.as_view(), name='project_designs'),
    path('engineering/project/<slug>/designs/<file_slug>/delete/', views.ProjectDesignDeleteView.as_view(),
         name='project_design_delete'),
    path('engineering/project/<slug>/equipments/', views.ProjectEquipmentsView.as_view(), name='project_equipments'),
    path('engineering/project/<slug>/equipments/<file_slug>/delete/', views.ProjectEquipmentDeleteView.as_view(),
         name='project_equipment_delete'),
    path('engineering/project/<slug>/equipments/<equipment_slug>/edit/', views.ProjectEquipmentView.as_view(),
         name='project_equipment_edit'),
    path('engineering/project/<slug>/bidding/', views.ProjectBiddingView.as_view(), name='project_bidding'),
    path('engineering/project/<slug>/bidding/status/', views.ProjectBiddingEditView.as_view(),
         name='project_bidding_status'),
    path('engineering/project/<slug>/bidding/status/<bid_slug>/<bid_action>/', views.ProjectBidStatusView.as_view(),
         name='project_bid_status'),
    path('engineering/project/<slug>/quotation/', views.ProjectQuotationView.as_view(), name='project_quotation'),
    path('engineering/project/<slug>/quotation/new/<quote_item_slug>/', views.ProjectQuotationItemNewView.as_view(),
         name='project_quotation_edit'),
    path('engineering/project/<slug>/quotation/status/<quote_item_slug>/<quote_item_action>/',
         views.ProjectQuotationItemStatusView.as_view(),
         name='project_quotation_status'),
    path('engineering/project/<slug>/fabrication/', views.ProjectFabricationView.as_view(), name='project_fabrication'),
    path('engineering/project/<slug>/fabrication/<task_slug>/clear/', views.ProjectFabricationClearView.as_view(),
         name='project_fabrication_clear'),
    path('engineering/project/<slug>/fabrication/status/<fabrication_slug>/<fabrication_action>/',
         views.ProjectFabricationStatusView.as_view(),
         name='project_fabrication_status'),

    path('api/v1/engineering/forms/leads/', views.ProjectLeadsViewSet.as_view()),
    path('api/v1/engineering/forms/teams/', views.ProjectTeamViewSet.as_view()),
    path('api/v1/engineering/forms/equipments/', views.ProjectEquipmentsViewSet.as_view()),
    path('api/v1/engineering/forms/projects/', views.ProjectFormViewSet.as_view()),
    path('api/v1/engineering/', include(router.urls)),
]
