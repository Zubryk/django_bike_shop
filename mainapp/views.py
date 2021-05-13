from django.shortcuts import render
from django.views.generic import DetailView
from .models import Bike, Accessory, Category, LatestProducts


def base_view(request):
    categories = Category.objects.get_queryset()
    products = LatestProducts.objects.get_products_for_main_page("bike", "accessory")

    print([category.get_absolute_url() for category in categories])

    context = {
        'categories' : categories,
        'products' : products
        }

    return render(request, 'base.html', context)


class ProductDetailView(DetailView):

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

class CategoryDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['cart'] = self.cart
    #     return context
