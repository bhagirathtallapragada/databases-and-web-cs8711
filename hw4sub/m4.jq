(: For each employee, find a list of Order Numbers they have taken :)
let $eno :=
for $i in json-doc("mo.json").EMPLOYEES[]
return $i.ENO
return 
let $list :=
for $i in $eno
let $b := [for $j in json-doc("mo.json").ORDERS[] where $j.TAKENBY eq $i return $j.ONO]
where size($b) gt 0
return {
    "eno":$i,
    "ono":$b
}
return $list