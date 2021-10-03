for $t in db:open("shipsDB")//class
where $t/@numGuns >= 10
return  $t/@name