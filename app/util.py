# -*- coding: utf-8 -*-
#!/usr/local/bin/python2.7

import urllib
import json


# 
# from app import app
# from forms import MainForm

localquerydoc = "app/queries/local.q"


def get_prefixed(uri):
    
    json_data = open('app/static/prefixes.json')
    data = json.load(json_data)
    inv_map = {v:k for k, v in data.items()}
                
    label = uri[uri.rfind('/') + 1:]
    label = label[label.rfind('#') + 1:]
    label = label[label.rfind(':') + 1:]
                    
    lastchars = "#", ":", "/"
    indices = []; 
        
    for lastchar in lastchars:
        if lastchar in uri:
            indices.append(uri.rfind(lastchar))
    
    namespace = uri[0: max(indices) + 1]
    prefix = inv_map.get(namespace) 
    if not prefix is None: 
        label = prefix + ":" + label
    return label; 



def compute_rankings(graph, rankingfile):
    
    resultsdict = []
    similarities = dict()
    
    with open (localquerydoc, "r") as localqueryfile:
        localQuery = localqueryfile.read()
    entities = graph.query(localQuery)
    
    for row in entities:
        for item in row: 
            item = str(item)
            
            aggregateQuery = "SELECT (COUNT(*) AS ?count) WHERE { "
            aggregateQuery += "<" + item + "> ?property ?value . "
            aggregateQuery += "?entity2 ?property ?value . "
            aggregateQuery += "FILTER (<" + item + "> != ?entity2) "
            aggregateQuery += "}"
                        
            results = graph.query(aggregateQuery)
    
            for result in results:
                for intitem in result:
                    similarities[str(item)] = int(intitem)

    count = 0 
    for k in sorted(similarities, key=similarities.get, reverse=True):       
        count += 1 
        
        labelQuery = 'SELECT ?label WHERE {'
        labelQuery += ' <' + k + '> rdfs:label ?label .'
        labelQuery += 'FILTER langMatches( lang(?label), "EN" ) '
        labelQuery += '}'
        
        label = '' 
        labelresult = graph.query(labelQuery)
        for labelrow in labelresult:
            for labelitem in labelrow:
                label = labelitem
                
        if ("[" in label):
            label = label[0:label.index('[')]

        decodedk = urllib.unquote(k).decode('utf8') 
        
        if (label == ''): 
            label = decodedk[decodedk.rfind(':') + 1:]
            
        resultsdict.append({'uri': decodedk, 'label': label, 'count': count, 'ranking': str(similarities[k])})


    with open(rankingfile, 'w') as outfile:
        json.dump(resultsdict, outfile)

    return resultsdict



def compute_similarities(graph, similaritiesfile):
    
    with open (localquerydoc, "r") as localqueryfile:
        localQuery = localqueryfile.read()
    entities = graph.query(localQuery)

    entitycount = 0
    similarities = dict()
    for row in entities:
        for item in row:
            similarities[str(item)] = 0
            entitycount += 1


    count = 0
    outer = 0

    linksdict = []
    nodesdict = []

    for outerrow in entities:
        for outeritem in outerrow:    
            outeritem = str(outeritem)
                
            outer += 1
            inner = 0

            for innerrow in entities:
                for inneritem in innerrow:
                    inneritem = str(inneritem)
                    
                    inner += 1

                    if inner > outer:
                        count += 1
                             
                            
                        if (outeritem.startswith("http") and (inneritem.startswith("http"))): 
                            similarity = compute_similarity(graph, outeritem, inneritem)
                        
                            similarities[str(outeritem)] = int(similarities[str(outeritem)]) + int(similarity)
                            similarities[str(inneritem)] = int(similarities[str(inneritem)]) + int(similarity)

                                
                            decodedouteritem = urllib.unquote(outeritem).decode('utf8') 
                            decodedinneritem = urllib.unquote(inneritem).decode('utf8') 

                            linksdict.append({'source': decodedouteritem, 'target': decodedinneritem, 'value': int(similarity)})


    for k in sorted(similarities, key=similarities.get, reverse=True):
        
        labelQuery = 'SELECT ?label WHERE {'
        labelQuery += ' <' + k + '> rdfs:label ?label .'
        labelQuery += 'FILTER langMatches( lang(?label), "EN" ) '
        labelQuery += '}'
        
        label = '' 
        labelresult = graph.query(labelQuery)
        for labelrow in labelresult:
            for labelitem in labelrow:
                label = labelitem
                
        if ("[" in label):
            label = label[0:label.index('[')]

        decodedk = urllib.unquote(k).decode('utf8') 
        
        if (label == ''): 
            label = decodedk[decodedk.rfind(':') + 1:]


        nodesdict.append({'name': decodedk, 'group': '1', 'label': label})


    similaritylist = {'links': linksdict, 'nodes': nodesdict}
    
    
    with open(similaritiesfile, 'w') as outfile:
        json.dump(similaritylist, outfile)
    



def compute_similarity(graph, outer, inner):
    similarityQuery = 'SELECT (COUNT(?p) AS ?count) WHERE {{ <'
    similarityQuery += outer
    similarityQuery += '> ?p ?v . '
    similarityQuery += '<'
    similarityQuery += inner
    similarityQuery += '> ?p ?v . '
    similarityQuery += '} UNION {?entity ?p <'
    similarityQuery += outer
    similarityQuery += '> . ?entity ?p <'
    similarityQuery += inner
    similarityQuery += '> .}}'    
    
    result = graph.query(similarityQuery)
    for row in result:
        for item in row:
            return item

