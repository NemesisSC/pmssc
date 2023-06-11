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



#
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def productView(request):
    try:

        product_list = Product.objects.all().order_by('created_at').reverse()
        product_serializer = ProductReadInfoSerializer(product_list, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Product Data Successfully",
            "data": product_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })
        
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def productByCategory(request, slug):
    try:

        product_list = Product.objects.filter(category__slug=slug).order_by('created_at').reverse()
        product_serializer = ProductReadInfoSerializer(product_list, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Product Data Successfully",
            "data": product_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })
        
@api_view(["GET"])
# @permission_classes([IsAuthenticated])       
def featuredProduct(request):
    try:

        product_list = Product.objects.filter(featured=True).order_by('created_at').reverse()
        product_serializer = ProductReadInfoSerializer(product_list, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Product Data Successfully",
            "data": product_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })

@api_view(["GET"])
# @permission_classes([IsAuthenticated])       
def hotProduct(request):
    try:

        product_list = Product.objects.filter(hot_items=True).order_by('created_at').reverse()
        product_serializer = ProductReadInfoSerializer(product_list, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Product Data Successfully",
            "data": product_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })

@api_view(["GET"])
# @permission_classes([IsAuthenticated])       
def onSaleProduct(request):
    try:

        product_list = Product.objects.filter(on_sale=True).order_by('created_at').reverse()
        product_serializer = ProductReadInfoSerializer(product_list, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Product Data Successfully",
            "data": product_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })

@api_view(["GET"])
# @permission_classes([IsAuthenticated])       
def inStockProduct(request):
    try:

        product_list = Product.objects.filter(status=True).order_by('created_at').reverse()
        product_serializer = ProductReadInfoSerializer(product_list, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Product Data Successfully",
            "data": product_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
#@permission_required(['product.add_product'], raise_exception=True)
def productCreate(request):
    try:

        product_data = request.data

        if not ProductUnit.objects.filter(name=product_data['unit']).exists():
            ProductUnit.objects.create(
                name=product_data['unit']
            )

        product_serializer = ProductInfoSerializer(data=product_data)

        if product_serializer.is_valid():
            # print(product_serializer.data)
            product_instance = product_serializer.save()
            product_instance.unit = str(product_instance.unit).upper()
            product_instance.pid = "P{:05d}".format(product_instance.id)
            product_instance.save()
            product_slug = slugify(unidecode(product_instance.name))
            suffix_counter = 1
            while True:
                temp_instance = Product.objects.filter(slug__exact=product_slug)
                if temp_instance.exists():
                    product_slug = slugify(unidecode(product_instance.name))
                    product_slug = "%s-%s" % (product_slug, suffix_counter)
                    suffix_counter += 1
                else:
                    break
            product_instance.slug = product_slug
            product_instance.save()
            print("hello")
            try:
                image_files = product_data['product_image']
                for img in image_files:
                    if img != "":
                        # Base 64 to Img
                        fmt, img_str = str(img).split(';base64,')
                        ext = fmt.split('/')[-1]
                        img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
                        ProductImages.objects.create(
                            product_id=product_instance.id,
                            image=img_file
                        )
            except Exception as e:
                pass

            return Response({
                'code': status.HTTP_200_OK,
                'response': "Product Created Successfully",
                "data": product_serializer.data
            })

        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Product Not Created",
                "data": product_serializer.errors

            })
    except Exception as e:
        print(e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Errors in data",
            'error': str(e)
        })


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
#@permission_required(['product.change_product'], raise_exception=True)
def productEdit(request, product_id):
    try:
        product_data = request.data

        if not ProductUnit.objects.filter(name=product_data['unit']).exists():
            ProductUnit.objects.create(
                name=product_data['unit']
            )

        print(product_data['name'])
        if 'name' in product_data:
            product_slug = slugify(unidecode(product_data['name']))
            suffix_counter = 1
            while True:
                temp_instance = Product.objects.filter(slug__exact=product_slug)
                if temp_instance.exists():
                    product_slug = slugify(unidecode(product_data['name']))
                    product_slug = "%s-%s" % (product_slug, suffix_counter)
                    suffix_counter += 1
                else:
                    break
            product_data['slug'] = product_slug

        product_instance = Product.objects.get(pid__exact=product_id)
        product_serializer = ProductInfoSerializer(product_instance, data=product_data, partial=True)
        if product_serializer.is_valid():
            product_serializer.save()
            try:
                image_files = product_data['product_image']
                for img in image_files:
                    if img != "":
                        # Base 64 to Img
                        fmt, img_str = str(img).split(';base64,')
                        ext = fmt.split('/')[-1]
                        img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
                        ProductImages.objects.create(
                            product_id=product_instance.id,
                            image=img_file
                        )
            except Exception as e:
                pass

            return Response({
                'code': status.HTTP_200_OK,
                'response': "Product Updated Successfully",
                "data": product_serializer.data
            })

        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Product Not updated",
                "data": product_serializer.errors

            })
    except Exception as e:
        print(e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Errors in data",
            'error': str(e)
        })

        # Image Work


#
#
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
#@permission_required(['product.view_product'], raise_exception=True)
def productDetails(request, product_id):
    try:
        product_details = Product.objects.get(pid__exact=product_id)
        print(product_details)
        product_serializer = ProductReadInfoSerializer(product_details, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Product Detailed Data Successfully",
            "data": product_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.delete_product'], raise_exception=True)
def productDelete(request, product_id):
    try:
        Product.objects.filter(pid__exact=product_id).delete()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Product deleted successfully!",
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Product delete failed!",
            "error": str(e)
        })


#
#
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
#@permission_required(['product.view_product'], raise_exception=True)
def productInfo(request, product_id):
    try:
        product_info = Product.objects.get(pid__exact=product_id)
        product_info = ProductInfoSerializer(product_info, context={'request': request}).data

        product_image = ProductImages.objects.filter(product_id=product_info['id'])
        product_image = ProductImageSerializer(product_image, context={'request': request}, many=True).data
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Product info received successfully!',
            'data': product_info,
            'image': product_image
        })
    except Exception as e:
        # system_manager.views.log(request.path, e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e),
            'data': {}
        })


#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.change_product'], raise_exception=True)
def productFeatured(request, product_id):
    try:
        product_instance = Product.objects.get(pid__exact=product_id)
        product_instance.featured = not product_instance.featured
        product_instance.save()
        response = {
            'code': status.HTTP_200_OK,
            'message': 'Featured status updated successfully!',
            'featured_item': product_instance.featured
        }
        # messages.success(request, 'Featured status updated successfully!')
    except Exception as e:

        response = {
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Featured Status update failed!",
            "error": str(e)
        }
    return Response(response)
    # return HttpResponseRedirect(reverse('crm.product.view'))
    #


@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.change_product'], raise_exception=True)
def productHotItem(request, product_id):
    try:
        product_instance = Product.objects.get(pid__exact=product_id)
        product_instance.hot_items = not product_instance.hot_items
        product_instance.save()
        response = {
            'code': status.HTTP_200_OK,
            'message': 'Hot Items status updated successfully!',
            'Hot-Item': product_instance.hot_items
        }
        # messages.success(request, 'Featured status updated successfully!')
    except Exception as e:

        response = {
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Hot Items Status update failed!",
            "error": str(e)
        }
    return Response(response)
    # return HttpResponseRedirect(reverse('crm.product.view'))


#

#
#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.change_product'], raise_exception=True)
def productBMSM(request, product_id):
    try:
        product_instance = Product.objects.get(pid__exact=product_id)
        product_instance.bmsm = not product_instance.bmsm
        product_instance.save()
        response = {
            'code': status.HTTP_200_OK,
            'message': 'Buy More Save More status updated successfully!',
            'BMSM': product_instance.bmsm
        }

    except Exception as e:

        response = {
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Buy More Save More Status update failed!",
            "error": str(e)
        }
    return Response(response)


@ api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.change_product'], raise_exception=True)
def productSS(request, product_id):
    try:
        product_instance = Product.objects.get(pid__exact=product_id)
        product_instance.super_sale = not product_instance.super_sale
        product_instance.save()
        response = {
            'code': status.HTTP_200_OK,
            'message': 'Super Sale status updated successfully!',
            'Super-Sale': product_instance.super_sale
        }

    except Exception as e:

        response = {
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Super Sale Status update failed!",
            "error": str(e)
        }
    return Response(response)


#     # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#

#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.change_product'], raise_exception=True)
def productStatusToggle(request, product_id):
    try:
        product_instance = Product.objects.get(pid__exact=product_id)
        product_instance.status = not product_instance.status
        product_instance.save()
        response = {
            'code': status.HTTP_200_OK,
            'message': 'Product status updated successfully!',
            'Status': product_instance.status
        }

    except Exception as e:

        response = {
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Product Status update failed!",
            "error": str(e)
        }
    return Response(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.view_productunit'], raise_exception=True)
def getProductUnit(request):
    try:

        product_unit_list = ProductUnit.objects.all()
        product_unit_serializer = ProductUnitSerializer(product_unit_list, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Product Unit Data Successfully",
            "data": product_unit_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.add_productunit'], raise_exception=True)
def createProductUnit(request):
    try:

        product_unit_data = request.data
        product_unit_serializer = ProductUnitSerializer(data=product_unit_data)

        if product_unit_serializer.is_valid():
            if not ProductUnit.objects.filter(name=product_unit_data['name']).exists():
                product_unit_serializer.save()

                return Response({
                    'code': status.HTTP_200_OK,
                    'response': "Product Unit Created Successfully",
                    "data": product_unit_serializer.data

                })
            else:
                return Response({
                    'code': status.HTTP_200_OK,
                    'response': "Product Unit Already Exists",
                })

        else:
            print("hello")
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Product Unit creation failed",
                "data": product_unit_serializer.errors

            })
    except Exception as e:
        print(e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Errors in data",
            'error': str(e)
        })


#
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.delete_productunit'], raise_exception=True)
def productUnitDelete(request, unit_id):
    try:
        ProductUnit.objects.filter(id=unit_id).delete()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Product Unit Deleted successfully!",
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Product Unit Delete failed!",
            "error": str(e)
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
#@permission_required(['product.change_product'], raise_exception=True)
def priceUpdater(request, product_id):
    product_data = request.data
    try:
        instance = Product.objects.get(pid__exact=product_id)
        instance.cost_price = float(product_data['cost_price'])
        instance.sell_price = float(product_data['sell_price'])
        instance.on_sale = float(product_data['on_sale'])
        instance.offer_price = float(product_data['offer_price'])
        instance.save()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Product Price Updated Successfully",

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Product Price Updated failed!",
            "error": str(e)
        })
