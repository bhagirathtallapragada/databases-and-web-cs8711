(: Get the names of customers who have ordered all parts costing less than 20.00. :)

let $parts := [
for $b in json-doc("mo.json").PARTS[]
where $b.PRICE < 20
return $b.PNO]
return

for $l in json-doc("mo.json").ORDERS[]
for $s in json-doc("mo.json").CUSTOMERS[]
let $pno :=
for $v in $l.ITEMS[]
for $r in $parts[]
where $r eq $v.PARTNUMBER
return $r
where count($pno) eq 6

where count($pno) eq 6 and $l.CUSTOMER eq $s.CNO
return $s.CNAME