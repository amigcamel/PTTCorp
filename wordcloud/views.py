#-*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse

import json

import sys
sys.path.append('/home/achiii/Github/pttwebcrawler')
from boardChtPatch import data


def genWordcloud(request, board_name):
    if board_name == 'Gossiping':
        from main.views import cands_ori
        cands = json.dumps(cands_ori)
    elif board_name == 'Hate':
        with open('/var/www/PTTCorp/static/wordcloud/Hate_.json') as jf:
            cands = jf.read()
    board_name = (board_name, data[board_name])
    return render_to_response('wordcloud.html',
                              {'cands': cands,
                               'board_name': board_name},
                              context_instance=RequestContext(request))
