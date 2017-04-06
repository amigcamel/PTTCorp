from django.conf.urls import patterns, url

import pttcorp_admin.views

urlpatterns = patterns('',
                       url('^update_log/$', pttcorp_admin.views.updateLogView, name='update_log'), 
                       url('^updateLogFunc/(\w+)/(\d+)/$', pttcorp_admin.views.updateLogFunc, name='updateLogFunc'),
                       url('^message_board/$', pttcorp_admin.views.messageBoardView, name='message_board'),
                       url('^messageBoardFunc/(\w+)/(\d+)/$', pttcorp_admin.views.messageBoardFunc, name='messageBoardFunc'),
                       )
