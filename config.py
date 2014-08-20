#!/usr/local/bin/python2.7

DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = '********'
ENDPOINTS = dict([('Drugbank', 'http://drugbank.bio2rdf.org/sparql'),
                  ('Pubmed Publications', 'http://cu.pubmed.bio2rdf.org/sparql'),
#                   ('Clinical Trials', 'http://semweb.cs.vu.nl:8080/openrdf-sesame/repositories/ct'),
#                   ('LinkedCT', 'http://linkedct.org/sparql/'),
                  ('DBPedia', 'http://dbpedia.org/sparql')])
