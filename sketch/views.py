#-*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext
from misc.cqpapi import Cqp
from misc.mongo import connect
from sketch.forms import ConcordanceForm, CollocationForm
from bson.objectid import ObjectId
from naturalCQP import ncqp
import json, urllib, re

def main(request):
    return render_to_response('sketch.html', {}, context_instance=RequestContext(request))

def concordance(request):
    if 'query' in request.GET:
        form = ConcordanceForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            window_size = form.cleaned_data['window_size']
            corpus = form.cleaned_data['corpus']
            time_order = int(form.cleaned_data['time_order'])
            show_pos = form.cleaned_data['POS']
            start_date = form.cleaned_data['start_date']
            if start_date:
                start_date = int(str(start_date).replace('-', ''))
            end_date = form.cleaned_data['end_date']
            if end_date:
                end_date = int(str(end_date).replace('-', ''))
            boards = form.cleaned_data['boards']
            
            if show_pos == 'True':
                show_pos = True
            elif show_pos == 'False':
                show_pos = False
            if request.user.is_authenticated():
                rsize = None
            else:
                rsize = 5000
            cqp = Cqp(corpus_name=corpus, window_size=window_size, time_order=time_order)
            # cqp.find(query.encode('utf-8'), rsize=rsize, show_pos=show_pos, begin_time=start_date, end_time=end_date, board_list=boards)
            if query.startswith('>>>'):
                query = ncqp(query[3:])

            query = query.encode('utf-8')

            cqp.find(query, show_pos=show_pos, begin_time=start_date, end_time=end_date, board_list=boards)
            # output = cqp.conclst
            output = cqp.conclst[:rsize]
            if corpus == 'PTT':
                freq_by_year = [{'year':str(year), 'count':float('%.4f' % (count*100))} for year, count in cqp.freq_by_year.iteritems()]
                freq_by_year.sort(key=lambda x:x['year'])
                freq_by_year = json.dumps(freq_by_year)
            if output == []:
                request.flash['notice'] = '*No result with "%s"' % query
                return HttpResponseRedirect(reverse('sketch_concordance'))

            return render_to_response('concordance.html', {'output':output, 'query':query, 'window_size':window_size, 'time_order':time_order, 'freq_by_year':freq_by_year, 'show_pos':repr(show_pos)}, context_instance=RequestContext(request))
    else:
        form = ConcordanceForm(initial={'window_size':6, 'corpus':'PTT', 'time_order':-1, 'POS':False})
    return render_to_response('concordance.html',{'form': form}, context_instance=RequestContext(request))

def source(request, board, mongoid, query):
    query = query.replace(' ', '').strip()
    res = connect('PTT', board).find({'_id':ObjectId(mongoid)}, {'_id':0, 'URL':1, 'content':1, 'post_time':1, 'author':1, 'title':1})
    res = res.next()
    res[u'board'] = board
    if urllib.urlopen(res['URL']).getcode() == 404:
        res['URL'] = u'deleted'
    res[u'content'] = re.sub(u'('+query+u')', u'<span>\\1</span>', res[u'content'])
    return render_to_response('source.html', {'output':res}, context_instance=RequestContext(request))

def collocation(request):
    if request.method == 'POST':
        form = CollocationForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            res = connect('PTTcollo', 'collo').find({'_id':query}, {'collos':1, 'occ':1})
            try:
                res = res.next()
                occ, output = res['occ'], res['collos']
                return render_to_response('collocation.html', {'output':output, 'query':query, 'occ':occ}, context_instance=RequestContext(request))
            except:
                request.flash['notice'] = '*No result with "%s"' % query
                return HttpResponseRedirect(reverse('sketch_collocation'))
    else:
        form = CollocationForm(initial={'minimum_frequency':10,
                                   'minimum_logDice':0,
                                   'maxinum_number_of_items_displayed_in_a_grammatical_relation':30
                                  })
    return render_to_response('collocation.html', {'form':form}, context_instance=RequestContext(request))
