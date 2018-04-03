from pattern.vector import SVM
#from Jseg import jieba
from os.path import realpath, dirname, join

CUR_PATH = dirname(realpath(__file__))
sentipol_cls = SVM.load(join(CUR_PATH, 'svm_mod.gpk'))
execfile(join(CUR_PATH, 'Sentipol.py'))


def sentipol_tmp(text):
    from Jseg import jieba
    text = jieba.seg(text).nopos().split()
    pol = sentipol_cls.classify(text)
    details = sentipol(text)
    return pol, details
