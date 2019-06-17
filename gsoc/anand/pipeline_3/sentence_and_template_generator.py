import argparse
from generate_url import generate_url_spec , get_url, generate_url
from get_properties import get_properties
import urllib
import urllib.parse
from bs4 import BeautifulSoup
import os

def check_query(query):
    query_original = query
    query = urllib.parse.quote(query)
    url = "https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query="+query+"&format=text%2Fhtml&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on&run=+Run+Query+"
    #print(url)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    print((soup.text))
    if(soup.text=="false"):
        return False
    else:
        print(query_original)
        return True

def sentence_and_template_generator(mother_ontology,vessel,prop,project_name,output_file,count=0, suffix = " of <A> ?", query_suffix = ""):
    if(type(prop)==str):
        prop = prop.split(',')

    natural_language_question = []
    sparql_query = []

    question_form = open("../utility/question_form.csv",'r').readlines()
    question_starts_with =question_form[0].split(',')
    query_starts_with = question_form[1].split(',')
    query_ends_with = question_form[2].split(',')
    question_number=[2]
    if(prop[3]=="owl:Thing" or prop[3]=="xsd:string"):
        question_number=[2,4]
    elif(prop[3]=="Place"):
       question_number=[3,4]
    elif(prop[3]=="Person"):
       question_number=[1,4]
    elif(prop[3]=="xsd:date" or "date" in prop[3] or "year" in prop[3] or "date" in prop[3] or "time" in prop[3] ):
       question_number=[0,4,5]    
    elif(prop[3]=="xsd:nonNegativeInteger" or "negative" in prop[3].lower() ):
       question_number=[2,6]
    elif(prop[3]=="xsd:integer" or "integer" in prop[3].lower() ):
       question_number=[2,6]    
    else:
        question_number=[2]  

    val = (generate_url_spec(prop[1]))
    prop_link = val[0]
    if(prop_link=="None" or prop_link== None):
        return
    derived = val[1]
    prop_link = "dbo:"+prop_link.strip().split('http://dbpedia.org/ontology/')[-1]

    for number in question_number:
        natural_language_question.append(question_starts_with[number]+prop[1]+ suffix)
        sparql_query.append(query_starts_with[number]+"where { <A>  "+ query_suffix + prop_link  +" ?x "+ query_ends_with[number])


    if(query_suffix==""):
        query_answer = ("select distinct(?a) where { ?a "+prop_link+" []  } ")
    else :
        query_answer = ("select distinct(?a) where { ?a "+query_suffix.split(" ")[0]+" [] . ?a  "+query_suffix +" "+ prop_link +" ?x } ")

    if(query_suffix==""):
        flag = (check_query(query_answer.replace("select distinct(?a)","ask")))
    else :
        flag = (check_query(query_answer.replace("select distinct(?a)","ask")))
    if(not flag):
        return

    count = count - 1
    if(count == 0):
        variable = "?x"
    else:
        variable = "?x"+ str(count) 
    query_suffix = prop_link + " "+variable+" . "+variable+" " 

    for number in range(len(natural_language_question)):
        vessel.append([mother_ontology,"","",natural_language_question[number],sparql_query[number],query_answer])
        output_file.write(';'.join(vessel[-1])+"\n")
        print(';'.join(vessel[-1])+"\n")
    print(str(natural_language_question)+"\n"+str(sparql_query)+"\n"+query_answer+"\n*************")
    
    suffix = " of "+ prop[1] +" of <A> ?"
    
    if(count>0):
        print(prop[3].split(":")[-1])
        val = generate_url(prop[3].split(":")[-1].lower())
        url = val[0]
        if(not url.startswith("http://mappings.dbpedia.org")):
            return
        list_of_property_information = get_properties(url=url,project_name=project_name,output_file =prop[1]+".csv" )
        for property_line in list_of_property_information:
            prop_inside = property_line.split(',')
            sentence_and_template_generator(output_file=output_file, mother_ontology=mother_ontology,vessel=vessel,prop=prop_inside, suffix = suffix,count = count, project_name=project_name, query_suffix = query_suffix )       
                



if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--prop', dest='prop', metavar='prop',
                                                            help='prop: person, place etc.', required=True)
    args = parser.parse_args()
    prop = args.prop
    sentence_and_template_generator(prop=prop)
    pass