#-*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse
from intro.forms import ContactForm
from misc.mongo import connect
from misc.sendmail import gmail


def main(request):
    return render_to_response(
        'intro.html',
        {},
        context_instance=RequestContext(request))


def data(request):
    pttmeta = connect('PTTmeta', 'info')
    pttmeta = pttmeta.find({}, {'_id': 0})
    pttmeta = list(pttmeta)
    return render_to_response('data.html',
                              {'metainfo': pttmeta},
                              context_instance=RequestContext(request))


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            subject += '(sent from %s by %s)' % (email, name)
            message = form.cleaned_data['message']
            gmail(subject, message)
            request.flash['notice'] = 'Congrats! Your message has been sent successfully!'
            return HttpResponseRedirect(reverse('intro_contact'))
    else:
        if request.user.is_anonymous():
            email = None
        else:
            email = request.user.email
        form = ContactForm(initial={'email': email})
    return render_to_response(
        'contact.html', {
            'form': form}, context_instance=RequestContext(request))
