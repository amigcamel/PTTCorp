#-*-coding:utf-8-*-
from django import forms

import re

# How to use Datepicker in django
# http://stackoverflow.com/questions/20700185/how-to-use-datepicker-in-django
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

from misc.mongo import connect
BOARDS = connect('PTTmeta', 'info').find({}, {
    'board': 1,
    'board_cht': 1,
    '_id': 0
})
BOARDS = [(i['board'], i['board_cht'])
          if 'board_cht' in i else (i['board'], i['board']) for i in BOARDS]

# http://stackoverflow.com/a/16523287/1105489
from django.forms.widgets import RadioFieldRenderer
from django.shortcuts import render
from django.utils.html import format_html_join
from django.utils.encoding import force_text


class RadioFieldWithoutULRenderer(RadioFieldRenderer):
    def render(self):
        return format_html_join(
            '\n',
            '{0}',
            [(force_text(w), ) for w in self],
        )


class ConcordanceForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': "ex:強者我朋友",
            "required": "required"
        }),
        min_length=1,
        max_length=100)
    boards = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(), choices=BOARDS)
    window_size = forms.IntegerField(
        max_value=10,
        min_value=4,
        widget=forms.NumberInput(attrs={'style': 'display:none'}))
    corpus = forms.ChoiceField(
        choices=[('PTT', 'Article (文章)'), ('PTTCOM', 'Comments (推噓文)')],
        widget=forms.RadioSelect())  # attrs={'disabled':'disabled'}))
    time_order = forms.ChoiceField(
        choices=[(-1, 'Descending'), (1, 'Ascending')],
        widget=forms.RadioSelect(renderer=RadioFieldWithoutULRenderer))
    POS = forms.ChoiceField(
        choices=[('True', 'Show'), ('False', 'Hide')],
        widget=forms.RadioSelect(renderer=RadioFieldWithoutULRenderer),
        label="Part-of-Speech")
    start_date = forms.DateField(widget=DateInput(), required=False)
    end_date = forms.DateField(widget=DateInput(), required=False)

    def clean_query(self):
        query = self.cleaned_data['query']
        query = query.strip()
        if query.startswith('['):
            res1 = re.search('\[[^\]].*\]', query)
            if res1:
                if res1.group() != query:
                    raise forms.ValidationError(
                        'CQL error: Unbalanced brackets')

            if query.count('"') % 2 != 0:
                raise forms.ValidationError(
                    'CQL error: Unbalanced quotation marks (")')
            res2 = re.search('\[(\w+)="(.*?)"\]', query)
            if res2:
                attr = res2.group(1)
                if attr not in ['word', 'pos']:
                    raise forms.ValidationError(
                        'CQL error: not attribute name for "%s"' % attr)
            else:
                raise forms.ValidationError('CQL error: Invalid syntax')
        return query


class CollocationForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'ex:服貿'}),
        min_length=1,
        max_length=10)
