from django.urls import path

from apps.general import views

urlpatterns = [
    path('', views.WebView.as_view(), name='home'),
    path('profile/settings', views.Settings.as_view(), name='my_profile'),
    # path('', views.HomeView.as_view(), name='home'),
    path('api/v1/accounts/login/', views.CustomAuthToken.as_view(), name='api_login'),
]
