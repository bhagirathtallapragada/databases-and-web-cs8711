for $t in db:open("shipsDB")//ship
where $t/battle/@outcome = "sunk"
return  $t/@name