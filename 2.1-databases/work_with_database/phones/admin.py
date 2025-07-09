from django.contrib import admin
from .models import Phone


# Register your models here.
@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'price', 'release_date', 'lte_exists', 'slug']
    list_display_links = ['name']
    list_filter = ['name', 'price', 'lte_exists']
    search_fields = ['name', 'price']
