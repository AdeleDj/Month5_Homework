from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterValidateSerializer, AuthValidateSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .models import UserConfirmation


@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    code = str(random.randint(100000, 999999))
    UserConfirmation.objects.create(user=user, code=code)

    return Response(
        status=status.HTTP_201_CREATED,
        data={'user_id': user.id}
    )


@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def confirm_api_view(request):
    code = request.data.get('code')
    try:
        confirm = UserConfirmation.objects.get(code=code)
        confirm.user.is_active = True
        confirm.user.save()
        confirm.delete()
        return Response(data={'message': 'User activated'})
    except UserConfirmation.DoesNotExist:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'error': 'Wrong code!'}
        )