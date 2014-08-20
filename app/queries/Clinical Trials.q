PREFIX etv:<http://eligibility.data2semantics.org/vocab/>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT { ?entity ?property ?value . } 
WHERE {
  ?entity a <http://eligibility.data2semantics.org/vocab/Trial> .
  ?entity ?property ?value .
  ?entity etv:hasCriterion ?criterion .
  ?criterion rdf:type etv:Criterion .
  ?criterion etv:hasOriginalText ?text .
  ?criterion etv:hasContent ?patternInstance. 
  ?patternInstance etv:hasConcept ?concept. 
  ?concept etv:hasConceptId ?id . 
  filter regex(?id, "^C0006142")
}