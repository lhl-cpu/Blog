from django.shortcuts import render,redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .forms import CommentForm


# Create your views here.
def upload_comment(request):
    '''referer = request.META.get('HTTP_REFERER',reverse('home'))
    user = request.user
    if not request.user.is_authenticated:
        return render(request,'error.html',{'error_message':'用户未登录', 'redirect_to':referer})
    text = request.POST.get('text','').strip()
    if text == '':
        return render(request,'error.html',{'error_message':'内容为空', 'redirect_to':referer})
    try:
        content_type = request.POST.get('content_type','')
        object_id = int(request.POST.get('object_id',''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request,'error.html',{'error_message':'评论对象错误', 'redirect_to':referer})

    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)'''
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    comment_form = CommentForm(request.POST,user=request.user)

    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_type']
        comment.save()
        return redirect(referer)
    else:
        return render(request,'error.html',{'error_message':comment_form.errors, 'redirect_to':referer})