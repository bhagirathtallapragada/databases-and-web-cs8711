for $s in distinct-values(db:open("shipsDB")//class/ship/battle) (: /text() :)
   return
   <battle name="{$s}">
   {
     for $t in db:open("ships")//class/ship
     where $t/battle = $s (: /text() :)
     return <ship name="{$t/@name}" />
   }
   </battle>