# -*- coding: utf-8 -*-

import os
import sys
import time
import re

def main(infile,outfile):

    startTime = time.time()
    fin = open(infile,'r')
    fout = open(outfile,'w')
    lines = fin.readlines()
    for line in lines:
        line = line.strip()
        i = line.find('http')
        if i != -1:
            line = re.sub(r'http[0-9a-zA-Z:./]+',' ',line)
        line = re.sub(r'「转」|（转）|「图转」|（图转）|\(转\)|\(图转\)|\(转）|\(转|（转','',line)
        line = re.sub(r'【转】|（转贴）|【图转】|【全文】|（转自网络）|（转\)|<转>','',line)
        line = re.sub(r'【','',line)
        line = re.sub(r'】','。',line)
        line = re.sub(r',','，',line)
        line = re.sub(r'(★)+|(〜)+|(⋯)+|｀･ω･´|｟|｠|\t|👏🔥🍻|🌴🐳💦|❤','',line)
        line = re.sub(r'(。)+|(\.){2,}|……','。',line)
        line = re.sub(r'(！)+|(!)+','！',line)
        line = re.sub(r'(～)+','～',line)
        line = re.sub(r'(~)+','~',line)
        line = re.sub(r'( )+',' ',line)
        for t in  re.findall(r'[0-9]+：[0-9]+：[0-9]+|[0-9]+：[0-9]+',line):
            line = re.sub(t,t.replace('：',':'),line)
        fout.write(line.strip()+'\n')

    fin.close()
    fout.close()
    print('Total Time : %fs!\n' % (time.time() - startTime))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'usage : %s input output' % sys.argv[0]
        exit(1)
    else:
        main(sys.argv[1], sys.argv[2])

