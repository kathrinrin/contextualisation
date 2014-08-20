# -*- coding: utf-8 -*-
#!/usr/local/bin/python2.7

from SPARQLWrapper import SPARQLWrapper, JSON, XML
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed
from flask import request, url_for, render_template, current_app
import rdflib
import util as u
import urllib2
import xml.sax
from werkzeug.urls import url_fix

from app import app
from forms import MainForm

# create our little application :)
app.config.from_object(__name__)


if not app.debug:
    import logging
    file_handler = logging.FileHandler("contextualisation_errors.log", delay=True)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    

@app.route('/')
def index():

    form = MainForm()
    with open (("app/queries/Drugbank.q"), "r") as queryfile:
        q = queryfile.read()
        form.query.data = q
    return render_template('base.html', form=form)




@app.route('/', methods=['POST'])
def work():    
    
    global facetsdict
    global resultsdict
    global graph
    
    form = MainForm()
    dataset = form.endpoints.data
    
    my_var = request.form.get("btn", "None")
    my_var2 = request.form.get("btn2", "None")
    if ((my_var == 'None') and (my_var2 == 'None')): 
        querydoc = ("app/queries/" + dataset + ".q")
        with open ((querydoc), "r") as queryfile:
            q = queryfile.read()
            form.query.data = q
        return render_template('base.html', form=form)
    
    
    if (my_var != 'None'):
        rankingfile = "app/rankings/ranking_" + dataset + ".txt"
        resultsfile = "app/results/results_" + dataset + ".rdf"
    
        if (True): 
#             if (form.datafromendpoint.data): 
           
            
            try:
                sparql = SPARQLWrapper(app.config['ENDPOINTS'].get(dataset))
                sparql.setReturnFormat(JSON)
                sparql.setQuery(form.query.data)
                sparql.setReturnFormat(XML)
                resultfile = open(resultsfile, "wb")
                r = sparql.query().convert()
                r.serialize(destination=resultfile, format="xml")
                resultfile.flush() 
                resultfile.close()
                

            except (urllib2.HTTPError, QueryBadFormed, TypeError, AttributeError), err:
                current_app.logger.debug(str(err))
                error = str(err)
                return render_template('base.html', results=[], url="", form=form, error=error, facets=[])
             

            try:  
                
                global graph
                graph = rdflib.Graph()
                graph.parse(resultsfile)
                resultsdict = u.compute_rankings(graph, rankingfile)
                url = "" 
                current_app.logger.debug(url)

                try: 
                    with open("app/static/similarities_" + dataset + ".json"):
                        url = url_for('.static', filename='similarities_' + dataset + '.json')
                except IOError:
                    url = "" 
                    
                current_app.logger.debug(url)
       
                with open ("app/queries/facets.q", "r") as myresultfile:
                    localQuery = myresultfile.read()
                entityresults = graph.query(localQuery)
                
                
                facetsdict = []
                for row in entityresults:
                    facet = row[0]
                    count = int(row[1])
                    label = u.get_prefixed(facet)
                    facetsdict.append({'facet': facet, 'label': label, 'count': count})            


            except (TypeError, xml.sax.SAXParseException), err:
                current_app.logger.debug(str(err))
                error = str(err)
                return render_template('base.html', results=resultsdict, url=url, form=form, error=error, facets=facetsdict)

        return render_template('base.html', results=resultsdict, url=url, form=form, error="", facets=facetsdict)


    if (my_var2 != 'None'):

        similaritiesfile = "app/static/similarities_" + dataset + ".json"
        u.compute_similarities(graph, similaritiesfile)
        url = url_for('.static', filename='similarities_' + dataset + '.json')
        return render_template('base.html', results=resultsdict, url=url, form=form, error="", facets=facetsdict)



# ADMINS = ['k.dentler@vu.nl']
# if not app.debug:
#     import logging
#     from logging.handlers import SMTPHandler
#     mail_handler = SMTPHandler('127.0.0.1',
#                                'server-error@mash-it.net',
#                                ADMINS, 'YourApplication Failed')
#     mail_handler.setLevel(logging.ERROR)
#     app.logger.addHandler(mail_handler)



@app.route('/entity')
def entity():
    
    global graph
    
    uri = request.args.get('uri')

    form = MainForm()
    
    

    facetQuery = "SELECT ?p ?o WHERE { <" + uri + "> ?p ?o . }"
    facetResults = graph.query(facetQuery)

    if not facetResults: 
        facetQuery = "SELECT ?p ?o WHERE { <" + url_fix(uri) + "> ?p ?o . }"
        facetResults = graph.query(facetQuery)
   
   
    facetsentitylist = []
    for fr in facetResults : 
        
        facetproperty = fr[0]
        prefixed_facetproperty = u.get_prefixed(facetproperty)
        facetobject = fr[1]
        prefixed_facetobject = ""
        if facetobject.startswith("http://"):
            prefixed_facetobject = u.get_prefixed(facetobject)


        
        subjects = graph.subjects(facetproperty, facetobject)
        occurrences = sum(1 for _ in subjects)
#         current_app.logger.debug(occurrences)
        
        
        facetsentitylist.append({'facetproperty': facetproperty, 'prefixed_facetproperty': prefixed_facetproperty, 'facetobject': facetobject, 'prefixed_facetobject': prefixed_facetobject, 'occurrences': occurrences})       



    sortedlist = sorted(facetsentitylist, key=lambda k: k['occurrences']) 
    return render_template('base2.html', form=form, uri=uri, facetsentity=sortedlist)





if __name__ == '__main__':
    app.run()
