from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.text import slugify
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


