from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import throttle_classes, api_view
from rest_framework.response import Response
from misc.mongo import mongoDB
#from models import Ptt
#from serializers import PttSerializer
from rest_framework.throttling import UserRateThrottle
#from rest_framework.views import APIView
import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object

@api_view(['GET'])
def test(request):
    res = {'status':'ok'}
    return HttpResponse(json.dumps(res, indent=4), content_type="application/json")
    return Response({'status':'ok'})

@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def article(request, board, start_date, end_date):
    try:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return HttpResponseBadRequest('Error: date format error!')
    duration = end_date - start_date
    duration = duration.days
    duration_limit = 180
    if duration < 0:
        return HttpResponseBadRequest('Error: end date smaller than start date!')
    elif duration > duration_limit:
        return HttpResponseBadRequest('Error: time range should not be greater than %s days' % duration_limit)
    res = mongoDB('PTT', board).find({'post_time':{'$gte':start_date, '$lt':end_date}}, {'_id':0, 'title':1, 'content':1, 'post_time':1})
    res = list(res)
    return HttpResponse(json.dumps(res, ensure_ascii=False, indent=4, cls=DateTimeEncoder), content_type="application/json; charset=utf-8")


#from rest_framework.pagination import PaginationSerializer
#from django.core.paginator import Paginator
#
#@api_view(['GET'])
#@throttle_classes([UserRateThrottle])
#def thesaurus(request, word):    
#    res = getThesaurus(word)
#
#    paginator = Paginator(res, 2)
##    page = paginator.page(1)
#    page = paginator.page(int(request.GET.get('page', '1')))
#    serializer = PaginationSerializer(instance=page, context={'request':request})
#    return Response(serializer.data)
#
#
#
#@api_view(['GET'])
#@throttle_classes([UserRateThrottle])
#def sketch(request, query):
#    res = getSketch(query)
#    res = json.dumps(res, ensure_ascii=False, indent=4)
#    return HttpResponse(res, content_type="application/json")
#
#
#@csrf_exempt
#@throttle_classes([UserRateThrottle])
#def seg(request):
#    if request.method == 'POST':
#        res = request.body
#        res = json.loads(res)
#        res = res.get('test', 'invalid')
#        return HttpResponse('ok')
#        return Response({'result':res})
#    else:
#        return JsonResponse({'message':'Please use POST method!'})
#        return HttpResponse('ok')
