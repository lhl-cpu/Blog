from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from Read_count.models import ReadNumExpent

class BlogType(models.Model):
    typename = models.CharField(max_length=15)

    def __str__(self):
        return self.typename

class Blog(models.Model,ReadNumExpent):
    title = models.CharField(max_length=50)
    blogtypename = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING,related_name='blog_blog')
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Blog %s>' % self.title

    class Meta:
        ordering = ['-created_time']