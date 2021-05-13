from django.urls import path
from .views import base_view, ProductDetailView, CategoryDetailView


urlpatterns = [
    path('', base_view, name = 'base'),
    path('products/<str:ct_model>/<str:slug>', ProductDetailView.as_view(), name = 'product'),
    path('category/<str:slug>', CategoryDetailView.as_view(), name='category_detail')
]