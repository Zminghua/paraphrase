# -*- coding: utf-8 -*-

import os
import sys
import time
import re
import yaml


def main(infile,outfile,is_pivot,config):
    
    pivot = {}
    rpivot = {}
    fin = open(infile,'r')
    fout = open(outfile,'w')
    lines = fin.readlines()
    for line in lines:
        line = line.strip().split(config['sep_p'])
        term = [ w.strip() for w in line[0:2]]
        fout.write(term[0]+chr(config['sep_1'])+term[1]+'\n')

        if is_pivot == 1:
            if not (re.search(r'['+config['punctuation'].encode('utf-8')+config['digit'].encode('utf-8')+config['alphabet'].encode('utf-8')+']',term[1]) or re.search(r'^('+config['tone'].encode('utf-8')+')$',term[1])):
                if pivot.has_key(term[0]):
                    pivot[term[0]].append(term[1])
                else:
                    pivot[term[0]] = [term[1]]

            if not (re.search(r'['+config['punctuation'].encode('utf-8')+config['digit'].encode('utf-8')+config['alphabet'].encode('utf-8')+']',term[0]) or re.search(r'^('+config['tone'].encode('utf-8')+')$',term[0])):
                if rpivot.has_key(term[1]):
                    rpivot[term[1]].append(term[0])
                else:
                    rpivot[term[1]] = [term[0]]

    if is_pivot == 1:
        for w in pivot.keys():
            if len(pivot[w]) > 1:
                for i in range(len(pivot[w])-1):
                    for j in range(i+1,len(pivot[w])):
                        fout.write(pivot[w][i]+chr(config['sep_1'])+pivot[w][j]+'\n')

        for w in rpivot.keys():
            if len(rpivot[w]) > 1:
                for i in range(len(rpivot[w])-1):
                    for j in range(i+1,len(rpivot[w])):
                        fout.write(rpivot[w][i]+chr(config['sep_1'])+rpivot[w][j]+'\n')

    fin.close()
    fout.close()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'usage : %s input output is_pivot config' % sys.argv[0]
    else:
        startTime = time.time()
        fconfig = open(sys.argv[4],'r')
        config = yaml.load(fconfig)
        fconfig.close()
        main(sys.argv[1],sys.argv[2],int(sys.argv[3]),config)
        print('Total Time : %fs!\n' % (time.time() - startTime))

