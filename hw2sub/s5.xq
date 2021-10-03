(: There is no class for which no ships have participated in battle hence expect a blank result for $numships/@bcnt = 0 :)
for $t in db:open("shipsDB")//class
let $numships := <shipsum sname="{$t/@name}" bcnt = "{fn:count($t//battle)}" />
 where $numships/@bcnt = 0 
 return  $numships/@sname