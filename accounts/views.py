from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views import View

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.http import JsonResponse

from django.utils.text import slugify

from accounts.forms import EmailForm
from accounts.verification_email import send_verification_email


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
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            send_verification_email(email, token, user)

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
    def check_authentication(self, request):
        session_id = request.COOKIES.get('sessionid')

        try:
            session = Session.objects.get(session_key=session_id)
        except Session.DoesNotExist:
            return JsonResponse({'message': 'Session not found'}, status=404)

        user_id = session.get_decoded().get('_auth_user_id')

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            username = user.username
            return JsonResponse({'username': username, 'message': 'User is authenticated'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)


class EmailVerificationView(View):
    def get(self, request, user_id, token):
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return render(request, 'accounts/email_verification/verification_success.html')
        except User.DoesNotExist:
            pass
        return render(request, 'accounts/email_verification/verification_failed.html')


class EmailResendView(View):
    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            User = get_user_model()
            user = User.objects.filter(email=email).first()
            if not user:
                return render(request, 'accounts/email_verification/verification_resend_failed.html', {
                    "message": "User not found, verify the email is correct"
                })
            if user.is_active:
                return render(request, 'accounts/email_verification/verification_resend_failed.html', {
                    "message": "You have already verified your account, just login!"
                })

            token = default_token_generator.make_token(user)
            send_verification_email(email, token, user)

            return render(request, 'accounts/email_verification/verification_resend_success.html')

    def get(self, request):
        form = EmailForm()
        return render(request, 'accounts/email_verification/resend_verification_email.html', {
            'form': form,
        })
