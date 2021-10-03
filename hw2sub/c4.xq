for $t in db:open("companyDB")//manager

let $emp := 
for $e in db:open("companyDB")//employee
where $e/@ssn = $t/@mssn
return $e

where fn:count(distinct-values($emp//dependent)) >=1
return  concat($emp/fname/text()," ",$emp/lname/text())