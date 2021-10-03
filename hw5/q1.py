import rdflib
var="gas"
g = rdflib.Graph()
g.parse("PeriodicTable.owl")
print("graph has %s statements." % len(g))
qres = g.query(
"""
PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
SELECT (str(?n) as ?NAME)
{ 
?e table:name ?n;
   table:standardState table:"""+var+""". 
}
""")

ls=[]
for row in qres:
    print("%s" % row)
    ls.append("%s" % row)
print(ls)


"""
for row in qres:
#  print("%s %s %s %s" % row)
  print(row['NAME'],row['SYMBOL'],row['ATOMICWEIGHT'],row['COLOR'])
"""