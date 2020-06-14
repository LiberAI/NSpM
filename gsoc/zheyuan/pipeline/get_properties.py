import urllib
import json
import sys
import csv
import io
import argparse
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_properties(url,  project_name="test_project", output_file = "get_properties.csv"):
    """
    - This function extracts the information regarding : [Name, Label, Domain, Range] from a page like this :
    http://mappings.dbpedia.org/server/ontology/classes/Place and saves it in a file in CSV format.
    - This code on execution creates a csv which contains all the properties, ontology,
    class related information and data types as field values in each row.
    - This function also returns a 2D list of the information mentioned above to the calling
    function
    """
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    if(not os.path.isdir(project_name)):
        os.makedirs(project_name)
    output_file = open(project_name+"/" + output_file, 'w')
    fl = 0
    accum = []
    for rows in tqdm(soup.find_all("tr")):
        x = rows.find_all("td")
        if len(x) <= 2:
            fl = 1
            continue
        if fl == 1:
            fl = 2
            continue
        name = rows.find_all("td")[0].get_text().replace(" (edit)", "")
        label = rows.find_all("td")[1].get_text()
        dom = rows.find_all("td")[2].get_text()
        rng = rows.find_all("td")[3].get_text()
        URL_name = ((rows.find_all("td")[0].find('a').attrs['href']))
        final = name + "," + label + "," + dom + "," + rng 
        #+ ","+ URL_name.split(':')[-1]
        accum.append(final)
        output_file.write(final+"\n")
    output_file.close()
    return accum


"""
Name, Label, Domain, Range, URL_name
"""

if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--url', dest='url', metavar='url',
                                                            help='Webpage URL: eg-http://mappings.dbpedia.org/server/ontology/classes/Place', required=True)
    requiredNamed.add_argument(
        '--output_file', dest='out_put', metavar='out_put', help='temp.csv', required=True)
    requiredNamed.add_argument(
        '--project_name', dest='project_name', metavar='project_name', help='test', required=True)
    args = parser.parse_args()
    url = args.url
    output_file = args.out_put
    project_name = args.project_name
    get_properties(url = url, project_name= project_name,  output_file = output_file)
    pass
