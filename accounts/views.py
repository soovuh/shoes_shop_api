from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.text import slugify
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


from django.utils.text import slugify

class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        User = get_user_model()
        try:
            # Generate a unique username based on the email address
            username = slugify(email.split('@')[0])
            hashed_password = make_password(password)
            user = User.objects.create(username=username, name=name, email=email, password=hashed_password)

            return Response({'message': 'Registration successful'})
        except Exception as e:
            return Response({'message': 'Registration failed', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'})
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
