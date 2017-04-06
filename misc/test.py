#-*-coding:utf8-*-

from mongo import connect
from math import log

def tfidf(text, board):
    res = connect('PTT', board).find({}, {'_id':0, 'content_seg':1})
    res = [i['content_seg'] for i in res]
    res = [[i[0] for i in j] for j in res] 
    types = list(set(text)) 
    dic = {}
    for t in types:
        dic[t] = 0
    con = []
    # counting each type number appeared in the whole docs
    for doc in res:
        for t in types:
            if t in doc:
                dic[t] += 1
    for t in types:
        tf = 1.0*text.count(t)/len(text)
        idf = log(1.0*len(res)/(dic[t]+1))
        v = tf*idf
        con.append((t, v))
    return con
        

def pre_count(board):
    import itertools
    res = connect('PTT', board).find({}, {'_id':0, 'content_seg':1})
    res = [i['content_seg'] for i in res]
    res = [[i[0] for i in j] for j in res]
    types = itertools.chain.from_iterable(res)
    types = list(set(types))
    dic = {}
    for t in types:
        dic[t] = 0
    for doc in res:
        for t in types:
            print t
            if t in doc:
                dic[t] += 1
    return dic
