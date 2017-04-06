#-*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from sentiment.forms import SentipolForm

from spcf import sentipol_wrapper

def main(request):
    return render_to_response('sentiment.html', {}, context_instance=RequestContext(request))

def sentipol(request):
    if request.method == 'POST':
        form = SentipolForm(request.POST)
        if form.is_valid():
            box = form.cleaned_data['box']
            res = sentipol_wrapper.sentipol_tmp(box)
            pol = res[0]
            output = res[1]
            content = res[1]['content']
            diff = res[1]['diff']
            pos = res[1]['pos']
            neg = res[1]['neg']
            return render_to_response('sentipol.html', {'content':content, 'pol': pol, 'pos':pos, 'neg':neg}, context_instance=RequestContext(request))
    else:
        form = SentipolForm()
    return render_to_response('sentipol.html', {'form':form}, context_instance=RequestContext(request))

