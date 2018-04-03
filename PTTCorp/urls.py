from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from main.views import *

import intro.views
import segmentation.views
import sketch.views
import sentiment.views
import api.views
import wordcloud.views

from django.contrib import admin
admin.autodiscover()

from registration.backends.default.views import RegistrationView
from main.forms import RegForm

# This is the decorator which only allows super to access certain pages
from pttcorp_admin.views import super_user_auth

urlpatterns = patterns(
    '',
    url('^$', index, name='index'),
    url('^intro/$', intro.views.main, name='intro_main'),
    url('^contact/$', intro.views.contact, name='intro_contact'),
    url('^data/$', intro.views.data, name='intro_data'),
    url('^segmentation/$', segmentation.views.main, name='segmentation_main'),
    url('^jseg/$', segmentation.views.seg_jseg, name='segmentation_jseg'),
    url('^pyccs/$', segmentation.views.pyccs, name='segmentation_pyccs'),
    url('^segcom/$', segmentation.views.segcom, name='segmentation_segcom'),
    url('^download_res/(\w+)/$',
        segmentation.views.download,
        name="download_res"),
    url('^sketch/$', sketch.views.main, name='sketch_main'),
    url('^concordance/$', sketch.views.concordance, name='sketch_concordance'),
    url('^collocation/$', sketch.views.collocation, name='sketch_collocation'),
    url('^source/([a-zA-Z0-9_-]+)/(\w+)/(.+)/$',
        sketch.views.source,
        name='sketch_source'),
    url('^sentiment/$', sentiment.views.main, name='sentiment_main'),
    url('^sentipol/$', sentiment.views.sentipol, name='sentiment_sentipol'),
    url('^api/$', TemplateView.as_view(template_name='api.html'), name="api"),
    url('^api/', include('api.urls')),
    url('^wordcloud/$',
        TemplateView.as_view(template_name='wordcloud.html'),
        name="wordcloud_main"),
    url('^wordcloud/(\w+)/$',
        wordcloud.views.genWordcloud,
        name='genWordcloud'),
    url('^pttcorp_admin/$',
        super_user_auth(TemplateView.as_view(template_name='admin_base.html')),
        name="pttcorp_admin"),
    url('^pttcorp_admin/', include('pttcorp_admin.urls')),
    url(r'^accounts/register/$',
        RegistrationView.as_view(form_class=RegForm),
        name='registration_register'),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^captcha/', include('captcha.urls')),
    #    url(r'^admin/', include(admin.site.urls)),
    (r'^facebook/', include('django_facebook.urls')),
)
