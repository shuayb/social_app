# accounts/api/views.py
from django.contrib.auth import get_user_model, user_logged_out
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework.permissions import IsAdminUser

from knox.models import AuthToken
from rest_framework.views import APIView

from acc.api.helpers import set_to_lower_case
from acc.api.permissions import OwnerCanUpdateOnly, IsSuperAdminUser
from .serializers import UserSerializer, \
    RegisterSerializer, \
    LoginSerializer, \
    UserDetailSerializer

# For Session authentication in case
# from django.contrib.auth import (
#     login as django_login,
#     logout as django_logout
# )

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class RegisterAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        set_to_lower_case(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
            # create() returns a tuple (instance, token) [1] specifies second
            # position
        })


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        set_to_lower_case(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # For setting cookie
        # Using sessions framework of django
        # django_login(self.request, user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    @staticmethod
    def logout(request):
        try:
            request._auth.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        # django_logout(request)
        # user_logged_out.send(sender=request.user.__class__,
        #                      request=request, user=request.user)
        return Response({"detail": "Successfully logged out."},
                        status=status.HTTP_200_OK)


# class UserList(ListAPIView):
#     name = 'user-list'
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsSuperAdminUser]


class UserDetailView(RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = UserDetailSerializer

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # When next line - serializer.save() -- is executed
        # UserDetailSerializer's method update is executed
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated & OwnerCanUpdateOnly]

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()  # UserDetailSerializer's method update is executed
        return Response(serializer.data, status=status.HTTP_200_OK)
