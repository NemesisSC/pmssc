import datetime

from rest_framework import status
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from unidecode import unidecode
from django.utils.text import slugify
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile
import base64
import system_manager.views
from .serializers import *
import json
from datetime import datetime, timedelta
import os
import csv
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
import os


def upload_to(instance, filename):
    right_now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = right_now.microsecond // 1000
    return f"{right_now:%Y%m%d%H%M%S}{milliseconds}{extension}"


