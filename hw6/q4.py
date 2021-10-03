#Retrieve the names of managers who have at least one dependent.

from py2neo import Graph
g = Graph(auth=('b','123'))
query = """
 match (e:Employee)<-[r:Dependents_of]-(d:Dependent), (dep:Department) where e.ssn=dep.mgrssn and e.ssn=d.dssn return e.fname as fn, e.minit as mn, e.lname as ln, collect(distinct d.name) as deps
"""
res = g.run(query)

ret=[]
for r in res:
    if(len(r['deps'])>0):
        ret.append(str(r['fn'])+' '+str(r['mn'])+' '+str(r['ln']))
print(ret)