from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.forms import GroupForm, UserForm
from apps.users.models import AllowedPermission
from apps.users.serializers import GroupSerializer, PermissionSerializer, UserSerializer, CreateGroupSerializer, \
    CreateUserSerializer


class UsersView(LoginRequiredMixin, View):
    template_name = 'users/index.html'
    context = {}

    def get(self, request):
        form = UserForm

        self.context['form'] = form
        self.context['users'] = User.objects.all()
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(request.POST.get('password'))
            new_user.save()

            messages.success(request, 'User successfully created.')
            return redirect(reverse('users_directory'))
        else:
            self.context['form'] = form
            messages.error(request, form.errors)
            return render(request, self.template_name, self.context)


class UserView(LoginRequiredMixin, View):
    template_name = 'users/edit_users.html'
    context = {}

    def get(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs['id'])
        form = UserForm(instance=user)

        self.context['form'] = form
        self.context['user'] = user
        return render(request, self.template_name, self.context)

    def post(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs['id'])
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(request.POST.get('password'))
            new_user.save()
            messages.success(request, 'User successfully updated.')
            return redirect(reverse('user_view', kwargs={'id': user.id}))
        else:
            self.context['form'] = form
            messages.error(request, form.errors)
            return render(request, self.template_name, self.context)


class UserDeleteView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs['id'])
        user_action = kwargs['user_action']
        if user_action == 'delete':
            user.delete()
            messages.success(request, 'User successfully deleted.')
        return redirect(reverse('users_directory'))


class RolesView(LoginRequiredMixin, View):
    template_name = 'users/roles.html'
    context = {}

    def get(self, request):
        form = GroupForm

        self.context['form'] = form
        self.context['groups'] = Group.objects.all()
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = GroupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'User role successfully created.')
            return redirect(reverse('users_roles'))
        else:
            self.context['form'] = form
            messages.error(request, form.errors)
            return render(request, self.template_name, self.context)


class RoleView(LoginRequiredMixin, View):
    template_name = 'users/edit_roles.html'
    context = {}

    def get(self, request, **kwargs):
        group = get_object_or_404(Group, id=kwargs['id'])
        form = GroupForm(instance=group)

        self.context['form'] = form
        self.context['group'] = group
        return render(request, self.template_name, self.context)

    def post(self, request, **kwargs):
        group = get_object_or_404(Group, id=kwargs['id'])
        form = GroupForm(request.POST, instance=group)

        if form.is_valid():
            form.save()
            messages.success(request, 'User role successfully updated.')
            return redirect(reverse('users_role', kwargs={'id': group.id}))
        else:
            self.context['form'] = form
            messages.error(request, form.errors)
            return render(request, self.template_name, self.context)


class RoleDeleteView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        group = get_object_or_404(Group, id=kwargs['id'])
        group_action = kwargs['group_action']
        if group_action == 'delete':
            group.delete()
            messages.success(request, 'User role successfully deleted.')
        return redirect(reverse('users_roles'))


class UserViewSet(viewsets.ModelViewSet):
    """
    Users viewset automatically provides `list` and `crud` actions.
    """
    queryset = User.objects.all()

    def get_queryset(self):
        users = User.objects.filter(is_staff=False)
        if self.request.GET.get('q'):
            return users.filter(
                Q(first_name__icontains=self.request.GET.get('q')) |
                Q(last_name__icontains=self.request.GET.get('q')))
        elif self.request.GET.get('f'):
            group_users = users.filter(groups__name=self.request.GET.get('f'))
            if self.request.GET.get('fq'):
                return group_users.filter(
                    Q(first_name__icontains=self.request.GET.get('fq')) |
                    Q(last_name__icontains=self.request.GET.get('fq')))
            return group_users
        else:
            return users

    serializer_class = UserSerializer
    lookup_field = 'id'


class CreateUserViewSet(viewsets.ModelViewSet):
    """
    Create users
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)


class GroupViewSet(viewsets.ModelViewSet):
    """
    View user groups
    """
    queryset = Group.objects.all()

    def get_queryset(self):

        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset

    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)


class CreateGroupViewSet(viewsets.ModelViewSet):
    """
    Create user groups
    """
    queryset = Group.objects.all()
    serializer_class = CreateGroupSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)


class PermissionViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        allowed_permissions = AllowedPermission.objects.all()

        permissions = []
        """
        get permission details for each model
        """
        for allowed_permission in allowed_permissions:
            model_permissions_object = {'model': allowed_permission.name, 'title': allowed_permission.title,
                                        'summary': allowed_permission.summary}
            permission_models = allowed_permission.models.all()
            model_perms = []
            for permission_model in permission_models:
                content_type = get_object_or_404(ContentType, model=permission_model.name,
                                                 app_label=allowed_permission.name)
                model_permissions = Permission.objects.filter(content_type=content_type)
                serializer = PermissionSerializer(model_permissions, many=True)
                model_perms.append(serializer.data)

            model_permissions_object['permissions'] = model_perms

            # append permissions
            permissions.append(model_permissions_object)

        return Response({'results': permissions})


class GroupsViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_groups = Group.objects.all()

        groups = []
        """
        get form employee groups
        """
        for group in all_groups:
            group_object = {'value': group.id, 'label': group.name}

            # append groups
            groups.append(group_object)

        return Response({'results': groups})


class UsersOptionViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_users = User.objects.all()

        users = []
        """
        get user options
        """
        for user in all_users:
            user_object = {'value': user.id, 'label': f'{user.first_name} {user.last_name}'}

            # append users
            users.append(user_object)

        return Response({'results': users})


class DeleteGroupUserViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        group_name = request.GET.get('group')
        user_id = request.GET.get('user')
        g = get_object_or_404(Group, name=group_name)
        g.user_set.remove(user_id)

        return Response({'results': True})
