for $t in db:open("companyDB")//employee
where fn:count(distinct-values($t//dependent)) >=2
return  concat($t/fname/text()," ",$t/lname/text())