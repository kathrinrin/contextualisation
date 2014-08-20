PREFIX pubmed: <http://bio2rdf.org/pubmed_vocabulary:>
PREFIX purl: <http://purl.org/dc/terms/>	

CONSTRUCT { ?entity ?property ?value }
 
WHERE {
  ?entity a pubmed:PubMedRecord . 
  ?entity purl:language "eng" .  
  ?entity pubmed:publication_type "JournalArticle" . 
  ?entity pubmed:article_date ?date . 
  FILTER (?date >= "2011-08-01T00:00:00Z"^^xsd:dateTime ) .
  ?entity purl:title ?title . 
  FILTER regex(?title, "breast", "i") . 
  ?entity <http://bio2rdf.org/pubmed_vocabulary:mesh_heading> ?heading . 
  ?heading a <http://bio2rdf.org/pubmed_vocabulary:MeshHeading> . 
  ?heading pubmed:mesh_descriptor_name ?descriptor . 
  FILTER regex(?descriptor, "breast", "i") . 
  ?entity ?property ?value .
}