from django.contrib.auth import authenticate, login, logout, get_user_model
from django.middleware.csrf import get_token

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.http import JsonResponse

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

            csrf_token = get_token(request)
            session_id = request.session.session_key

            # Return the CSRF token and session ID in the response
            return Response({
                'message': 'Login successful',
                'csrf_token': csrf_token,
                'session_id': session_id
            })
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_username(self, request):
        csrf_token = request.headers['X-Csrftoken']
        session_id = request.COOKIES.get('sessionid')

        # Retrieve the session object based on the session ID
        session = Session.objects.get(session_key=session_id)

        # Retrieve the user ID from the session data
        user_id = session.get_decoded().get('_auth_user_id')

        # Retrieve the user object using the user ID
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            username = user.username
            # Return the user's username in the response
            return JsonResponse({'username': username})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
