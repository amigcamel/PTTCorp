#-*-coding:utf8-*-
from __future__ import division
from collections import OrderedDict
from CWB.CL import Corpus
import PyCQP_interface
from datetime import datetime
import os
import re
from mongo import connect


class Cqp(object):
    def __init__(self, window_size=6, corpus_name='PTT', time_order=-1):
        self.window_size = window_size
        self.corpus_name = corpus_name
        self.time_order = time_order
        self.freq_by_month = OrderedDict()
        ms = [
            201406,
            201407,
            201408,
            201409,
            201410,
            201411,
            201412,
            201501,
            201502,
            201503,
            201504,
            201505]
        for m in ms:
            self.freq_by_month[m] = 0

    def find(
            self,
            token,
            begin_time=20140601,
            end_time=20150531,
            board_list=['Gossiping']):
        if begin_time:
            if not isinstance(begin_time, int):
                raise TypeError('"begin_time" should be an "int"')
        if end_time:
            if not isinstance(end_time, int):
                raise TypeError('"end_time" should be an "int"')
        if board_list:
            if not isinstance(board_list, list):
                raise TypeError('"board_list" should be a "list"')

        self.conclst = []
        registry_dir = '/usr/local/share/cwb/registry'
        cqp = PyCQP_interface.CQP(
            bin='/usr/local/bin/cqp',
            options='-c -r ' + registry_dir)
        cqp.Exec(self.corpus_name + ";")
        cqp.Query('[word="%s"];' % token)

        rsize = int(cqp.Exec("size Last;"))
        self.results = cqp.Dump(first=0, last=rsize)
        os.system('kill -9 $(pidof cqp)')
        if self.results == [['']]:
            return None

        corpus = Corpus(self.corpus_name, registry_dir=registry_dir)
        words = corpus.attribute("word", "p")

        ids = corpus.attribute("text_id", "s")
        boards = corpus.attribute("text_board", "s")
        ptimes = corpus.attribute("text_time", "s")
        for num, line in enumerate(self.results, 1):
            print num
            output = dict()
            start = int(line[0])
            end = int(line[1]) + 1

            # post_time filter
            ptime = ptimes.find_pos(start)[-1]
            if begin_time is not None and end_time is not None:
                if begin_time <= int(ptime) <= end_time:
                    pass
                else:
                    continue
            elif begin_time is not None and end_time is None:
                if int(ptime) < begin_time:
                    continue

            elif begin_time is None and end_time is not None:
                if int(ptime) > end_time:
                    continue

            # board_list filter
            board = boards.find_pos(start)[-1]

            if board_list:
                if board not in board_list:
                    continue

            lw = words[start - self.window_size:start]
            rw = words[end:end + self.window_size]
            qw = words[start:end]

            left = ' '.join(['%s' % word for word in lw])
            mid = ' '.join(['%s' % word for word in qw])
            right = ' '.join(['%s' % word for word in rw])

            mongoid = ids.find_pos(start)[-1]

            ptime = int(str(ptime)[:-2])
            print ptime
            self.freq_by_month[ptime] += 1

            output['conc'] = (left, mid, right)
            output['board'] = board
            output['post_time'] = ptime
            output['mongoid'] = mongoid

            self.conclst.append(output)
        if self.time_order == -1:
            rev = True
        elif self.time_order == 1:
            rev = False
        else:
            raise ValueError('time order should be either 1 or -1')
        self.conclst.sort(key=lambda x: x['post_time'], reverse=rev)
