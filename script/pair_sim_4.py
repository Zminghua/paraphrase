# -*- coding: utf-8 -*-

import os
import sys
import time
import re
import numpy as np
import operator
import yaml
import multiprocessing

def LSH(h,config):
    for i in xrange(n):
        posti = set(post[i][0].keys())

    for w in set(left[can[0]].keys()+left[can[1]].keys()):
        w0 = left[can[0]][w] if left[can[0]].has_key(w) else 0.0
        lfea0.append(w0)
        w1 = left[can[1]][w] if left[can[1]].has_key(w) else 0.0
        lfea1.append(w1)
    v1 = np.sign( np.array(lfea0).dot(h[0:llen,:]) )
    v2 = np.sign( np.array(lfea1).dot(h[0:llen,:]) )
    leftsim = math.cos(np.flatnonzero(v1-v2).size*math.pi/config['LSH_bit'])


def main(infile,ne,path,s,config):

    h = np.random.normal(0,1,[config['LSH_dim'],config['LSH_bit']])
    flog = open(path+'/log.4.'+ne,'w')
    flog.write('Process %s !\n' % (ne))
    post = []
    startTime = time.time()
    fin = open(infile+'.'+ne,'r')
    lines = fin.readlines()
    n = len(lines)
    for i in xrange(n):
        line = lines[i].strip().split(chr(config['sep_3']))
        num = len(line[1].strip().split(config['sep_w']))
        keywords = [ item.strip()[::-1].split(chr(config['sep_1']),1) for item in line[0].strip().split(chr(config['sep_2'])) ]
        post.append( [{ w[1][::-1]:float(w[0][::-1]) for w in keywords }, num, i] )
        weight = np.array(post[i][0].values())
        post[i].append(np.sqrt(weight.dot(weight)))

    fout = open(infile+'.'+ne+'.sim','w')
    post.sort(key=operator.itemgetter(1))
    lens = list(zip(*post)[1])
    pointer = {}
    pointer[config['sen_max_len']+1] = n
    for i in xrange(config['sen_max_len'],0,-1):
        if i in lens:
            pointer[i] = lens.index(i)
        else:
            pointer[i] = pointer[i+1]

    tempTime = time.time()
    for i in xrange(s,n):
        if i % 5000 == 0 :
            flog.write('%s time : %fs!\n' % (ne, time.time() - tempTime))
            tempTime = time.time()

        posti = set(post[i][0].keys())
        l = min(post[i][1]+config['sen_word_span'],config['sen_max_len']+1)
        for j in xrange(i+1,pointer[l]):
            postj = set(post[j][0].keys())
            lap = config['key_overlap_floor'][min(len(posti),len(postj))]
            if len(posti & postj) < lap:
                continue
            wsum = 0.0
            
            flog.write('i = '+str(i)+'\t'+str(post[i][2]+1)+' '+str(post[i][1])+'-'+str(post[j][2]+1)+' '+str(post[j][1])+' > '+str(len(posti & postj))+'\n')

            for w in posti|postj:
                wi = post[i][0][w] if post[i][0].has_key(w) else 0.0
                wj = post[j][0][w] if post[j][0].has_key(w) else 0.0
                wsum += wi*wj
            fout.write(str(wsum/(post[i][3]*post[j][3]))+chr(config['sep_5'])+str(post[i][2])+chr(config['sep_4'])+lines[post[i][2]].strip()+chr(config['sep_5'])+str(post[j][2])+chr(config['sep_4'])+lines[post[j][2]].strip()+'\n')

    fout.close()
    fin.close()
    flog.write('%s total time : %fs!\n' % (ne, time.time() - startTime))
    flog.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'usage : %s input path config ! ' % sys.argv[0]
        exit(1)
    else:
        fconfig = open(sys.argv[3],'r')
        config = yaml.load(fconfig)
        fconfig.close()
        
        neprocess = []
        neprocess.append(multiprocessing.Process(target = main, args = (sys.argv[1],'no',sys.argv[2],0,config,)))
        neprocess.append(multiprocessing.Process(target = main, args = (sys.argv[1],'nh',sys.argv[2],0,config,)))
        neprocess.append(multiprocessing.Process(target = main, args = (sys.argv[1],'ni',sys.argv[2],0,config,)))
        neprocess.append(multiprocessing.Process(target = main, args = (sys.argv[1],'ns',sys.argv[2],0,config,)))
        for process in neprocess:
            process.start()
        for process in neprocess:
            process.join()

