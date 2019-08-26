# QALD JSON format generator

- Runs on Python 2.7

- It requires the interpreter function to run this. Thus to use this please copy this folder to the main folder and copy the python file to the man folder, for your ease please run the following code on the terminal : 
```
./shifter.sh
```
- The QALD format generator is a program that generates the input for the gerbil portal.
- The function requires the english and it's translated version to be present in the this folder with the following file names: `test.en` and `test.sparql`.
- The question and corresponding SPARQL form should have the same line number.
- The code can be run by running the `qald_json_gerbil_input.py` present outside this folder. An example of the output json file is as follows:

```json
{
	"questions": [{
		"id": "1",
		"question": [{
			"language": "en",
			"string": "Which German cities have more than 250000 inhabitants?"
		}],
		"query": {
			"sparql": "SELECT DISTINCT ?uri WHERE { { ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/City> . } UNION { ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/Town> . }  ?uri <http://dbpedia.org/ontology/country> <http://dbpedia.org/resource/Germany> .  ?uri <http://dbpedia.org/ontology/populationTotal> ?population .  FILTER ( ?population > 250000 ) } "
		},
		"answers": [{
			"head": {
				"vars": [
					"uri"
				]
			},
			"results": {
				"bindings": [{
					"uri": {
						"type": "uri",
						"value": "http://dbpedia.org/resource/Bonn"
					}
				}]
			}
		}]
	}]
}
```
