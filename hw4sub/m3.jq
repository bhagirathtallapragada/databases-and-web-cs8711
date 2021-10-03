(: Get the names of employees who have never made a sale to a customer living in their own zipcode. :)

let $an :=
for $k in json-doc("mo.json").ORDERS[]
for $l in json-doc("mo.json").CUSTOMERS[]
for $p in json-doc("mo.json").EMPLOYEES[]
where $k.CUSTOMER eq $l.CNO
and $p.ZIP eq $l.ZIP
and $k.TAKENBY eq $p.ENO
return $p.ENAME
return
distinct-values(let $ans:=
for $s in json-doc("mo.json").EMPLOYEES[]
for $h in $an 
where not $s.ENAME eq $h
return $s.ENAME
return $ans)