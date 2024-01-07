from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import Category

class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

