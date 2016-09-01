# -*- coding: utf-8 -*-

import os
import sys
import time
import re
import yaml

wordnet = {}
model = {}

def load_net(net):
    fnet = open(net,'r')
    lines = fnet.readlines()
    index = 1
    for line in lines:
        line = line.strip().split(' ')[1:]
        if len(line)>1:
            for w in line:
                wordnet[w.strip().decode('cp936').encode('utf-8')] = index
        index += 1
    fnet.close()


def load_lm(lm,config):
    flm = open(lm,'r')
    lines = flm.readlines()
    for line in lines:
        if line[0] != '-':
            continue
        line = line.strip().split('\t')
        if re.search(r'['+config['punctuation'].encode('utf-8')+config['digit'].encode('utf-8')+config['alphabet'].encode('utf-8')+']',line[1].strip()):
            continue
        model[line[1].strip()]=[float(line[0].strip())]
        if len(line) == 3:
            model[line[1].strip()].append(float(line[2].strip()))
    flm.close()


def bigram(term):
    if model.has_key(' '.join(term)):
        return model[' '.join(term)][0]
    else:
        return model[term[1]][0]+model[term[0]][1]


def trigram(term):
    if model.has_key(' '.join(term)):
        return model[' '.join(term)][0]
    elif model.has_key(' '.join(term[0:2])):
        return model[' '.join(term[0:2])][1]+bigram(term[1:3])
    else:
        return bigram(term[1:3])


def fluent(terms):
    fvalue = []
    terms = [t.strip().split(' ') for t in terms]
    for term in terms:
        if len(term) == 1:
            fvalue.append(0.0)
        elif len(term) == 2:
            fvalue.append(bigram(term))
        else:
            temp = 0.0
            for i in range(3,len(term)+1):
                temp += trigram(term[(i-3):i])
            fvalue.append(temp)
    return fvalue


def main(infile,outfile,config):

    plen = 0
    phrase = {}
    fin = open(infile,'r')
    fout = open(outfile,'w')
    lines = fin.readlines()
    for line in lines:
        line = line.strip()
        term = [ w.strip() for w in line.split(chr(config['sep_1']))]
        if re.search(r'['+config['punctuation'].encode('utf-8')+config['digit'].encode('utf-8')+config['alphabet'].encode('utf-8')+']',term[0]) or re.search(r'['+config['punctuation'].encode('utf-8')+config['digit'].encode('utf-8')+config['alphabet'].encode('utf-8')+']',term[1]):
            continue
        
        word0 = ''.join(term[0].strip().split(config['sep_w']))
        word1 = ''.join(term[1].strip().split(config['sep_w']))
        if wordnet.has_key(word0) and wordnet.has_key(word1):
            if wordnet[word0] == wordnet[word1]:
                if word0 != word0:
                    print term[0]+','+term[1]
                continue
        
        if (term[0] in term[1]) or (term[1] in term[0]):
            continue
        if re.search(r'^('+config['tone']+')$',term[0]) or re.search(r'^('+config['tone']+')$',term[1]):
            continue
        
        #fvalue = fluent(term[0:2])
        #if fvalue[0] < config[phrase_fluent_floor] and fvalue[1] < config[phrase_fluent_floor]:
        #    continue
        
        rline = term[1]+chr(config['sep_1'])+term[0]
        if phrase.has_key(line):
            phrase[line] += 1
        elif phrase.has_key(rline):
            phrase[rline] += 1
        else:
            phrase[line] = 1

    for p in phrase.keys():
        if phrase[p] >= config['phrase_freq_floor']:
            fout.write(p+chr(config['sep_1'])+str(phrase[p])+'\n')

    fin.close()
    fout.close()


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'usage : %s input output lm wordnet config ! ' % sys.argv[0]
    else:
        startTime = time.time()
        fconfig = open(sys.argv[5],'r')
        config = yaml.load(fconfig)
        fconfig.close()
        
        load_lm(sys.argv[3],config)
        load_net(sys.argv[4])
        main(sys.argv[1],sys.argv[2],config)
        
        print('Total Time : %fs!\n' % (time.time() - startTime))

