from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from Read_count.util import get_senven_days,get_today_hot,get_yesterday_hot
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from blog.models import Blog
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm,RegForm

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

def mylogin(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from'),reverse('home'))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)

def myregister(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            #创建用户
            user = User.objects.create_user(username,email,password)
            user.save()
            #用户登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from'),reverse('home'))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request,'register.html',context)