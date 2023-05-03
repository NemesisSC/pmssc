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
    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blogCreate(request):
    try:
        blog_data = request.data

        if 'image' in blog_data:
            fmt, img_str = str(blog_data['image']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            blog_data['image'] = img_file
        blog_serializer = BlogSerializer(data=blog_data)

        if blog_serializer.is_valid():
            blog_instance = blog_serializer.save()
            blog_slug = slugify(unidecode(blog_serializer.data['title']))
            suffix_counter = 1
            while True:
                temp_instance = Blogs.objects.filter(slug__exact=blog_slug)
                if temp_instance.exists():
                    blog_slug = slugify(unidecode(blog_serializer.data['title']))
                    blog_slug = "%s-%s" % (blog_slug, suffix_counter)
                    suffix_counter += 1
                else:
                    break
            blog_instance.slug = blog_slug
            blog_instance.save()

            return Response({
                'code': status.HTTP_200_OK,
                'response': "Blog Successfully",
                "data": blog_serializer.data

            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Blog Not Created",
                "data": blog_serializer.errors

            })
    except Exception as e:
        print(e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Errors in data",
            'error': str(e)
        })

@api_view(['GET'])

def getBlogs(request):
    try:

        blog_list = Blogs.objects.all()
        blog_serializer = BlogSerializer(blog_list, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Blogs received successfully!',
            'data': blog_serializer.data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })

@api_view(['GET'])
def getBlogs(request):
    try:

        blog_list = Blogs.objects.all()
        blog_serializer = BlogSerializer(blog_list, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Blogs received successfully!',
            'data': blog_serializer.data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })

        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def blogEdit(request, blog_id):
    try:
        blog_data = request.data

        if 'image' in blog_data:
            fmt, img_str = str(blog_data['image']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            blog_data['image'] = img_file


        if 'title' in blog_data:

            blog_slug = slugify(unidecode(blog_data['title']))

            suffix_counter = 1
            while True:
                temp_instance = Blogs.objects.filter(slug__exact=blog_slug)

                if temp_instance.exists():
                    blog_slug = slugify(unidecode(blog_data['title']))
                    blog_slug = "%s-%s" % (blog_slug, suffix_counter)
                    suffix_counter += 1
                else:
                    break
            blog_data['slug'] = blog_slug

        blog_instance = Blogs.objects.get(id=blog_id)
        blog_serializer = BlogSerializer(blog_instance, data=blog_data, partial=True)
        if blog_serializer.is_valid():
            blog_serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Blog Update Successfully",
                "data": blog_serializer.data

            })
        else:
            print("hello")
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Blog Update Failed",
                "data": blog_serializer.errors

            })
    except Exception as e:
        print(e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Errors in data",
            'error': str(e)
        })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def blogDelete(request, blog_id):
    try:
        Blogs.objects.filter(id=blog_id).delete()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Blog deleted successfully!",
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Blog delete failed!",
            "error": str(e)
        })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def blogStatusToggle(request, blog_id):
#     try:
#         blog_instance = Blogs.objects.get(id=blog_id)
#         blog_instance.status = not blog_instance.status
#         blog_instance.save()
#         return Response({
#             'code': status.HTTP_200_OK,
#             'response': "Blog status updated successfully!",
#         })
#     except Exception as e:
#         return Response({
#             'code': status.HTTP_200_OK,
#             'response': "Blog status updated failed!",
#             "error": str(e)
#         })