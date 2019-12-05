from django.contrib import admin
from .models import BlogType, Blog

# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'typename')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','blogtypename','get_read_num', 'created_time', 'last_update_time', 'author')