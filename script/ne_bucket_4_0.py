# -*- coding: utf-8 -*-

import os
import sys
import time
import re
import numpy as np
import operator
import yaml
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

def main(infile,model,config):

    startTime = time.time()
    postagger = Postagger()
    postagger.load(model+'pos.model')
    recognizer = NamedEntityRecognizer()
    recognizer.load(model+'ner.model')

    fin = open(infile,'r')
    fns = open(infile+'.ns','w')
    fni = open(infile+'.ni','w')
    fnh = open(infile+'.nh','w')
    fno = open(infile+'.no','w')
    lines = fin.readlines()
    n = len(lines)
    for i in xrange(n):
        line = lines[i].strip().split(chr(config['sep_3']))
        words = line[1].strip().split(config['sep_w'])
        postags = postagger.postag(words)
        netags = recognizer.recognize(words, postags)
        nes = list(set(netags)-set(['O']))
        if len(nes) > 0:
            ne = nes[0].strip().split('-')[1]
            if ne == 'Ns':
                fns.write(lines[i])
            elif ne == 'Ni':
                fni.write(lines[i])
            elif ne == 'Nh':
                fnh.write(lines[i])
            else:
                fno.write(lines[i])
        else:
            fno.write(lines[i])

    postagger.release()
    recognizer.release()
    fin.close()
    fns.close()
    fni.close()
    fnh.close()
    fno.close()
    print('Total Time : %fs!\n' % (time.time() - startTime))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'usage : %s input ltp_model config ! ' % sys.argv[0]
        exit(1)
    else:
        fconfig = open(sys.argv[3],'r')
        config = yaml.load(fconfig)
        fconfig.close()
        main(sys.argv[1],sys.argv[2],config)

