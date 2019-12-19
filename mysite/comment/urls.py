from django.urls import path
from .models import Comment
from . import views

urlpatterns = [
    path('comment/',views.update_comment, name="update_comment")
]
