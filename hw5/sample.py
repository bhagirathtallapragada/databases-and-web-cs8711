import rdflib

g = rdflib.Graph()
g.parse("PeriodicTable.owl")
print("graph has %s statements." % len(g))


## Query 1: Find element name, element symbol, atomic weight and color of
## all elements from the group with group name "Halogen"

qres = g.query(
"""
PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
SELECT (str(?n) as ?NAME) (str(?s) as ?SYMBOL) (str(?a) as ?ATOMICWEIGHT) (str(?c) as ?COLOR)
{ 
?g rdf:type table:Group;
   table:name "Halogen"^^xsd:string;
   table:element ?e.
?e table:name ?n;
   table:symbol ?s;
   table:atomicWeight ?a;
   table:color ?c. 
}""")

for row in qres:
  print("%s %s %s %s" % row)