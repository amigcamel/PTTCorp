#-*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse

from segmentation.forms import segForm
#from Jseg import jieba
from PyCCS import ckip

import pickle


def main(request):
    return render_to_response(
        'segmentation.html',
        {},
        context_instance=RequestContext(request))


def jseg_res_patch(jseg_res):
    jseg_res.raw = [(x[0].encode('utf-8'), x[1]) for x in jseg_res.raw]
    return jseg_res


def seg_jseg(request):
    from Jseg import jieba
    if request.method == 'POST':
        form = segForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                if request.FILES['upload_file'] is None:
                    return HttpResponse('ok')
                upload_file = request.FILES['upload_file']
                box = form.cleaned_data['upload_file']
            else:
                box = form.cleaned_data['box']
            try:
                output = jieba.seg(box)
                output_html = output.text(mode='html')
                request.session['output'] = pickle.dumps(output)
                return render_to_response(
                    'jseg.html', {
                        'output': output_html}, context_instance=RequestContext(request))
            except BaseException:
                raise
    else:
        form = segForm(
            initial={
                'box': '強者我朋友是住在天龍國的魯蛇\n中文斷詞真的很複雜◢▆▅▄▃ 崩╰(〒皿〒)╯潰 ▃▄▅▆◣'})
    return render_to_response(
        'jseg.html', {
            'form': form}, context_instance=RequestContext(request))


def download(request, output_format, encoding="utf-8"):
    from django.core.servers.basehttp import FileWrapper
    import tempfile
    import csv

    temp = tempfile.TemporaryFile()
    output = request.session.get('output')
    if output:
        output = pickle.loads(output)
        if output_format == 'csv':
            writer = csv.writer(temp)
            writer.writerows([[word.encode(encoding)
                               for word in tup] for tup in output.raw])
        elif output_format == 'txt':
            temp.write(output.text().encode(encoding))
        else:
            return HttpResponseRedirect(reverse(seg_jseg))
        temp.flush()
        wrapper = FileWrapper(temp)
        response = HttpResponse(
            wrapper,
            content_type='text/%s' %
            output_format)
        response['Content-Disposition'] = 'attachment; filename=jseg_result.%s' % output_format
        response['Content-Length'] = temp.tell()
        temp.seek(0)
        return response
    else:
        return HttpResponseRedirect(reverse(seg_jseg))


def pyccs(request):
    if request.method == 'POST':
        form = segForm(request.POST)
        if form.is_valid():
            box = form.cleaned_data['box']
            request.session['input'] = box
            try:
                output = ckip.seg(box)
                output_html = output.text('html')
                request.session['output'] = pickle.dumps(output)
                return render_to_response(
                    'pyccs.html', {
                        'output': output_html}, context_instance=RequestContext(request))
            except BaseException:
                raise
                return render_to_response(
                    'pyccs.html', {
                        'errmsg': True}, context_instance=RequestContext(request))
    else:
        form = segForm(initial={'box': '歡迎光臨台灣大學語言學研究所LOPE實驗室'})
    return render_to_response(
        'pyccs.html', {
            'form': form}, context_instance=RequestContext(request))


def segcom(request):
    if request.method == 'POST':
        form = segForm(request.POST, request.FILES)
        if form.is_valid():
            box = form.cleaned_data['box'].strip('\r\n').strip('\n')
            try:
                output = compare_seg(box)
            except BaseException:
                return render_to_response(
                    'segcom.html', {
                        'errmsg': True}, context_instance=RequestContext(request))
            jieba_res, ckip_res = output[0], output[1]
            return render_to_response('segcom.html',
                                      {'jieba_res': jieba_res,
                                       'ckip_res': ckip_res},
                                      context_instance=RequestContext(request))
    else:
        form = segForm(
            initial={
                'box': '英國「每日郵報」（Daily Mail）報導，之前是金正日宣傳部門具有影響力的官員張振成（JangJin-sung），據悉9月在荷蘭一項會議發表這段聳人聽聞的言論。這場會議有數名流亡北韓高官參與。'})
    return render_to_response(
        'segcom.html', {
            'form': form}, context_instance=RequestContext(request))


def compare_seg(txt):
    from Jseg import jieba
    jres = jieba.seg(txt).nopos('list')
    cres = ckip.seg(txt).nopos('list')
    if len(''.join(jres)) != len(''.join(cres)):
        raise Exception(
            'Unequal length of results from Jseg and CKIP Segmentator... cannot be compared')
    source = ''.join(jres)
    cnt_j, cnt_c = 0, 0
    idxcon_j, idxcon_c = [], []
    for word in jres:
        idx = ''
        for char in word:
            idx += '_%d' % cnt_j
            cnt_j += 1
        idxcon_j.append(idx)
    for word in cres:
        idx = ''
        for char in word:
            idx += '_%d' % cnt_c
            cnt_c += 1
        idxcon_c.append(idx)

    ovlps = set(idxcon_j) & set(idxcon_c)
    output_j, output_c = '', ''
    for i in idxcon_j:
        idxs = [int(j) for j in i.split('_') if j != '']
        recv = ''.join([source[idx] for idx in idxs])
        if i in ovlps:
            output_j += recv
        else:
            output_j += '<span class="pos">%s</span>' % recv
        output_j += ' '
    for i in idxcon_c:
        idxs = [int(j) for j in i.split('_') if j != '']
        recv = ''.join([source[idx] for idx in idxs])
        if i in ovlps:
            output_c += recv
        else:
            output_c += '<span class="pos">%s</span>' % recv
        output_c += ' '
    return (output_j, output_c)
