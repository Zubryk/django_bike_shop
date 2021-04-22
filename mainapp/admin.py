from django.contrib import admin
from django import forms
from .models import *


class BikeCategoryChoiceField(forms.ModelChoiceField):
    pass


class BikeAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return BikeCategoryChoiceField(Category.objects.filter(slug='bikes'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AccessoryCategoryChoiceField(forms.ModelChoiceField):
    pass


class AccessoryAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return AccessoryCategoryChoiceField(Category.objects.filter(slug='accessories'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Bike, BikeAdmin)
admin.site.register(Accesory)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)