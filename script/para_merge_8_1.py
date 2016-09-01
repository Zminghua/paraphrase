# -*- coding: utf-8 -*-

import os
import sys
import time
import math
import re
import yaml
        

def main(infile,paralib,config):
    
    para = []
    info = []
    flib = open(paralib,'r')
    lines = flib.readlines()
    for line in lines:
        term = [ w.strip() for w in line.strip().split(chr(config['sep_1']))]
        para.append(term[0:2])
        info.append(term[2])
    flib.close()

    fin = open(infile,'r')
    lines = fin.readlines()
    for line in lines:
        term = [ w.strip() for w in line.strip().split(chr(config['sep_1']))]
        if term[0:2] in para:
            info[para.index(term[0:2])] = term[2]
        elif term[1::-1] in para:
            info[para.index(term[1::-1])] = term[2]
        else:
            para.append(term[0:2])
            info.append(term[2])
    fin.close()

    flib = open(paralib,'w')
    for i in xrange(len(para)):
        flib.write(para[i][0]+chr(config['sep_1'])+para[i][1]+chr(config['sep_1'])+info[i]+'\n')
    flib.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'usage : %s input paralib config' % sys.argv[0]
    else:
        startTime = time.time()
        fconfig = open(sys.argv[3],'r')
        config = yaml.load(fconfig)
        fconfig.close()
        main(sys.argv[1],sys.argv[2],config)
        print('Total Time : %fs!\n' % (time.time() - startTime))

