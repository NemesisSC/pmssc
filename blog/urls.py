from django.urls import path, include

from .views import *

urlpatterns = [

    path('', getBlogs),
    path('/details/<int:blog_id>', getBlogs),
    path('/create', blogCreate),
    path('/edit/<int:blog_id>', blogEdit),
    path('/delete/<int:blog_id>', blogDelete),
    path('/status/<int:blog_id>', blogStatusToggle),

]
