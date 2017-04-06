#-*-coding:utf-8-*-
# ref: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/
from django import template
from django.utils.safestring import mark_safe

import re

register = template.Library()

@register.filter
def keyword_sub(string):
	res = re.sub('\s\[(.*?)\]\s', '<font color="red">\\1</font>', string)
	return mark_safe(res)
# def keyword_sub(string, keyword):
#     if keyword in string:
#         res = string.replace(keyword, '<font color="red">%s</font>' % keyword)
#         return mark_safe(res)

@register.filter
def pushtag_cht(pushtag):
	if pushtag == 'push':
		pushtag = 'push (推)'
	elif pushtag == 'boo':
		pushtag = 'boo (噓)'
	elif pushtag == 'arrow':
		pushtag = 'arrow (→)'
	return pushtag

@register.filter(name='seg_patch')
def seg_patch(txt):
    txt = re.sub('_(.*?)__diff', '<span>\\1</span>', txt)
    return txt

@register.filter(name='conv_to_date')
def conv_to_date(num):
    year, month, day = num[:4], num[4:6], num[6:]
    return '%s/%s/%s' % (year, month, day)

#@register.filter(name='emo_patch')
#def emo_patch(emolst):
#    for i in emolst:
#        txt = txt.replace(i, '<span>'+i+'</span>')
#    return txt
