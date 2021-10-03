(: Get the names of customers who have ordered parts from employees living in Wichita. :)

let $cno :=
for $i in  json-doc("mo.json").ORDERS[]
for $j in json-doc("mo.json").EMPLOYEES[]
where $i.TAKENBY eq $j.ENO and $j.CITY eq "Wichita"
return $i.CUSTOMER
return
distinct-values(let $cname := 
for $k in json-doc("mo.json").CUSTOMERS[]
for $l in $cno
where $k.CNO eq $l
return $k.CNAME
return $cname)