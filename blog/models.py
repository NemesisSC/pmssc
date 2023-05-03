from django.db import models


import system_manager.helper


class Blogs(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to=system_manager.helper.generate_filename, default='default/placeholder.jpeg')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)