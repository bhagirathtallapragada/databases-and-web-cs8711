(: Find all pairs of book titles of books that contain a shared author (i.e. both books have an author with same last name) :)

let $s := distinct-values(let $cno :=
for $i in  json-doc("bookstore.json").Books[]
return $i.Authors[].Last_Name
return $cno)
return


let $m := for $h in json-doc("bookstore.json").Books[]
where $h.Authors[]
return {
    "name": $h.Title,
    "auth": [$h.Authors[].Last_Name]
}
return $m

for $k in $m
for $p in $s
where $m.auth 