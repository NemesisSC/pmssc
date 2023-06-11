from django.db import models

import uuid
# Create your models here.

def generate_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "cwcspublications_%s.%s" % (uuid.uuid4(), extension)
    return new_filename


class Category(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    pid = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True)
    
    category = models.CharField(max_length=200)
    cat_description = models.TextField(null=True)
    sub_category  = models.CharField(max_length=200)
    cat_featured = models.BooleanField(default=False)
    
    featured = models.BooleanField(default=False)
    stock_status = models.BooleanField(default=False)
    hot_items = models.BooleanField(default=False)
    description = models.TextField(null=True)
    sell_description = models.TextField(null=True, blank=True)
    purchase_description = models.TextField(null=True, blank=True)
    sell_price = models.FloatField()
    offer_price = models.FloatField(default=0)
    on_sale = models.BooleanField(default=False)
    tags = models.JSONField(null=True)
    attributes = models.JSONField(null=True)
    status = models.BooleanField(default=False)
    super_sale = models.BooleanField(default=False)
    bmsm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductUnit(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_img')
    image = models.ImageField(upload_to=generate_filename)
