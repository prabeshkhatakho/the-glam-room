from django.contrib import admin
from myapp.models import Contact
from .models import Gallery, Price, ServiceCategory, AboutUsCategory, Makeup

# Register your models here.

admin.site.register(Contact)




@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(AboutUsCategory)
class AboutUsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'category', 'price', 'is_active')
    list_filter = ('category', 'is_active')

from .models import Product
from .models import Hairstyle

admin.site.register(Product)

admin.site.register(Hairstyle)
admin.site.register(Makeup)

# admin.py
from .models import Appointment

admin.site.register(Appointment)

# admin.py
from .models import Artist

admin.site.register(Artist)



