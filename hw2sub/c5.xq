distinct-values(let $count:=count(db:open("companyDB")//projects/project[@controllingDepartment = "5"])
return
for $t in db:open("companyDB")//projects
return
for $i in $t/project[@controllingDepartment = "5"]/workers/worker
where count($t/project[@controllingDepartment = "5"]/workers/worker[@essn eq $i/@essn]) = $count
return concat(db:open("companyDB")//employees/employee[@ssn eq $i/@essn]/fname," ",db:open("companyDB")//employees/employee[@ssn eq $i/@essn]/lname))