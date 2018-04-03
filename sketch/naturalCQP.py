#-*-coding:utf8-*-
import itertools


def ncqp(s):
    if not isinstance(s, unicode):
        try:
            s = s.decode('utf-8')
        except BaseException:
            raise
    combinatorics = itertools.product([True, False], repeat=len(s) - 1)

    solution = []
    for combination in combinatorics:
        i = 0
        one_such_combination = [s[i]]
        for slab in combination:
            i += 1
            if not slab:  # there is a join
                one_such_combination[-1] += s[i]
            else:
                one_such_combination += [s[i]]
        solution.append(one_such_combination)
    res = '|'.join([''.join(['[word="%s"]' % i for i in j]) for j in solution])
    return res


#import re
#
#
# def ncqp(s):
#    if not isinstance(s, unicode):
#        try:
#            s = s.decode('utf-8')
#        except:
#            raise
#    l = len(s)
#    res = [[s[idx:idx+width+1] for idx in range(l) if width+idx< l] for width in range(l)]
#    res = '|'.join([''.join(['[word="%s"]' % i for i in j]) for j in res])
#    return res

# def ncqp(string):
#     x = '...'
#     X = '[]'
#     if 'x' in string: #\x should be considered
#         res = re.split('((?:x){1,})', string)
#         output = ''
#         for i in res:
#             if i != '':
#                 output += re.sub('(.*)', '[word="\\1"]', i)
#     else:
#         output = string
#     print output
