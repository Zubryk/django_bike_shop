from django.urls import path
from .views import base_view, ProductDetailView, CategoryDetailView, CartView, AddToCartView, DeleteFromView, ChangeQTYView


urlpatterns = [
    path('', base_view, name = 'base'),
    path('products/<str:ct_model>/<str:slug>', ProductDetailView.as_view(), name = 'product'),
    path('category/<str:slug>', CategoryDetailView.as_view(), name = 'category_detail'),
    path('cart/', CartView.as_view(), name = 'cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>', AddToCartView.as_view(), name = 'add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>', DeleteFromView.as_view(), name = 'delete_from_cart'),
    path('change_qty/<str:ct_model>/<str:slug>', ChangeQTYView.as_view(), name = 'change_qty'),
]