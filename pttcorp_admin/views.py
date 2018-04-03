#-*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext
#from django.contrib.auth.decorators import user_passes_test
from .forms import UpdateLogModelForm
from .models import UpdateLogModel
from pttcorp_comments.forms import CommentModelForm, CommentModelReplyForm
from pttcorp_comments.models import CommentModel
import datetime

REDIRECT_URL = 'index'


def super_user_auth(func):
    def check_super_user(*args, **kwargs):
        if args[0].user.is_superuser:
            return func(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(REDIRECT_URL))

    return check_super_user


@super_user_auth
def updateLogView(request):
    update_log = UpdateLogModel.objects.all()
    update_log = reversed(update_log)

    form = UpdateLogModelForm(request.POST)
    if form.is_valid():
        update_message = form.cleaned_data['update_message']
        #update_datetime = form.cleaned_data['update_datetime']
        UpdateLogModel.objects.create(update_message=update_message)
        return HttpResponseRedirect(reverse('update_log'))
    else:
        form = UpdateLogModelForm()
    return render_to_response(
        'update_log.html', {
            'form': form,
            'update_log': update_log
        },
        context_instance=RequestContext(request))


@super_user_auth
def updateLogFunc(request, func, db_id):
    if func == "modify":
        obj = UpdateLogModel.objects.get(id=db_id)
        ori_msg = obj.update_message
        update_log = reversed(UpdateLogModel.objects.all())
        edit_form = UpdateLogModelForm(request.POST)
        if edit_form.is_valid():
            mod_message = edit_form.cleaned_data['update_message']
            obj.update_message = mod_message
            obj.save()
            return HttpResponseRedirect(reverse('update_log'))
        else:
            edit_form = UpdateLogModelForm(initial={'update_message': ori_msg})
        return render_to_response(
            'update_log.html', {
                'edit_form': edit_form,
                'update_log': update_log
            },
            context_instance=RequestContext(request))
    elif func == 'delete':
        UpdateLogModel.objects.filter(id=db_id).delete()
    else:
        pass
    return HttpResponseRedirect(reverse('update_log'))


#@user_passes_test(test_func=lambda u: u.is_superuser, login_url='index')


@super_user_auth
def messageBoardView(request):
    comments = reversed(CommentModel.objects.all())
    return render_to_response(
        'message_board.html', {'comments': comments},
        context_instance=RequestContext(request))


@super_user_auth
def messageBoardFunc(request, func, db_id):
    comment = CommentModel.objects.get(id=db_id)
    reply_form = CommentModelReplyForm(request.POST)
    if request.method == 'POST':
        if reply_form.is_valid():
            reply = reply_form.cleaned_data['reply']
            comment.reply = reply
            comment.reply_datetime = datetime.datetime.now()
            comment.save()
            return HttpResponseRedirect(reverse('message_board'))
    else:
        reply = CommentModelReplyForm()
    return render_to_response(
        'message_board.html', {
            'reply_form': reply_form,
            'comment': comment
        },
        context_instance=RequestContext(request))
