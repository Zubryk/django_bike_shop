from django.shortcuts import render
from django.views.generic import DetailView
from .models import Bike, Accessory


def test_view(request):
    return render(request, 'base.html', {})


class ProductDetailView(DetailView):

    CT_MODEL_CLASS = {
        'accessory': Accessory,
        'bike': Bike 
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    # model = Model
    # queryset = Model.objects.all()
    context_object_name = 'product'
    template_name = 'product.html'
    slug_url_kwarg = 'slug'