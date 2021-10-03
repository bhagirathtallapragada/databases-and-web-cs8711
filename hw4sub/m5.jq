(: Get order numbers of orders that took longer than 2 days to ship. :)

for $k in json-doc("mo.json").ORDERS[]
where date($k.SHIPPEDDATE)-date($k.RECEIVEDDATE) > dayTimeDuration("P2D")
return $k.ONO