from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.logistics import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'create/project', views.CreateProjectViewSet)
router.register(r'bids', views.ProjectBidViewSet)
router.register(r'create/bid', views.CreateProjectBidViewSet)
router.register(r'quotes', views.ProjectQuoteViewSet)
router.register(r'create/quote', views.CreateProjectQuoteViewSet)
router.register(r'quoteitems', views.ProjectQuoteItemViewSet)
router.register(r'create/quoteitem', views.CreateProjectQuoteItemViewSet)

urlpatterns = [
    path('logistics/directory/', views.LogisticsView.as_view(), name='logistics_directory'),
    path('logistics/logistic/<slug>/overview/', views.LogisticView.as_view(), name='logistic_overview'),
    path('logistics/logistic/<slug>/bidding/', views.LogisticsBiddingView.as_view(), name='logistic_bidding'),
    path('logistics/logistic/<slug>/bidding/status/', views.LogisticsBiddingEditView.as_view(),
         name='logistic_bidding_status'),
    path('logistics/logistic/<slug>/bidding/status/<bid_slug>/<bid_action>/', views.LogisticsBidStatusView.as_view(),
         name='logistic_bid_status'),
    path('logistics/logistic/<slug>/quotation/', views.LogisticsQuotationView.as_view(), name='logistic_quotation'),
    path('logistics/logistic/<slug>/quotation/new/<quote_item_slug>/', views.LogisticsQuotationItemNewView.as_view(),
         name='logistic_quotation_edit'),
    path('logistics/logistic/<slug>/quotation/status/<quote_item_slug>/<quote_item_action>/',
         views.LogisticsQuotationItemStatusView.as_view(),
         name='logistic_quotation_status'),
    path('logistics/logistic/<slug>/warehouse/', views.LogisticsWarehouseView.as_view(), name='logistic_warehouse'),

    path('api/v1/logistics/forms/equipments/', views.ProjectEquipmentsViewSet.as_view()),
    path('api/v1/logistics/', include(router.urls)),
]
