from django.contrib import admin
from .models import Animal, AnimalPhoto, Application


class AnimalPhotoInline(admin.TabularInline):
    model = AnimalPhoto
    extra = 1


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'age', 'gender')
    list_filter = ('species', 'gender')
    search_fields = ('name', 'breed')
    inlines = [AnimalPhotoInline]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'animal', 'full_name', 'phone', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'phone')