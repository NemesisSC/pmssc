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
from datetime import datetime, timedelta
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



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
#@permission_required(['product.view_category'], raise_exception=True)
def get_category(request):
    try:
        category_list = Category.objects.filter(parent=0)
        category_serializer = CategorySerializer(category_list, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": category_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
#@permission_required(['product.view_category'], raise_exception=True)
def get_sub_category(request):
    try:
        category_list = Category.objects.all().exclude(parent=0)
        category_serializer = CategorySerializer(category_list, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": category_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })



@api_view(['POST'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.add_category'], raise_exception=True)
def categoryCreate(request):
    try:
        category_data = request.data

        if 'image' in category_data:
            fmt, img_str = str(category_data['image']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            category_data['image'] = img_file

        if 'top_banner' in category_data:
            fmt, img_str = str(category_data['top_banner']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            category_data['top_banner'] = img_file

        if 'side_banner' in category_data:
            fmt, img_str = str(category_data['side_banner']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            category_data['side_banner'] = img_file
        category_serializer = CategorySerializer(data=category_data)

        if category_serializer.is_valid():
            category_instance = category_serializer.save()
            category_slug = slugify(unidecode(category_serializer.data['name']))
            suffix_counter = 1
            while True:
                temp_instance = Category.objects.filter(slug__exact=category_slug)
                if temp_instance.exists():
                    category_slug = slugify(unidecode(category_serializer.data['name']))
                    category_slug = "%s-%s" % (category_slug, suffix_counter)
                    suffix_counter += 1
                else:
                    break
            category_instance.slug = category_slug
            category_instance.save()

            return Response({
                'code': status.HTTP_200_OK,
                'response': "Category Created Successfully",
                "data": category_serializer.data

            })
        else:
            print("hello")
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Category Not Created",
                "data": category_serializer.errors

            })
    except Exception as e:
        print(e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Errors in data",
            'error': str(e)
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.change_category'], raise_exception=True)
def categoryFeatureToggle(request, category_id):
    try:
        category_instance = Category.objects.get(id=category_id)
        category_instance.featured = not category_instance.featured
        category_instance.save()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Category featured status updated successfully!",
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Category featured status updated failed!",
            "error": str(e)
        })


#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.change_category'], raise_exception=True)
def categoryStatusToggle(request, category_id):
    try:
        category_instance = Category.objects.get(id=category_id)
        category_instance.status = not category_instance.status
        category_instance.save()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Category status updated successfully!",
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Category status updated failed!",
            "error": str(e)
        })


#
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.delete_category'], raise_exception=True)
def categoryDelete(request, category_id):
    try:
        Category.objects.filter(id=category_id).delete()
        Category.objects.filter(parent=category_id).delete()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Category deleted successfully!",
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Category delete failed!",
            "error": str(e)
        })


#
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.change_category'], raise_exception=True)
def categoryEdit(request, category_id):
    try:
        category_data = request.data

        if 'image' in category_data:
            fmt, img_str = str(category_data['image']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            category_data['image'] = img_file

        if 'top_banner' in category_data:
            fmt, img_str = str(category_data['top_banner']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            category_data['top_banner'] = img_file

        if 'side_banner' in category_data:
            fmt, img_str = str(category_data['side_banner']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            category_data['side_banner'] = img_file

        if 'name' in category_data:
            category_slug = slugify(unidecode(category_data['name']))
            suffix_counter = 1
            while True:
                temp_instance = Category.objects.filter(slug__exact=category_slug)
                if temp_instance.exists():
                    category_slug = slugify(unidecode(category_data['name']))
                    category_slug = "%s-%s" % (category_slug, suffix_counter)
                    suffix_counter += 1
                else:
                    break
            category_data['slug'] = category_slug

        category_instance = Category.objects.get(id=category_id)
        category_serializer = CategorySerializer(category_instance, data=category_data, partial=True)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Category Updated Successfully",
                "data": category_serializer.data

            })
        else:
            print("hello")
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Category Update Failed",
                "data": category_serializer.errors

            })
    except Exception as e:
        print(e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Errors in data",
            'error': str(e)
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.view_category'], raise_exception=True)
def getCategoryByParent(request):
    try:
        print(request.data["parent"])
        parent_id = request.data["parent"]
        category_list = Category.objects.filter(parent=parent_id)
        category_serializer = CategorySerializer(category_list, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Subcategories received successfully!',
            'data': category_serializer.data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })
