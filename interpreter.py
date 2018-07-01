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

from generator_utils import decode

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    encoded_sparql = sys.argv[1]
    decoded_sparql = decode(encoded_sparql)
    decoded_sparql = re.sub(r"dbr:([^\s]+)" , r"<http://dbpedia.org/resource/\1>" , decoded_sparql)
    print decoded_sparql
