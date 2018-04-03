#-*-coding:utf-8-*-
import json
import os

DIC_PATH = 'dics'
af = os.listdir(DIC_PATH)
af = [os.path.join(DIC_PATH, jf) for jf in af]

wlst_all = []
for jf in af:
    with open(jf) as f:
        wlst = json.load(f)
        wlst_all += wlst

fin = list(set(wlst_all))

with open('custom_dic.txt', 'w') as fd:
    for w in fin:
        fd.write('%s 200 NA\n' % w.encode('utf-8'))
