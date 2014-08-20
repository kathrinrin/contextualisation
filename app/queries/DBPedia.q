PREFIX dbp-cat: <http://dbpedia.org/resource/Category:>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX purl: <http://purl.org/dc/terms/>

CONSTRUCT { ?entity ?property ?value . } 

WHERE {
  ?entity purl:subject dbp-cat:ABBA_members . 
  ?entity ?property ?value . 
  
  MINUS {
    ?entity ?property ?value . 
    FILTER(LANG(?value) != "en")
  }
}
