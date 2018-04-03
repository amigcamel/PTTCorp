#-*-coding:utf-8-*-

import mongo
from datetime import datetime

year_con = dict()

for i in xrange(2001, datetime.today().year + 1):
    year_con[i] = 0


BOARDS = mongo.connect('PTTmeta', 'info').find(
    {}, {'_id': 0, 'board': 1, 'board_cht': 1})
BOARDS = dict([(i['board'], i['board_cht']) if 'board_cht' in i else (
    i['board'], i['board']) for i in BOARDS])


for board in BOARDS:
    res = mongo.connect('PTT', board).find(
        {}, {'_id': 0, 'content_seg': 1, 'post_time': 1})
    for doc in res:
        year = doc['post_time'].year
        content_seg = doc['content_seg']
        toknum = len(content_seg)
        print board, year, toknum
        year_con[year] += toknum


newdic = dict()

for k, v in year_con.iteritems():
    newdic[str(k)] = v


DB_PTTmeta.meta.save({'toknumByYear': newdic})
