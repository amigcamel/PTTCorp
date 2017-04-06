#-*-coding:utf8-*-
from __future__ import division
from CWB.CL import Corpus
import PyCQP_interface
from datetime import datetime
import os
import re
from mongo import connect

BOARDREF = connect('PTTmeta', 'info').find({}, {'_id':0, 'board':1, 'board_cht':1})
BOARDREF = dict([(i['board'], i['board_cht']) if i.has_key('board_cht') else (i['board'], i['board']) for i in BOARDREF])

toknumByYear = connect('PTTmeta', 'meta').find({}, {'_id':0, 'toknumByYear':1})
toknumByYear = toknumByYear.next()['toknumByYear']

class Cqp(object):
    def __init__(self, window_size=6, corpus_name='PTT', time_order=-1):
        self.window_size = window_size
        self.corpus_name = corpus_name
        self.time_order = time_order
        self.freq_by_year = dict()

    def find(self, token, rsize=None, show_pos=False, begin_time=None, end_time=None, board_list=None):
        if begin_time:
            if not isinstance(begin_time, int):
                raise TypeError('"begin_time" should be an "int"')
        if end_time:
            if not isinstance(end_time, int):
                raise TypeError('"end_time" should be an "int"')
        if board_list:
            if not isinstance(board_list, list):
                raise TypeError('"board_list" should be a "list"')

        for i in xrange(2001, datetime.today().year+1):
            self.freq_by_year[i] = 0
        self.conclst = []
        registry_dir='/usr/local/share/cwb/registry'
        cqp=PyCQP_interface.CQP(bin='/usr/local/bin/cqp',options='-c -r '+registry_dir)
        cqp.Exec(self.corpus_name+";")
        if token.startswith('['):
            wildcard='.'
            for i in reversed(range(1,6)):
                token = token.replace(wildcard*i, wildcard*i*3)
#                    token = re.sub('(\[word=")(%s)("\])' % (wildcard*i), '\\1%s\\3' % (wildcard*i*3), token)
#                else:
#                    token = re.sub('(\[word=")(%s)("\])' % (wildcard*i), '\\1\\2|%s\\3' % (wildcard*i*3), token)
            cqp.Query(token)
        else:
            cqp.Query('[word="%s"];' % token)
        if rsize == None:
            rsize=int(cqp.Exec("size Last;"))
        self.results=cqp.Dump(first=0,last=rsize)
        os.system('kill -9 $(pidof cqp)')
        if self.results == [['']]:
            return 'nores'

        corpus = Corpus(self.corpus_name,registry_dir=registry_dir);
        words = corpus.attribute("word","p")
        if show_pos == True:
            postags = corpus.attribute("pos","p")
        elif show_pos == False:
            pass
        else:
            raise
    #    sentences = corpus.attribute("s","s") -> find position in sentences (line number)
        ids = corpus.attribute("text_id","s")
        boards = corpus.attribute("text_board", "s")
        ptimes = corpus.attribute("text_time", "s")
        for line in self.results:
            output = dict()
            start = int(line[0])
            end = int(line[1])+1

            # post_time filter
            ptime = ptimes.find_pos(start)[-1]
            if begin_time != None and end_time != None:
                if begin_time <= int(ptime) <= end_time:
                   pass
                else:
                    continue
            elif begin_time != None and end_time == None:
                if int(ptime) < begin_time:
                    continue

            elif begin_time == None and end_time != None:
                if int(ptime) > end_time:
                    continue           

            # board_list filter
            board = boards.find_pos(start)[-1]

            if board_list:
                if board not in board_list:
                    continue

            lw = words[start-self.window_size:start]
            rw = words[end:end+self.window_size]
            qw = words[start:end]

            if show_pos is True:
                lp = postags[start-self.window_size:start]
                rp = postags[end:end+self.window_size]
                qp = postags[start:end]             

                left = ' '.join(['%s<span>/%s</span>' % (word, pos) for word, pos in zip(lw, lp)])
                mid = ' '.join(['%s<span>/%s</span>' % (word, pos) for word, pos in zip(qw, qp)])
                right = ' '.join(['%s<span>/%s</span>' % (word, pos) for word, pos in zip(rw, rp)])     

            elif show_pos is False:
                left = ' '.join(['%s' % word for word in lw])
                mid = ' '.join(['%s' % word for word in qw])
                right = ' '.join(['%s' % word for word in rw])     


#           s_bounds = sentences.find_pos(end-1)
            mongoid = ids.find_pos(start)[-1]
            if self.corpus_name == 'PTT':
                self.freq_by_year[int(ptime[:4])] += 1
            output['conc'] = (left, mid, right)
            output['board'] = board
            output['post_time'] = ptime
            output['mongoid'] = mongoid
            output['board_cht'] = BOARDREF[board]
            self.conclst.append(output)
        if self.time_order == -1:
            rev = True
        elif self.time_order == 1:
            rev = False
        else:
            raise ValueError('time order should be either 1 or -1')
        self.conclst.sort(key=lambda x: x['post_time'], reverse=rev)

        if self.corpus_name == 'PTT':
            for y in self.freq_by_year.iterkeys():
                if y in self.freq_by_year and y in toknumByYear:
                    self.freq_by_year[y] = self.freq_by_year[y]/toknumByYear[str(y)]
