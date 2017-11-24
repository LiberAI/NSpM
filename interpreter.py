#!/usr/bin/env python
"""

Neural SPARQL Machines - Interpreter module

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
https://arxiv.org/abs/1708.07624

Version 0.0.3

"""
import sys
# import json
# import urllib2, urllib, httplib, json
# import random
# import re
# import os

reload(sys)
sys.setdefaultencoding("utf-8")

# load grammar
SPARQL_GRAMMAR = []
with open('sparql.grammar') as f:
    for line in f:
        line = line[:-1].split('\t')
        SPARQL_GRAMMAR.append((line[0], line[1]))

def inverse_replacements(s):
    for r in SPARQL_GRAMMAR:
        s = s.replace(r[1], r[0]) # inverse (Neural SPARQL to SPARQL grammar)
    return s

en_q = list()
with open(sys.argv[2]) as f:
    for line in f:
        en_q.append(line[:-1])

with open(sys.argv[1]) as f:
    i = 0
    for line in f:
        print "{}\n\t{}\t{}\n-----".format(en_q[i], line, inverse_replacements(line[:-1]))
        i += 1
        