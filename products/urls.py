from django.urls import path, include

from .views import *


urlpatterns = [
    path('', productView),
    path('category/<str:slug>', productByCategory),
    # path('products-ssr', productViewSSR, name='crm.product.view.ssr'),
    path('create', productCreate),
    path('edit/<str:product_id>', productEdit),
    path('details/<str:product_id>', productDetails),
    path('delete/<str:product_id>', productDelete),
    path('info/<str:product_id>', productInfo),
    path('featured', featuredProduct),
    path('hot', hotProduct),
    path('on-sale', onSaleProduct),
    path('in-stock', inStockProduct),
    path('toggle-featured/<str:product_id>', productFeatured),
    path('hot-item/<str:product_id>', productHotItem),
    path('bmsm/<str:product_id>', productBMSM),
    path('super-sale/<str:product_id>', productSS),
    path('status/<str:product_id>', productStatusToggle),




    path('/unit', getProductUnit),
    path('/unit/create', createProductUnit),
    path('/unit/delete/<int:unit_id>', productUnitDelete),
]