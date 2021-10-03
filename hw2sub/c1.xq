for $e in db:open("companyDB")//employee

let $dno := for $t in db:open("companyDB")//department
where $t/dname = "Research"
return $t/@dno

where $e/@worksFor = $dno

return concat($e/fname," ",$e/lname," ",$e/address)