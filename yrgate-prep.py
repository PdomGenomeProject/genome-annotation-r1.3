#!/usr/bin/env python
from __future__ import print_function
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start', type=int, default=1, help='Number at '
                    'which to begin counting; default is 1')
parser.add_argument('gff3', type=argparse.FileType('r'))
args = parser.parse_args()

count = args.start - 1
mrnas = dict()
for line in args.gff3:
    line = line.rstrip()
    fields = line.split('\t')
    if len(fields) != 9:
        print(line)
        continue
    
    featuretype = fields[2]
    if featuretype == 'gene':
        count += 1
        label = 'PdomGENEr1.3-%05d' % count
        line = line + ';Name=' + label
        print(line)
    elif featuretype == 'mRNA':
        glabel = 'PdomGENEr1.3-%05d' % count
        if glabel not in mrnas:
            mrnas[glabel] = 0
        mrnas[glabel] += 1
        mlabel = 'PdomMRNAr1.3-%05d.%d' % (count, mrnas[glabel])
        line = line + ';Name=' + mlabel
        print(line)
    else:
        print(line)
