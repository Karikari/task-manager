from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auths.serializers import *
from apps.commons.ModelUtils import get_user_by_email


class SignUpView(APIView):
  serializer_class = SignupSerializer
  permission_classes = [AllowAny, ]

  @swagger_auto_schema(operation_description="Sign Up", responses={201: "Created", 400: "Bad Request"}, request_body=SignupSerializer)
  def post(self, request):
    serializer = self.serializer_class(data=request.data)

    if serializer.is_valid():
      user = get_user_by_email(User, email=request.data['email'])
      if user:
        return Response({'error': 'User already exist'}, status=status.HTTP_400_BAD_REQUEST)
      serializer.save()

      user = get_user_by_email(User, email=serializer.data['email'])
      if user:
        user_data = UserSerializer(user).data
        response_data = {'data': user_data,'token': user.token}
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
  serializer_class = LoginSerializer
  permission_classes = [AllowAny, ]

  @swagger_auto_schema(operation_description="Login", responses={200: "Success", 400: "Bad Request"}, request_body=LoginSerializer)
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      token = get_user_by_email(User, email=serializer.data['email']).token
      if token:
        response_data = {'token': token}
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(operation_description="Password Reset", responses={200: "Success", 400: "Bad Request"}, request_body=PasswordResetSerializer)
    def post(self, request):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
          user = get_user_by_email(User, email=request.data['email'])
          if user:
              user.set_password(request.data['password'])
              user.save()
              return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
          return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
