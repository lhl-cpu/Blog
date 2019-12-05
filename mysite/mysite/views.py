from django.shortcuts import render
from Read_count.util import get_senven_days,get_today_hot,get_yesterday_hot
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from blog.models import Blog

def home(requset):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_senven_days(blog_content_type)

    #设置昨天高速缓存
    yesterday_data = cache.get('yesterday_data')
    if yesterday_data is None:
        cache.set('yesterday_data', get_yesterday_hot(blog_content_type) , 3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['get_yesterday_hot'] = get_yesterday_hot(blog_content_type)
    context['get_today_hot'] = get_today_hot(blog_content_type)
    return render(requset,'home.html',context)