from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Blog,BlogType
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from Read_count.util import read_count_make
from comment.forms import CommentForm

blog_each_num_page = 8

# Create your views here.
def blog_list_comment(request,blogs_all_list):
    paginator = Paginator(blogs_all_list,blog_each_num_page)
    page_num = request.GET.get('page',1)
    page_of_blogs = paginator.get_page(page_num)
    curr_page_num = page_of_blogs.number #获取当前页数
    page_range = list(range(max(curr_page_num - 2, 1),curr_page_num)) + list(range(curr_page_num,min(curr_page_num+2,paginator.num_pages) + 1))
    #省略标记
    if page_range[0]-1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    #首页和尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #博客分类统计数量
    '''blog_list_type_count = []
    blog_types = BlogType.objects.all()
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blogtypename=blog_type).count()
        blog_list_type_count.append(blog_type)'''

    #博客时间归档统计数量
    blog_dates = Blog.objects.dates('created_time','month',order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['blog_dates'] = blog_dates_dict
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog_blog'))
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = blog_list_comment(request,blogs_all_list)
    return render(request, 'blog_list.html', context)

def blog_with_type(request,blog_type_id):
    blog_type = get_object_or_404(BlogType,pk=blog_type_id)
    blogs_all_list = Blog.objects.filter(blogtypename=blog_type)

    context = blog_list_comment(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog_with_type.html', context)

def blog_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)

    context = blog_list_comment(request,blogs_all_list)
    context['blog_with_date'] = "%s年%s月" % (year,month)
    return render(request, 'blog_with_date.html', context)

def blog_tital(request,blog_id):
    context = {}

    blog = get_object_or_404(Blog, pk=blog_id)
    getkey = read_count_make(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk)

    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['comment_forms'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_id})
    context['comments'] = comments
    response = render(request, 'blog_tital.html', context)#响应
    response.set_cookie(getkey ,'true')
    return response