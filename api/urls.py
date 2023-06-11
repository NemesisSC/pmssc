from django.urls import path, include

urlpatterns = [

    path('auth/', include('authentication.urls')), 
    path('product/category/', include('category.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    
      

]

