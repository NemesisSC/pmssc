from django.conf import settings
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from .models import *



class ProductInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class ProductCartSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'pid', 'name', 'sell_price'
        )


class ProductUnitSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = '__all__'


class ProductImageSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductReadInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    category = serializers.SerializerMethodField('get_category')
    subcategory = serializers.SerializerMethodField('get_subcategory')

    def get_category(self, instance):
        try:
            return {
                'name': instance.category.name,
                'slug': instance.category.slug
            }
        except Exception:
            return {
                'name': '',
                'slug': ''
            }

    def get_subcategory(self, instance):
        try:
            return {
                'name': instance.subcategory.name,
                'slug': instance.subcategory.slug
            }
        except Exception:
            return {
                'name': '',
                'slug': ''
            }

    def get_images(self, instance):
        image_urls = []
        images_list = ProductImageSerializer(instance.product_img.all(), many=True,
                                             context={'request': self.context['request']}).data
        if len(images_list) > 0:
            for img in images_list:
                image_urls.append(img['image'])
        else:
            image_urls.append(
                'http://%s/media/default/placeholder.jpeg' % (self.context['request']).META.get('HTTP_HOST'))
        return image_urls

    class Meta:
        model = Product
        fields = (
            'id', 'pid', 'name', 'slug', 'unit', 'featured', 'hot_items', 'description',
            'sell_description', 'purchase_description', 'sell_price', 'offer_price', 'on_sale',
            'tags', 'attributes', 'status', 'super_sale', 'bmsm', 'images', 'category', 'subcategory',
            'created_at', 'updated_at'
        )
