#-*-coding:utf-8-*-
from django import forms
from .models import CommentModel


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        labels = {'username': u'使用者', 'message': u'留言'}
        fields = (
            'username',
            'message',
        )
        widgets = {
            'username':
            forms.TextInput(attrs={
                'required': 'required',
                'class': 'form-control'
            }),
            'message':
            forms.Textarea(attrs={'required': 'required'})
        }


class CommentModelReplyForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('reply', )
        widgets = {
            'reply':
            forms.Textarea(attrs={
                'required': 'required',
                'class': 'form-control'
            })
        }
