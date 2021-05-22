from django.db import models
from django.db.models.base import Model
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from .models import Bike, Accessory, Category, LatestProducts, Customer, Cart, CartProduct
from .mixins import CategoryDetailMixin, CartMixin


def base_view(request):
    customer = Customer.objects.get(user = request.user)
    cart = Cart.objects.get(owner = customer)
    categories = Category.objects.get_queryset()
    products = LatestProducts.objects.get_products_for_main_page("bike", "accessory")

    context = {
        'categories' : categories,
        'products' : products,
        'cart' : cart
        }

    return render(request, 'base.html', context)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):

    CT_MODEL_CLASS = {
        'accessory': Accessory,
        'bike': Bike 
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context
 
 
class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        customer = Customer.objects.get(user = request.user)
        cart = Cart.objects.get(owner = customer, in_order = False)
        content_type = ContentType.objects.get(model = ct_model)
        product = content_type.model_class().objects.get(slug = product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user = cart.owner,
            cart = cart,
            content_type = content_type,
            object_id=product.id
        )
        if created:
            cart.products.add(cart_product)
        cart.save()
            
        return HttpResponseRedirect('/cart/')

class DeleteFromView(View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        customer = Customer.objects.get(user = request.user)
        cart = Cart.objects.get(owner = customer, in_order = False)
        content_type = ContentType.objects.get(model = ct_model)
        product = content_type.model_class().objects.get(slug = product_slug)
        cart_product = CartProduct.objects.get(
            user = cart.owner,
            cart = cart,
            content_type = content_type,
            object_id=product.id
        )
        cart.products.remove(cart_product)
        cart_product.delete()
        cart.save()

        return HttpResponseRedirect('/cart/')

class ChangeQTYView(View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        customer = Customer.objects.get(user = request.user)
        cart = Cart.objects.get(owner = customer, in_order = False)
        content_type = ContentType.objects.get(model = ct_model)
        product = content_type.model_class().objects.get(slug = product_slug)
        cart_product = CartProduct.objects.get(
            user = cart.owner,
            cart = cart,
            content_type = content_type,
            object_id=product.id
        )
        cart_product.qty = int(request.POST.get('qty'))
        cart_product.save()
        cart.save()
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_queryset()
        return render(request, 'cart.html', {'cart' : self.cart, 'categories' : categories})