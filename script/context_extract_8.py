# -*- coding: utf-8 -*-

import os
import sys
import time
import math
import re
import yaml
import numpy as np

left = {}
right = {}
cans = []
norm = {}

def LSH(can,llen,rlen,h,config):
    lfea0 = []
    lfea1 = []
    for w in set(left[can[0]].keys()+left[can[1]].keys()):
        w0 = left[can[0]][w] if left[can[0]].has_key(w) else 0.0
        lfea0.append(w0)
        w1 = left[can[1]][w] if left[can[1]].has_key(w) else 0.0
        lfea1.append(w1)
    v1 = np.sign( np.array(lfea0).dot(h[0:llen,:]) )
    v2 = np.sign( np.array(lfea1).dot(h[0:llen,:]) )
    leftsim = math.cos(np.flatnonzero(v1-v2).size*math.pi/config['LSH_bit'])

    rfea0 = []
    rfea1 = []
    for w in set(right[can[0]].keys()+right[can[1]].keys()):
        w0 = right[can[0]][w] if right[can[0]].has_key(w) else 0.0
        rfea0.append(w0)
        w1 = right[can[1]][w] if right[can[1]].has_key(w) else 0.0
        rfea1.append(w1)
    v1 = np.sign( np.array(rfea0).dot(h[0:rlen,:]) )
    v2 = np.sign( np.array(rfea1).dot(h[0:rlen,:]) )
    rightsim = math.cos(np.flatnonzero(v1-v2).size*math.pi/config['LSH_bit'])
    return leftsim,rightsim


def cosine(can):
    leftsum = 0.0
    for w in set(left[can[0]].keys()+left[can[1]].keys()):
        w0 = left[can[0]][w] if left[can[0]].has_key(w) else 0.0
        w1 = left[can[1]][w] if left[can[1]].has_key(w) else 0.0
        leftsum += w0*w1
    leftsim = leftsum/( norm[can[0]][0] * norm[can[1]][0] )
        
    rightsum = 0.0
    for w in set(right[can[0]].keys()+right[can[1]].keys()):
        w0 = right[can[0]][w] if right[can[0]].has_key(w) else 0.0
        w1 = right[can[1]][w] if right[can[1]].has_key(w) else 0.0
        rightsum += w0*w1
    rightsim = rightsum/( norm[can[0]][1] * norm[can[1]][1] )
    return leftsim,rightsim


def overlap(phrase1,phrase2,config):
    wordset1 = set()
    wordset2 = set()
    for w in phrase1.decode('utf-8').strip().split(config['sep_w']):
        wordset1 = wordset1.union(list(w))
    for w in phrase2.decode('utf-8').strip().split(config['sep_w']):
        wordset2 = wordset2.union(list(w))
    return (len((wordset1 & wordset2)-set(config['tone'].strip().split('|'))) + 0.0) / len(wordset1 | wordset2)


def main(infile,outfile,context,config):
    
    h = np.random.normal(0,1,[config['LSH_dim'],config['LSH_bit']])
    fin = open(infile,'r')
    fcorpus = open(context,'r')
    fout = open(outfile,'w')
    lines = fin.readlines()
    for line in lines:
        term = [ w.strip() for w in line.strip().split(chr(config['sep_1']))]
        cans.append(term)
        if not left.has_key(term[0]):
            left[term[0]] = {}
            right[term[0]] = {}
        if not left.has_key(term[1]):
            left[term[1]] = {}
            right[term[1]] = {}

    lines = fcorpus.readlines()
    for line in lines:
        line = line.strip().split(config['sep_w'])
        span = min(config['max_phrase_len'], len(line))
        for i in range(span):
            end = len(line) - i
            for j in range(end):
                phrase = ' '.join(line[j:j+i+1])
                if left.has_key(phrase):
                    for k in range(config['context_window']):
                        if j-k > 0:
                            if left[phrase].has_key(line[j-1-k]):
                                left[phrase][line[j-1-k]] += 1.0
                            else:
                                left[phrase][line[j-1-k]] = 1.0
                        else:
                            if left[phrase].has_key(config['sen_start']):
                                left[phrase][config['sen_start']] += 1.0
                            else:
                                left[phrase][config['sen_start']] = 1.0

                        if j+i+1+k < len(line):
                            if right[phrase].has_key(line[j+i+1+k]):
                                right[phrase][line[j+i+1+k]] += 1.0
                            else:
                                right[phrase][line[j+i+1+k]] = 1.0
                        else:
                            if right[phrase].has_key(config['sen_end']):
                                right[phrase][config['sen_end']] += 1.0
                            else:
                                right[phrase][config['sen_end']] = 1.0

    for phrase in left.keys():
        lweight = np.array(left[phrase].values())
        rweight = np.array(right[phrase].values())
        norm[phrase] = [np.sqrt(lweight.dot(lweight)), np.sqrt(rweight.dot(rweight))]
   
    for can in cans:
        if [can[1],can[0]] in cans:
            if cans.index([can[1],can[0]]) > cans.index(can):
                continue
        
        lsim = 0.0
        rsim = 0.0
        llen = len(set(left[can[0]].keys()+left[can[1]].keys()))
        rlen = len(set(right[can[0]].keys()+right[can[1]].keys()))
        #if llen > 128 and rlen > 128:
        #    lsim,rsim = LSH(can,llen,rlen)
        #else:
        lsim,rsim = cosine(can)
        
        sim = lsim*config['context_left_weight'] + rsim*config['context_right_weight']
        if lsim > config['context_left_sim_floor'] and rsim > config['context_right_sim_floor'] :

            if overlap(can[0],can[1],config) > config['phrase_overlap_floor']:
                fout.write(can[0]+chr(config['sep_1'])+can[1]+chr(config['sep_1'])+'sim='+str(sim)+',lsim='+str(lsim)+',rsim='+str(rsim)+',lset0='+str(len(set(left[can[0]].keys())))+',lset1='+str(len(set(left[can[1]].keys())))+',lunion='+str(llen)+',linter='+str(len(set(left[can[0]].keys()) & set(left[can[1]].keys())))+',rset0='+str(len(set(right[can[0]].keys())))+',rset1='+str(len(set(right[can[1]].keys())))+',runion='+str(rlen)+',rinter='+str(len(set(right[can[0]].keys()) & set(right[can[1]].keys())))+'\n')
        else:
            print can[0]+','+can[1]+','+str(lsim)+','+str(rsim)+','+str(llen)+','+str(rlen)


    fin.close()
    fcorpus.close()
    fout.close()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'usage : %s input output context config' % sys.argv[0]
    else:
        startTime = time.time()
        fconfig = open(sys.argv[4],'r')
        config = yaml.load(fconfig)
        fconfig.close()
        main(sys.argv[1],sys.argv[2],sys.argv[3],config)
        print('Total Time : %fs!\n' % (time.time() - startTime))

