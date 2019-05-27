# A Neural QA Model for DBpedia
## Abstract
With booming amount of information being continuously added to the internet, organising the facts becomes a very difficult task. Currently DBpedia hosts billions of such data points and corresponding relations in the RDF format.

RDF is a directed, labeled graph data format for representing information in the Web. SPARQL is a query language for RDF. SPARQL can be used to express queries across diverse data sources, whether the data is stored natively as RDF or viewed as RDF via middleware. The results of SPARQL queries can be results sets or RDF graphs. (Source : https://www.w3.org/TR/rdf-sparql-query/​) Extracting data from such data sources requires a query to be made in SPARQL and the response to the query is a link that contains the information pertaining to the answer or the answer itself.

Accessing such data is difficult for a lay user, who does not know how to write a query. This proposal tries to built upon a System :(​ https://github.com/AKSW/NSpM/tree/master ​) — which tries to make this humongous linked data available to a larger user base in their natural languages(now restricted to English) by improving, adding and amending upon the existing codebase.

The primary objective of the project being able to translate any natural language question to a valid SPARQL query.

You can find the supporting blogs at : https://anandpanchbhai.com/A-Neural-QA-Model-for-DBpedia/