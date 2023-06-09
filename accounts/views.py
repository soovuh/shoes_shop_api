from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.db.utils import IntegrityError

from django.utils.text import slugify

from accounts.forms import EmailForm, ResetPasswordForm
from accounts.models import Address
from accounts.verification_email import send_verification_email, send_reset_email
from cart.models import Cart
from private import frontend_page, base_link


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
            cart = Cart.objects.create(user=user)
            cart.save()

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

    @action(detail=False, methods=['get'])
    def get_user_info(self, request):
        session_id = request.COOKIES.get('sessionid')

        try:
            session = Session.objects.get(session_key=session_id)
        except Session.DoesNotExist:
            return JsonResponse({'message': 'Session not fonud'}, status=404)

        user_id = session.get_decoded().get('_auth_user_id')

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            name = user.name
            phone_number = user.phone_number
            user_address = user.address
            email = user.email
            if user_address:
                address = {
                    'city': user_address.city,
                    'street': user_address.street,
                    'postcode': user_address.postcode
                }
            else:
                address = None
            return JsonResponse({'username': name, 'phone_number': phone_number, 'address': address, 'email': email})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def change_user_info(self, request):
        session_id = request.COOKIES.get('sessionid')

        try:
            session = Session.objects.get(session_key=session_id)
        except Session.DoesNotExist:
            return JsonResponse({'message': 'Session not fonud'}, status=404)

        user_id = session.get_decoded().get('_auth_user_id')

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            previous_address = user.address
            phone_number = request.data.get('phone_number')
            name = request.data.get('username')
            city = request.data.get('city')
            street = request.data.get('street')
            postcode = request.data.get('postcode')

            if phone_number:
                try:
                    try:
                        phone_used = User.objects.get(phone_number=phone_number)
                        if phone_used != user:
                            return JsonResponse({'message': "Phone already used"})
                    except ObjectDoesNotExist:
                        user.phone_number = phone_number
                        user.save()
                except IntegrityError:
                    return JsonResponse({'message': "Phone already used"})
            if name:
                user.name = name
                user.save()
            if city and street and postcode:
                city = city.capitalize()
                street = street.capitalize()

                try:
                    address = Address.objects.get(city=city, street=street, postcode=postcode)
                except Address.DoesNotExist:
                    address = Address.objects.create(city=city, street=street, postcode=postcode)
                    address.save()
                user.address = address
                user.save()
                if User.objects.filter(address=previous_address).aggregate(count=Count('id'))['count'] < 1:
                    previous_address.delete()
            return JsonResponse({'message': "Change Success"})
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

                return render(request, 'accounts/email_verification/verification_success.html', {
                    'frontend_page': frontend_page,
                    'base_link': base_link,
                })
        except User.DoesNotExist:
            pass
        return render(request, 'accounts/email_verification/verification_failed.html', {
            'frontend_page': frontend_page,
            'base_link': base_link,
        })


class EmailResendView(View):
    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            User = get_user_model()
            user = User.objects.filter(email=email).first()
            if not user:
                return render(request, 'accounts/email_verification/verification_resend_failed.html', {
                    "message": "User not found, verify the email is correct",
                    'frontend_page': frontend_page,
                    'base_link': base_link,
                })
            if user.is_active:
                return render(request, 'accounts/email_verification/verification_resend_failed.html', {
                    "message": "You have already verified your account, just login!",
                    'frontend_page': frontend_page,
                    'base_link': base_link,
                })

            token = default_token_generator.make_token(user)
            send_verification_email(email, token, user)

            return render(request, 'accounts/email_verification/verification_resend_success.html', {
                'frontend_page': frontend_page,
                'base_link': base_link,
            })

    def get(self, request):
        form = EmailForm()
        return render(request, 'accounts/email_verification/resend_verification_email.html', {
            'form': form,
            'frontend_page': frontend_page,
            'base_link': base_link,
        })


class EmailPasswordResetView(View):
    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            User = get_user_model()
            user = User.objects.filter(email=email).first()
            if not user:
                return render(request, 'accounts/password_reset/reset_password_failed.html', {
                    "message": "User not found, verify the email is correct",
                    'frontend_page': frontend_page,
                    'base_link': base_link,
                })
            if not user.is_active:
                return render(request, 'accounts/password_reset/reset_password_failed.html', {
                    "message": "Firstly, you need to verify your email!",
                    'frontend_page': frontend_page,
                    'base_link': base_link,
                })

            token = default_token_generator.make_token(user)
            send_reset_email(email, token, user)

            return render(request, 'accounts/password_reset/verification_reset_email_success.html', {
                'frontend_page': frontend_page,
                'base_link': base_link,
            })

    def get(self, request):
        form = EmailForm()
        return render(request, 'accounts/password_reset/email_for_reset.html', {
            'form': form,
            'frontend_page': frontend_page,
            'base_link': base_link,
        })


class PasswordResetView(View):
    def get(self, request, user_id, token):
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                form = ResetPasswordForm()
                return render(request, 'accounts/password_reset/reset_password.html', {
                    'form': form,
                    'frontend_page': frontend_page,
                    'base_link': base_link,
                })
        except User.DoesNotExist:
            pass
        return render(request, 'accounts/password_reset/reset_password_failed.html', {
            'message': 'Reset Email expired!',
            'frontend_page': frontend_page,
            'base_link': base_link,
        })

    def post(self, request, user_id, token):

        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                form = ResetPasswordForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data['password']
                    password1 = form.cleaned_data['password1']
                    if password1 == password:
                        hashed_password = make_password(password)
                        user.password = hashed_password
                        user.save()
                        return render(request, 'accounts/password_reset/reset_password_success.html', {
                            'frontend_page': frontend_page,
                            'base_link': base_link,
                        })
        except User.DoesNotExist:
            pass
        return render(request, 'accounts/password_reset/reset_password_failed.html', {
            'message': 'Passwords do not match or the password does not match the standards!',
            'frontend_page': frontend_page,
            'base_link': base_link,
        })
