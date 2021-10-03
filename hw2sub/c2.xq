for $p in db:open("companyDB")//project

let $m := 
for $t in db:open("companyDB")//department
where $t/@dno = $p/@controllingDepartment
return $t/manager/@mssn

let $e :=
for $i in db:open("companyDB")//employee
where $i/@ssn = $m
return $i

where $p/plocation = "Stafford"


return concat($p/@pnumber," ",$p/@controllingDepartment," ",$e/lname," ",$e/address," ",$e/dob)