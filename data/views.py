#-*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext

def main(request):
    return render_to_response('data.html', {}, context_instance=RequestContext(request))

