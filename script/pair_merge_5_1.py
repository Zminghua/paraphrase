# -*- coding: utf-8 -*-

import os
import sys
import time
import math
import re
import yaml
        

def main(source,target,sourcelib,targetlib,config):
    
    para = []
    fslib = open(sourcelib,'r')
    ftlib = open(targetlib,'r')
    slines = fslib.readlines()
    tlines = ftlib.readlines()
    for i in xrange(len(slines)):
        term = [ slines[i].strip(),tlines[i].strip() ]
        para.append(term)
    fslib.close()
    ftlib.close()

    fsin = open(source,'r')
    ftin = open(target,'r')
    slines = fsin.readlines()
    tlines = ftin.readlines()
    for i in xrange(len(slines)):
        term = [ slines[i].strip(),tlines[i].strip() ]
        if (term not in para) and (term[::-1] not in para):
            para.append(term)
    fsin.close()
    ftin.close()

    fslib = open(sourcelib,'w')
    ftlib = open(targetlib,'w')
    for i in xrange(len(para)):
        fslib.write(para[i][0]+'\n')
        ftlib.write(para[i][1]+'\n')
    fslib.close()
    ftlib.close()


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'usage : %s source target sourcelib targetlib config' % sys.argv[0]
    else:
        startTime = time.time()
        fconfig = open(sys.argv[5],'r')
        config = yaml.load(fconfig)
        fconfig.close()
        main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],config)
        print('Total Time : %fs!\n' % (time.time() - startTime))

