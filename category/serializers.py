from django.conf import settings
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from .models import *



class CategorySerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



