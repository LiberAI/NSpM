#!/usr/bin/env python
"""

Neural SPARQL Machines - Interpreter module.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://arxiv.org/abs/1708.07624

Version 1.0.0

"""
import sys
import re

from generator_utils import decode, fix_URI
import importlib

if __name__ == '__main__':
    importlib.reload(sys)
    encoded_sparql = sys.argv[1]
    decoded_sparql = decode(encoded_sparql)
    decoded_sparql = fix_URI(decoded_sparql)
    print(decoded_sparql)
