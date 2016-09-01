# -*- coding: utf-8 -*-

import os
import sys
import time
import re

def main(weibo):

    startTime = time.time()
    fweibo = open(weibo,'r')
    #fn = open('num','w')
    #fw = open('word','w')
    #fnd = open('ndot','w')
    fwd = open('wordd','w')
    #fwordd = open('worddot','w')
    fnw = open('nword','w')
    fndw = open('nwordd','w')
    fother = open('other','w')
    lines = fweibo.readlines()
    for line in lines:
        line = line.strip()
        if re.match(r'^《.+》$',line):
            #fother.write(line+'\n')
            continue
        elif re.match(r'^([0-9]+:[0-9][0-9]:[0-9][0-9]|[0-9]+:[0-9][0-9])$',line):
            #fother.write(line+'\n')
            continue
        elif re.match(r'^([0-9]{3,4}-[0-9]+-[0-9]+)$',line):
            #fother.write(line+'\n')
            continue
        elif re.match(r'^([0-9]+)$',line):
            #fn.write(line+'\n')
            continue
        elif re.match(r'^([a-z]+)$',line):
            #fw.write(line+'\n')
            continue
        elif re.match(r'^([0-9a-z]+)$',line):
            fnw.write(line+'\n')
            #continue
        elif re.match(r'^([\.\-/]*[0-9]+[\.\-/]*)$',line):
            #fother.write(line+'\n')
            continue
        elif re.match(r'^[0-9\.]+$',line):
            #fother.write(line+'\n')
            continue
        elif re.match(r'^([\.\-/]*[a-z]+[\.\-/]*)$',line):
            #fother.write(line+'\n')
            continue
        elif re.match(r'^([a-z\.]+)$',line):
            fwd.write(line+'\n')
        elif re.match(r'^([0-9a-z\.]+)$',line):
            fndw.write(line+'\n')
        else:
            fother.write(line+'\n')
            #continue

    fweibo.close()
    #fn.close()
    #fw.close()
    #fnd.close()
    fwd.close()
    #fwordd.close()
    fnw.close()
    fndw.close()
    fother.close()
    print('Total Time : %fs!\n' % (time.time() - startTime))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage : %s' % sys.argv[0]
    else:
        main(sys.argv[1])
