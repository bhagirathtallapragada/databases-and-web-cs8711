#Retrieve the names of employees who work on all projects controlled by department "5"

from py2neo import Graph
g = Graph(auth=('b','123'))
query = """
 MATCH (e:Employee)-[r:works_on]->(p), (p)-[q:controlled_by]->(d:Department) where d.number='5' RETURN distinct e.fname as fn, e.minit as mn, e.lname as ln 
"""
res = g.run(query)

ret=[]
for r in res:
    ret.append(str(r['fn'])+' '+str(r['mn'])+' '+str(r['ln']))
print(ret)