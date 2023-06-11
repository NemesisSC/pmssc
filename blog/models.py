from django.db import models
import uuid



def generate_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "cwcspublications_%s.%s" % (uuid.uuid4(), extension)
    return new_filename


class Blogs(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to= generate_filename, default='default/placeholder.jpeg')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)