# -*- coding: utf-8 -*-

import os
import sys
import time
import re
import operator
import math
import yaml

stopw = []
def load_stop(stop):
    fstop = open(stop,'r')
    lines = fstop.readlines()
    for line in lines:
        stopw.append(line.strip())
    fstop.close()


def main(infile, outfile, config):

    startTime = time.time()
    fin = open(infile,'r')
    fout = open(outfile,'w')
    lines = fin.readlines()
    n = len(lines)
    idf = {}
    for i in xrange(len(lines)):
        lines[i] = [ item.strip().split(chr(config['sep_1']))[0] for item in lines[i].strip().split(config['sep_w'])]
        for w in set(lines[i]):
            if idf.has_key(w):
                idf[w] = idf[w] + 1.0
            else:
                idf[w] = 1.0

    for words in lines:
        candidate = {}
        l = len(words) + 0.0
        if (l>config['sen_max_len']) or (l<config['sen_min_len']):
            continue
        if l/len(set(words)) > config['sen_word_duplicate']:
            continue
        
        klen = 0
        for w in set(words):
            if w not in stopw:
                klen += 1
        num = min(klen, config['key_num'][klen//config['n_word_to_key']])
        if num < config['key_num_floor']:
            continue
        for w in set(words):
            if w in stopw:
                continue
            candidate[w] = (words.count(w)/l) * math.log(n/idf[w])
        candidate = sorted(candidate.iteritems(),key=operator.itemgetter(1),reverse=True)
        kwords = [ candidate[i][0]+chr(config['sep_1'])+str(candidate[i][1]) for i in xrange(num) ]
        fout.write(chr(config['sep_2']).join(kwords)+chr(config['sep_3'])+config['sep_w'].join(words)+'\n')

    fin.close()
    fout.close()
    print('Total Time : %fs!\n' % (time.time() - startTime))


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'usage : %s input output stopword config! ' % sys.argv[0]
        exit(1)
    else:
        fconfig = open(sys.argv[4],'r')
        config = yaml.load(fconfig)
        fconfig.close()
        load_stop(sys.argv[3])
        main(sys.argv[1],sys.argv[2],config)

