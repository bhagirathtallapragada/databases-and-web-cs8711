import rdflib
var="gas"
sym="H"
g = rdflib.Graph()
g.parse("PeriodicTable.owl")
print("graph has %s statements." % len(g))
qres = g.query(
"""
PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
SELECT (str(?n) as ?NAME) (str(?s) as ?SYMBOL) (str(?an) as ?ATOMICNUMBER) (str(?wn) as ?ATOMICWEIGHT) (str(?g) as ?GROUP) (str(?p) as ?PERIOD) (str(?b) as ?BLOCK) (str(?cL) as ?CLASSIFICATION) (str(?c) as ?COLOR)
{ 
?e table:name ?n;
   table:symbol "Ar"^^xsd:string;
   table:atomicNumber ?an;
   table:atomicWeight ?wn;
   table:group ?g;
   table:period ?p;
   table:block ?b;
   table:classification ?cl;
   table:color ?c.
}
""")

ls=[]
for row in qres:
    # print("%s %s %s %s %s %s %s %s %s" % row)
    print(row['NAME'],row['SYMBOL'],row['ATOMICNUMBER'],row['ATOMICWEIGHT'],row['GROUP'],row['PERIOD'],row['BLOCK'],row['CLASSIFICATION'],row['COLOR'])
    ls.append("%s %s %s %s %s %s %s %s %s" % row)
# print(ls)

"""
?g rdf:type table:Element;
?g table:"He"^^xsd:string.
"""