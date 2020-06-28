import re
from tqdm import tqdm
from bs4 import BeautifulSoup
import urllib.request

labels = ['publisher', 'leaderName', 'mayor', 'country', 'musicComposer', 'routeEnd', 'starring', 'targetAirport', 'timeZone', 'origin', 'architect', 'team', 'Holiday', 'party', 'language', 'activeYearsEndDate', 'Protein', 'founder', 'foundingDate', 'governmentType', 'deathDate', 'type', 'birthName', 'vicePresident', 'knownFor', 'birthYear', 'crosses', 'city', 'height', 'ingredient', 'spouse', 'battle', 'child', 'location', 'doctoralAdvisor', 'portrayer', 'wineRegion', 'influenced', 'Beverage', 'developer', 'programmingLanguage', 'completionDate', 'budget', 'Organisation', 'numberOfPages', 'Sport', 'deathCause', 'growingGrape', 'product', 'capital', 'bandMember', 'largestCity', 'director', 'mission', 'ethnicGroup', 'officialLanguage', 'leader', 'foundationPlace', 'writer', 'date', 'abbreviation', 'dissolutionDate', 'successor', 'runtime', 'sourceCountry', 'maximumDepth', 'numberOfLocations', 'currency', 'state', 'birthDate', 'series', 'firstAscentPerson', 'composer', 'creator', 'influencedBy', 'almaMater', 'presenter', 'editor', 'discoverer', 'areaTotal', 'restingPlace', 'deathPlace', 'class', 'populationTotal', 'alias', 'owner', 'author', 'birthPlace', 'award']
ontologies = []
for label in labels:
    if re.match(r'^[A-Z].*', label):
        print(label)
        ontologies.append(label)
# ontologies = '[Holiday,Protein,Beverage,Organisation,Sport]'
properties = list(set(labels) ^ set(ontologies))
print(properties)
domains = set()
for property in properties:
    url = "http://dbpedia.org/ontology/"+property
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    for a in soup.find_all(rel="rdfs:domain"):
        domains.add(re.search(r'dbo:([a-zA-Z]+)', a.text).group(1))

        print(re.search(r'dbo:([a-zA-Z]+)', a.text).group(1))
print(list(domains | set(ontologies)))
# '[Airline, MeanOfTransportation, Mountain, Organisation, Beverage, Food, Software, Film, Protein, WrittenWork, Work, TelevisionShow, Band, ArchitecturalStructure, PopulatedPlace, Sport, Stream, Person, RouteOfTransportation, Place, Bridge, FictionalCharacter, Holiday, WineRegion, Scientist, Grape]'
# python multi_generate_templates.py --label '[Airline, MeanOfTransportation, Mountain, Organisation, Beverage, Food, Software, Film, Protein, WrittenWork, Work, TelevisionShow, Band, ArchitecturalStructure, PopulatedPlace, Sport, Stream, Person, RouteOfTransportation, Place, Bridge, FictionalCharacter, Holiday, WineRegion, Scientist, Grape]'--project_name test --depth 1 --multi True