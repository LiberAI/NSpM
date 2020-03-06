# Read the description in the supplied readme.md
import argparse
from generate_url import generate_url_spec, generate_url
from get_properties import get_properties
import urllib
from urllib2 import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import os
from tqdm import tqdm


def rank_check(query, diction, count, original_count):
    query_original = query
    count = original_count - count
    ques = " "
    for value in range(count):
        if (value == 0):
            ques = ques + "?x "
        else:
            ques = ques + "?x" + str(value + 1) + " "
    query = query.replace("(?a)", "(?a)" + ques) + " order by RAND() limit 100"
    # print(query)
    try:  # python3
        query = urllib.parse.quote_plus(query)
    except:  # python2
        query = urllib.quote_plus(query)
    url = "https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=" + query + "&format=text%2Fhtml&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on&run=+Run+Query+"
    # url = "https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query="+query + \
    #    "&format=application%2Fsparql-results%2Bjson&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on&run=+Run+Query+"
    # print(url)
    try:  # python3
        page = urllib.request.urlopen(url)
    except:  # python2
        page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    total = len(soup.find_all("tr"))
    accum = 0
    for rows in (soup.find_all("tr")):
        for td in rows.find_all("a"):
            damp = 0.85
            denom = 0
            interaccum = 0
            for a in td:
                if (a in diction.keys()):
                    denom += 1
                    damp *= damp
                    interaccum += damp * float(diction[a])
                """ print (a.get_text())
                if(a.get_text() in diction.keys()):
                    print(diction(a.get_text())) """
            if (denom):
                interaccum = interaccum / denom
            accum += interaccum
    return float(accum / total)


def check_query(log, query):
    query_original = query
    try:  # python3
        query = urllib.parse.quote_plus(query)
    except:  # python2
        query = urllib.quote_plus(query)
    url = "https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=" + query + "&format=text%2Fhtml&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on&run=+Run+Query+"
    # print(url)
    try:  # python3
        page = urllib.request.urlopen(url)
    except:  # python2
        page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    # print((soup.text))
    if (soup.text == "false"):
        log.error(url)
        log.error(query_original)
        return False
    elif (soup.text == "true"):
        # log.info(url)
        # log.info(query_original )
        return True
    else:
        log.error("Broken Link")
        log.error(url)
        log.error(query_original)


def sentence_and_template_generator(prop_dic, test_set, log, mother_ontology, vessel, prop, project_name, output_file,
                                    diction, original_count=0, count=0, suffix=" of <A> ?", query_suffix=""):
    if (type(prop) == str):
        prop = prop.split(',')
    # original_count = count
    natural_language_question = []
    sparql_query = []
    question_form = open("../utility/question_form.csv", 'r').readlines()
    question_starts_with = question_form[0].split(',')
    query_starts_with = question_form[1].split(',')
    query_ends_with = question_form[2].split(',')
    question_number = [2]
    if (prop[3] == "owl:Thing" or prop[3] == "xsd:string"):
        question_number = [2, 4]
    elif (prop[3] == "Place"):
        question_number = [3, 4]
    elif (prop[3] == "Person"):
        question_number = [1, 4]
    elif (prop[3] == "xsd:date" or "date" in prop[3] or "year" in prop[3] or "date" in prop[3] or "time" in prop[3]):
        question_number = [0, 4, 5]
    elif (prop[3] == "xsd:nonNegativeInteger" or "negative" in prop[3].lower()):
        question_number = [2, 6]
    elif (prop[3] == "xsd:integer" or "integer" in prop[3].lower()):
        question_number = [2, 6]
    else:
        question_number = [2]

    val = (generate_url_spec(prop[0]))
    prop_link = val[0]
    if (prop_link == "None" or prop_link == None):
        return
    derived = val[1]
    prop_link = "dbo:" + prop_link.strip().split('http://dbpedia.org/ontology/')[-1]

    for number in question_number:
        natural_language_question.append(question_starts_with[number] + prop[1] + suffix)
        sparql_query.append(
            query_starts_with[number] + "where { <A>  " + query_suffix + prop_link + " ?x " + query_ends_with[number])

    if (query_suffix == ""):
        query_answer = ("select distinct(?a) where { ?a " + prop_link + " []  } ")
    else:
        query_answer = ("select distinct(?a) where { ?a " + query_suffix.split(" ")[
            0] + " [] . ?a  " + query_suffix + " " + prop_link + " ?x } ")

    if (query_suffix == ""):
        flag = (check_query(log=log, query=query_answer.replace("select distinct(?a)", "ask")))
    else:
        flag = (check_query(log=log, query=query_answer.replace("select distinct(?a)", "ask")))
    if (not flag):
        return

    rank = rank_check(diction=diction, count=count, query=query_answer, original_count=original_count)

    count = count - 1
    if (count == 0):
        variable = "?x"
    else:
        variable = "?x" + str(count)
    query_suffix = prop_link + " " + variable + " . " + variable + " "
    # for temp_counter in range(original_count):
    if (not prop[0] in prop_dic[original_count - count - 1]):
        for number in range(len(natural_language_question)):
            vessel.append(
                [mother_ontology, "", "", natural_language_question[number], sparql_query[number], query_answer])
            output_file.write((';'.join(vessel[-1]) + ";" + str(rank) + "\n").replace("  ", " "))
            log.info(';'.join(vessel[-1]) + str(rank) + "\n")
    else:
        for number in range(len(natural_language_question)):
            vessel.append(
                [mother_ontology, "", "", natural_language_question[number], sparql_query[number], query_answer])
            test_set.write((';'.join(vessel[-1]) + ";" + str(rank) + "\n").replace("  ", " "))
            log.info("Test: " + ';'.join(vessel[-1]) + str(rank) + "\n")
    prop_dic[original_count - count - 1].append(prop[0])
    # print(str(natural_language_question)+"\n"+str(sparql_query)+"\n"+query_answer+"\n*************")

    suffix = " of " + prop[1] + " of <A> ?"

    if (count > 0):
        print(prop[3].split(":")[-1])
        val = generate_url(prop[3].split(":")[-1])
        url = val[0]
        if (not url.startswith("http://mappings.dbpedia.org")):
            return
        list_of_property_information = get_properties(url=url, project_name=project_name, output_file=prop[1] + ".csv")
        for property_line in tqdm(list_of_property_information):
            prop_inside = property_line.split(',')
            sentence_and_template_generator(prop_dic=prop_dic, test_set=test_set, log=log,
                                            original_count=original_count, diction=diction, output_file=output_file,
                                            mother_ontology=mother_ontology, vessel=vessel, prop=prop_inside,
                                            suffix=suffix, count=count, project_name=project_name,
                                            query_suffix=query_suffix)

