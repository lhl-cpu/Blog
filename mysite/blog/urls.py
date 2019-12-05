from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list,name="blog_list"),
    path("type/<int:blog_type_id>",views.blog_with_type,name="blog_with_type"),
    path("<int:blog_id>",views.blog_tital,name="blog_tital"),
    path("date/<int:year>/<int:month>",views.blog_with_date,name="blog_with_date")
]