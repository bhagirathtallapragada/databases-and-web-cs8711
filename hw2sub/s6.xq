for $t in db:open("shipsDB")//class
let $year := $t/ship/@launched
(: for $s in $t/ship :)
where fn:count($t/ship/@launched) > fn:count(distinct-values($year))
return $t/@name