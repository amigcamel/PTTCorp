from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^test/$', 'api.views.test', name='api_test'),
    url(r'^article/([a-zA-Z_-]+)/from/([0-9-]+)/to/([0-9-]+)/$',
        'api.views.article', name='api_article'),
    #    url(r'seg/$', 'ptt.views.seg', name='seg'),
]
