from django.contrib import admin
from .models import ReadNum,Read_detial
# Register your models here.
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_type')

@admin.register(Read_detial)
class Read_detialAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_type')