#!/usr/bin/env python
"""

Neural SPARQL Machines - Generator test unit.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
https://arxiv.org/abs/1708.07624

Version 0.1.0-akaha

"""
import generator
import generator_utils
import operator


def test_extract_variables():
    query = 'select distinct(?x) ?y where { ?x a C . ?x a ?y}'
    query2 = 'select distinct ?a where'

    result = generator_utils.extract_variables(query)
    result2 = generator_utils.extract_variables(query2)

    assert result == ['x', 'y']
    assert result2 == ['a']


def test_single_resource_sort():
    matches = [{'usages': [17]}, {'usages': [0]}, {'usages': [3]}, {'usages': [2]}, {'usages': [1]}]

    result = sorted(matches, key=generator.prioritize_usage)

    assert map(operator.itemgetter(0), map(operator.itemgetter('usages'), result)) == [17, 3, 2, 1, 0 ]


def test_couple_resource_sort():
    matches = [{'usages': [17, 2]}, {'usages': [0, 0]}, {'usages': [3, 2]}, {'usages': [2, 2]}, {'usages': [1, 2]}]

    result = sorted(matches, key=generator.prioritize_usage)

    assert map(operator.itemgetter('usages'), result) == [[17, 2], [3, 2], [2, 2], [1, 2], [0, 0]]


def test_encoding():
    original = 'SELECT ?city WHERE { ?m skos:broader dbc:Cities_in_Germany . ?city dct:subject ?m . ?city dbo:areaTotal ?area . ?b dbo:artist dbr:John_Halsey_(musician) } order by asc (?area)'
    expected_encoding = 'SELECT var_city WHERE brack_open var_m skos_broader dbc_Cities_in_Germany sep_dot var_city dct_subject var_m sep_dot var_city dbo_areaTotal var_area sep_dot var_b dbo_artist dbr_John_Halsey_ attr_open musician attr_close  brack_close _oba_ var_area '

    result = generator_utils.encode(original)

    assert result == expected_encoding
    assert str.strip(generator_utils.decode(result)) == original


def test_shorten_query():
    shorten = generator_utils.shorten_query

    assert shorten('ORDER BY var_area') == '_oba_ var_area'
    assert shorten('order by asc par_open var_area par_close') == '_oba_ var_area'
    assert shorten('order by desc attr_open var_area attr_close') == '_obd_ var_area'


def test_normalize_predicates():
    alt = 'dbp_placeOfBirth'

    assert generator_utils.normalize_predicates(alt) == 'dbo_birthPlace'