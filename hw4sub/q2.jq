(: Assume that the last names of authors are unique. Find last names of authors along with the titles of all books they have authored. You may need the distinct-values() function to eliminate duplicates :)

let $s := distinct-values(let $list:=
for $i in  json-doc("bookstore.json").Books[]
return $i.Authors[].Last_Name
return $list)
return

for $p in $s 
return {
    "Author": $p,
    "Books" :  [
    for $v in json-doc("bookstore.json").Books[]
    where $v.Authors[][$$.Last_Name eq $p] 
    return $v.Title
    ]
}