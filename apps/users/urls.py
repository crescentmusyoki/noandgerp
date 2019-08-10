from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users import views

router = DefaultRouter()
router.register(r'list', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'create/group', views.CreateGroupViewSet)
router.register(r'create/employee', views.CreateUserViewSet)

urlpatterns = [
    path('users/directory/', views.UsersView.as_view(), name='users_directory'),
    path('users/directory/<id>/', views.UserView.as_view(), name='user_view'),
    path('users/directory/<id>/<user_action>/', views.UserDeleteView.as_view(), name='user_directory_delete'),
    path('users/roles/', views.RolesView.as_view(), name='users_roles'),
    path('users/roles/<id>', views.RoleView.as_view(), name='users_role'),
    path('users/roles/<id>/<group_action>/', views.RoleDeleteView.as_view(), name='users_role_delete'),
    path('api/v1/users/permissions/', views.PermissionViewSet.as_view()),
    path('api/v1/users/forms/groups/', views.GroupsViewSet.as_view()),
    path('api/v1/users/forms/users/', views.UsersOptionViewSet.as_view()),
    path('api/v1/users/remove/user/', views.DeleteGroupUserViewSet.as_view()),
    path('api/v1/users/', include(router.urls))
]
