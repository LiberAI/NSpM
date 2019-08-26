#!/usr/bin/env python
"""

Neural SPARQL Machines - Interpreter module

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
https://arxiv.org/abs/1708.07624

Version 0.1.0-akaha

"""
import sys
import re

from generator_utils import decode,fix_URI

def interpreter(val):
    reload(sys)
    sys.setdefaultencoding("utf-8")
    encoded_sparql = val
    decoded_sparql = decode(encoded_sparql)
    decoded_sparql = fix_URI(decoded_sparql)
    return( decoded_sparql)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    encoded_sparql = sys.argv[1]
    decoded_sparql = decode(encoded_sparql)
    decoded_sparql = fix_URI(decoded_sparql)
    print( decoded_sparql)
