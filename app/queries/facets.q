SELECT ?p (COUNT( ?p ) AS ?count ) 

WHERE { 
  ?s ?p ?o 
} 

GROUP BY ?p 
ORDER BY DESC(?count)
