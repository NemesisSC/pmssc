from django.urls import path, include

from .views import *


urlpatterns = [
    path('list', get_category),
    path('sub', get_sub_category),
    path('new', categoryCreate),
    path('edit/<int:category_id>', categoryEdit),
    path('delete/<int:category_id>', categoryDelete),
    path('featured/<int:category_id>', categoryFeatureToggle),
    path('status/<int:category_id>', categoryStatusToggle),
    path('by-parent', getCategoryByParent),
]