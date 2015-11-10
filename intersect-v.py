#!/usr/bin/env python
from __future__ import print_function
import argparse
import intervaltree
import re

parser = argparse.ArgumentParser()
parser.add_argument('orig', type=argparse.FileType('r'))
parser.add_argument('yrgate', type=argparse.FileType('r'))
args = parser.parse_args()

yrgate_annots = dict()
for line in args.yrgate:
    if '\tgene\t' in line:
        line = line.rstrip()
        fields = line.split('\t')
        seqid = fields[0]
        if seqid not in yrgate_annots:
            yrgate_annots[seqid] = intervaltree.IntervalTree()
        start = int(fields[3])
        end = int(fields[4])
        yrgate_annots[seqid].addi(start, end, line)

toprint = dict()
for line in args.orig:
    line = line.rstrip()
    fields = line.split('\t')
    if len(fields) != 9:
        print(line)
        continue
    
    featuretype = fields[2]
    if featuretype == 'gene':
        seqid = fields[0]
        start = int(fields[3])
        end = int(fields[4])
        if seqid not in yrgate_annots or yrgate_annots[seqid][start:end] == set():
            gid = re.search('ID=([^;\n]+)', line).group(1)
            toprint[gid] = True
            print(line)
    elif featuretype in ['mRNA', 'tRNA']:
        tid = re.search('ID=([^;\n]+)', line).group(1)
        gid = re.search('Parent=([^;\n]+)', line).group(1)
        if gid in toprint:
            toprint[tid] = True
            if featuretype == 'tRNA':
                line = re.sub('Name=([^;\n]+)', 'Name=' + tid, line)
            print(line)
    else:
        idmatch = re.search('Parent=([^;\n]+)', line)
        if idmatch and idmatch.group(1) in toprint:
            print(line)
