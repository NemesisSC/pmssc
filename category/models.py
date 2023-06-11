from django.db import models


import system_manager.helper


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    parent = models.IntegerField(default=0)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to=system_manager.helper.generate_filename, null=True, default='default/placeholder.jpeg')
    top_banner = models.ImageField(upload_to=system_manager.helper.generate_filename,null=True, default='default/placeholder.jpeg')
    side_banner = models.ImageField(upload_to=system_manager.helper.generate_filename, null=True, default='default/placeholder.jpeg')
    featured = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)