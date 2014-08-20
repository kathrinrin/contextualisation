PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX linkedct: <http://static.linkedct.org/resource/linkedct/>
PREFIX db: <http://static.linkedct.org/resource/>
PREFIX dbpedia: <http://dbpedia.org/property/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX map: <file:/C:/d2r-server-0.4/ctmap.n3#>
PREFIX dc: <http://purl.org/dc/terms/>


CONSTRUCT { ?entity ?property ?value . }
WHERE {
  ?entity ?property ?value .
  ?entity a linkedct:trials .
  ?entity linkedct:condition ?condition .
  ?condition linkedct:condition_name ?condition_name .
  FILTER regex(?condition_name, "breast", "i")
 }
