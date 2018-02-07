import sys

from generator_utils import decode

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")

    encoded_sparql = sys.argv[1]
    decoded_sparql = decode(encoded_sparql)
    print decoded_sparql
