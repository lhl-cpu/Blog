from django.urls import path
from .models import Comment
from . import views

urlpatterns = [
    path('comment/',views.upload_comment, name="upload_comment")
]
