from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


User = get_user_model()


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model':ct_model, 'slug':obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in = args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatestProducts:
    objects = LatestProductsManager()


class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50, verbose_name = "category_name")
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug' : self.slug})
    

class Product(models.Model):

    class Meta:
        abstract = True

    category  = models.ForeignKey("Category", verbose_name="Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique = True)
    image = models.ImageField()
    description = models.TextField(null = True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.title

class Bike(Product):

    bike_type = models.CharField(max_length=10)
    brand = models.CharField(max_length=25)
    size = models.CharField(max_length=2)
    frame = models.CharField(max_length=20)
    wheels = models.CharField(max_length=10)
    speeds = models.CharField(max_length=5)
    brakes = models.CharField(max_length=15)
    warranty = models.CharField(max_length=15)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return get_product_url(self, 'product')


class Accessory(Product):

    class Meta:
        verbose_name_plural = "Accessories"

    accessory_type = models.CharField(max_length=15)
    warranty = models.CharField(max_length=15)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return get_product_url(self, 'product')
    


class CartProduct(models.Model):

    user = models.ForeignKey("Customer", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.content_object.title

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey("Customer", on_delete=models.CASCADE)
    products = models.ManyToManyField("CartProduct", blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=250) 

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name