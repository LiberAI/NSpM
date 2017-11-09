import generator

def test_extract_variables():
    query = 'select distinct(?x) ?y where { ?x a C . ?x a ?y }'
    query2 = 'select distinct ?a where'

    result = generator.extract_variables(query)
    result2 = generator.extract_variables(query2)

    assert result == ['x', 'y']
    assert result2 == ['a']