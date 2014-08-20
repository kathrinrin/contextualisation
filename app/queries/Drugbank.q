PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX drugbank:<http://bio2rdf.org/drugbank_vocabulary:>

CONSTRUCT { ?entity ?property ?value . } 
  
WHERE { 
  ?entity a drugbank:Drug . 
  ?entity drugbank:indication ?indication 
  FILTER regex(?indication, "breast cancer", "i") . 
  ?entity ?property ?value 
}