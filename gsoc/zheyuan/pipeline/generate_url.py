import xmltodict
import pprint
import json
import sys
import urllib
import argparse
from bs4 import BeautifulSoup


def get_url(url):
        """Fuction to extract the http://mappings.dbpedia.org/server/ontology/classes/<some entity> 
        page link for the given http://mappings.dbpedia.org/index.php/OntologyClass:<some entity>"""
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        link = soup.findAll('a', attrs={"rel": "nofollow"})[0]['href']
        return link


def generate_url(given_label):
        """
        - This function generates a proper url to extract information about class, properties and
        data types from the DBpedia database. (Like:​ http://mappings.dbpedia.org/server/ontology/classes/Place​ )
        - It returns a url string to the calling function.
        """
        xmldoc = open('../utility/dbpedia.owl', encoding="utf-8").read()
        jsondoc = ((xmltodict.parse(xmldoc)))
        count = 0

        for onto in jsondoc['rdf:RDF'].keys():
                if(not (onto == 'owl:Class')):
                        continue
                for val in ((jsondoc['rdf:RDF'][onto])):
                        count += 1
                        about = val['@rdf:about']
                        label = ""
                        for lang in (val['rdfs:label']):
                                if(lang['@xml:lang'] == 'en'):
                                        # print("Label: "+lang['#text'])
                                        label = lang['#text']
                        if(type(val['rdfs:subClassOf']) == list):
                                for subcl in val['rdfs:subClassOf']:
                                        #print("Sub-class of: "+subcl['@rdf:resource'])
                                        pass
                        elif(type(val['rdfs:subClassOf']) != "list"):
                                        #print("Sub-class of: "+val['rdfs:subClassOf']['@rdf:resource'])
                                        pass
                        url = val['prov:wasDerivedFrom']['@rdf:resource']
                        # print("URL:" + get_url(url))
                        if(given_label == val['@rdf:about'].split('http://dbpedia.org/ontology/')[-1]):
                                return [get_url(url),about]
        return ["None","None"]



if __name__ == "__main__":
        """
        Use the format 'python.py generate_url --label <Label: can be person, place etc.>`
        Section to parse the command line arguments.
        """
        parser = argparse.ArgumentParser()
        requiredNamed = parser.add_argument_group('Required Arguments')

        requiredNamed.add_argument('--label', dest='label', metavar='label',
                                                                help='label: person, place etc.', required=True)
        args = parser.parse_args()
        label = args.label
        print(generate_url(label))
        pass

def generate_url_spec(given_label):
        xmldoc = open('../utility/dbpedia.owl', encoding="utf-8").read()
        jsondoc = ((xmltodict.parse(xmldoc)))
        for onto in jsondoc['rdf:RDF'].keys():
                if(not (onto == 'owl:DatatypeProperty' or onto == "owl:ObjectProperty")):
                        continue
                for val in ((jsondoc['rdf:RDF'][onto])):
                        wiki_number = "None"
                        try:
                                for value in val['owl:equivalentClass']['@rdf:resource']:
                                        if "wikidata" in value:
                                                wiki_number= value.strip().split("/")[-1] 
                        except:
                                pass
                        derived = ""
                        try:
                                derived = val['prov:wasDerivedFrom']['@rdf:resource']
                        except:
                                derived = "None"
                        label = ""
                        try:
                                if(type(val['rdfs:label']) == list):
                                        for lang in (val['rdfs:label']):
                                                if(lang['@xml:lang'] == 'en'):
                                                        # print("Label: "+lang['#text'])
                                                        label = lang['#text']
                                elif(type(val['rdfs:label']) != "list"):
                                                lang = dict(val['rdfs:label'])
                                                label = lang['#text']
                                                pass
                                if(given_label == val['@rdf:about'].split('http://dbpedia.org/ontology/')[-1]):
                                        return [val['@rdf:about'],derived,wiki_number]
                        except:
                                if(given_label == val['@rdf:about'].split('http://dbpedia.org/ontology/')[-1]):
                                        return [val['@rdf:about'],derived,wiki_number]
                                continue
        return ["None", "None", "None"]
