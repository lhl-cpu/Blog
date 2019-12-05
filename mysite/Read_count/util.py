import datetime
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,Read_detial
from django.utils import timezone


def read_count_make(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model ,obj.pk)

    if not request.COOKIES.get(key):#处理cookie
        '''if ReadNum.objects.filter(content_type=ct,object_id=obj.pk).count():
            #存在记录
            readnum = ReadNum.objects.get(content_type=ct,object_id=obj.pk)
        else:
            #不存在
            readnum = ReadNum(content_type=ct,object_id=obj.pk)'''
        #阅读计数加一
        readnum,created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        '''if Read_detial.objects.filter(content_type=ct,object_id=obj.pk,date=date).count():
            readnum = Read_detial.objects.get(content_type=ct,object_id=obj.pk,date=date)
        else:
            #不存在
            readnum = Read_detial(content_type=ct,object_id=obj.pk,date=date)'''
        #当天阅读计数加一
        date = timezone.now().date()
        readDetial,created = Read_detial.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        readDetial.read_num += 1
        readDetial.save()
    return key


def get_senven_days(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_detials = Read_detial.objects.filter(content_type=content_type, date=date)
        result = read_detials.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates,read_nums


def get_today_hot(content_type):
    today = timezone.now().date()
    read_detail = Read_detial.objects.filter(content_type=content_type,date=today).order_by('-read_num')
    return read_detail[:5]

def get_yesterday_hot(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_detail = Read_detial.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')
    return read_detail[:5]

def get_senvenday_hot(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_detail = Read_detial.objects.filter(content_type=content_type,date=date).order_by('-read_num')
    return read_detail[:5]