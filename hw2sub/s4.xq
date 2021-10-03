for $t in db:open("shipsDB")//class
let $numships := fn:count($t/ship)
where $numships >= 3
 return  $t/@name