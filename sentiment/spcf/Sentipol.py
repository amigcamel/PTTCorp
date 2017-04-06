#-*-coding:utf-8-*-
import json
from pattern.vector import count
from os.path import realpath, dirname, join

CUR_PATH = dirname(realpath(__file__))

def sentipol(post_seg):
    '''emotion polarity (情緒極性) determiner'''
    pos_con, neg_con = [], []
    pos_cnt, neg_cnt = 0, 0
    for word in post_seg:
	if word in pos_lst:
            pos_cnt += 1
            pos_con.append(word)
	elif word in neg_lst:
	    neg_cnt += 1
            neg_con.append(word)
    diff = pos_cnt - neg_cnt        
    
    pos_fin = count(pos_con).items()
    neg_fin = count(neg_con).items()
    
    pos_fin = sorted(pos_fin, key=lambda x:x[-1], reverse=True)
    neg_fin = sorted(neg_fin, key=lambda x:x[-1], reverse=True)
  
    postmod = ' '.join(post_seg)

    for w, n in pos_fin:
        postmod = postmod.replace(w, '<span class="positive">%s</span>' % w)
    for w, n in neg_fin:
        postmod = postmod.replace(w, '<span class="negative">%s</span>' % w)

    return {'content':postmod, 'diff':diff, 'pos':pos_fin, 'neg':neg_fin}

# loading Emotion Lexicon (情緒詞表)
print 'loading Emotion Lexicon (情緒詞表)...'
with open(join(CUR_PATH, 'jieba_user_dict/dics/emo_pos.json')) as fp, open(join(CUR_PATH, 'jieba_user_dict/dics/emo_neg_ex.json')) as fn:
    pos_lst = json.load(fp)
    neg_lst = json.load(fn)
