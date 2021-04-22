from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


User = get_user_model()


class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50, verbose_name = "category_name")
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.name
    
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


class Accesory(Product):

    class Meta:
        verbose_name_plural = "Accessories"

    accesory_type = models.CharField(max_length=15)
    warranty = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class CartProduct(models.Model):

    user = models.ForeignKey("Customer", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.content_type.title


class Cart(models.Model):

    owner = models.ForeignKey("Customer", on_delete=models.CASCADE)
    products = models.ManyToManyField("CartProduct", blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=250) 

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name