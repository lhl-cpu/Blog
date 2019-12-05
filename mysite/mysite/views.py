from django.shortcuts import render
from Read_count.util import get_senven_days,get_today_hot,get_yesterday_hot,get_senven_days
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog

def home(requset):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_senven_days(blog_content_type)


    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['get_yesterday_hot'] = get_yesterday_hot(blog_content_type)
    context['get_today_hot'] = get_today_hot(blog_content_type)
    context['get_senven_days'] = get_senven_days(blog_content_type)
    return render(requset,'home.html',context)