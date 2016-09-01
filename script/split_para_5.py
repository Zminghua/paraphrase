# -*- coding: utf-8 -*-

import os
import sys
import time
import re
import yaml

parent = [-1]
def Find(post):
    s = post
    while parent[s] >= 0:
        s = parent[s]
    while s != post:
        tmp = parent[post]
        parent[post] = s
        post = tmp
    return s


def Union(post1,post2):
    r1 = Find(post1)
    r2 = Find(post2)
    temp = parent[r1] + parent[r2]
    if parent[r1] > parent[r2]:
        parent[r1] = r2
        parent[r2] = temp
    else:
        parent[r2] = r1
        parent[r1] = temp


def main(infile,source,target,config):
    global parent

    parent = [-1]*config['sen_num']
    posts = {}
    pend = {}
    startTime = time.time()
    fin = open(infile,'r')
    fsource = open(source,'w')
    ftarget = open(target,'w')
    lines = fin.readlines()
    for line in lines:
        line = line.strip().split(chr(config['sep_5']))
        temp = [ term.strip().split(chr(config['sep_4'])) for term in line[1:]]
        pid = [ int(term[0]) for term in temp ]
        post = [ term[1].strip().split(chr(config['sep_3']))[1] for term in temp ]
        
        if (post[0] in post[1]) or (post[1] in post[0]):
            continue
        if float(line[0]) > config['pair_sim_ceil']:
            continue
        if float(line[0]) < config['pair_sim_floor']:
            continue

        if float(line[0]) < config['pair_sim_pend']:
            posts[pid[0]] = post[0]
            posts[pid[1]] = post[1]
            if pend.has_key(pid[0]):
                pend[pid[0]].append(pid[1])
            else:
                pend[pid[0]] = [pid[1]]
            continue

        if Find(pid[0]) != Find(pid[1]):
            Union(pid[0],pid[1])

        fsource.write(post[0]+'\n')
        ftarget.write(post[1]+'\n')

    for id0 in pend.keys():
        for id1 in pend[id0]:
            if Find(id0) == Find(id1):
                fsource.write(posts[id0]+'\n')
                ftarget.write(posts[id1]+'\n')

    fin.close()
    fsource.close()
    ftarget.close()
    print('Total Time : %fs!\n' % (time.time() - startTime))

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'usage : %s input source target config ! ' % sys.argv[0]
        exit(1)
    else:
        fconfig = open(sys.argv[4],'r')
        config = yaml.load(fconfig)
        fconfig.close()
        main(sys.argv[1],sys.argv[2],sys.argv[3],config)

