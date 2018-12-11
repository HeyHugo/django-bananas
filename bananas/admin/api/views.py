from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .mixins import BananasAPI
from .permissions import IsAnonymous
from .schemas import schema
from .serializers import (
    AuthenticationSerializer,
    PasswordChangeSerializer,
    UserSerializer,
)

UNDEFINED = object()


class BananasAdminAPI(BananasAPI, viewsets.GenericViewSet):
    pass


class LoginAPI(BananasAdminAPI):

    name = _("Log in")
    basename = "login"
    permission_classes = (IsAnonymous,)
    serializer_class = AuthenticationSerializer  # Placeholder for schema

    class Admin:
        verbose_name_plural = None

    @schema(responses={200: UserSerializer})
    def create(self, request):
        """
        Log in django staff user
        """
        # TODO: Decorate api with sensitive post parameters as Django admin do?
        # from django.utils.decorators import method_decorator
        # from django.views.decorators.debug import sensitive_post_parameters
        # sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

        login_form = AuthenticationForm(request, data=request.data)

        if not login_form.is_valid():
            raise serializers.ValidationError(login_form.errors)

        auth_login(request, login_form.get_user())

        # TODO: Return user?
        return Response(status=status.HTTP_200_OK)


class LogoutAPI(BananasAPI, viewsets.ViewSet):

    name = _("Log out")
    basename = "logout"

    class Admin:
        verbose_name_plural = None

    @schema(responses={204: ""})
    def create(self, request):
        """
        Log out django staff user
        """
        auth_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordAPI(BananasAdminAPI):

    name = _("Change password")
    basename = "change_password"
    serializer_class = PasswordChangeSerializer  # Placeholder for schema

    class Admin:
        verbose_name_plural = None

    @schema(responses={204: ""})
    def create(self, request):
        """
        Change password for django staff user
        """
        # TODO: Decorate api with sensitive post parameters as Django admin do?

        password_form = PasswordChangeForm(request.user, data=request.data)

        if not password_form.is_valid():
            raise serializers.ValidationError(password_form.errors)

        password_form.save()

        return Response(status=status.HTTP_204_ACCEPTED)
