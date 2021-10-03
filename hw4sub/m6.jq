(: Get order number and total price for each order. :)

for $j in json-doc("mo.json").ORDERS[]
let $k :=
for $i in $j.ITEMS[]
for $k in json-doc("mo.json").PARTS[]
where $k.PNO eq $i.PARTNUMBER
return $k.PRICE * $i.QUANTITY
return {"ono": $j.ONO, "total":sum($k)}


