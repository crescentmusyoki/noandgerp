from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from rest_framework import pagination
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

# Web view
from apps.general.forms import UserForm


class WebView(LoginRequiredMixin, View):
    template_name = 'index.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)


# User settings
class Settings(LoginRequiredMixin, View):
    template_name = 'profile/settings.html'
    context = {}

    def get(self, request):
        user_form = UserForm(instance=request.user)

        self.context['user_form'] = user_form
        return render(request, self.template_name, self.context)


# Home view
class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# Login API
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        full_name = '%s %s' % (user.first_name, user.last_name)
        user_groups = user.groups.all()
        user_group = None
        for ug in user_groups:
            user_group = ug.name

        perms = user.get_all_permissions()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'data': {
            'token': token.key,
            'full_name': full_name,
            'user_id': user.pk,
            'username': user.username,
            'user_group': user_group,
            'email': user.email,
            'permissions': perms
        }})


class APIPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class NoNewUsersAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.
        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse
        (Comment reproduced from the overridden method.)
        """
        return False
