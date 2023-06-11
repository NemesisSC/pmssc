from django.urls import path, include

from .views import *

urlpatterns = [

    path('', gb),
    path('/details/<int:blog_id>', gb),
    path('/create', bc),
    path('/edit/<int:blog_id>', be),
    path('/delete/<int:blog_id>', bd),
    path('/status/<int:blog_id>', bst),

]
