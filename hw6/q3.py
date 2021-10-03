#Retrieve the names of all employees who have two or more dependents.

from py2neo import Graph
g = Graph(auth=('b','123'))
query = """
 MATCH (a:Employee)<-[r:Dependents_of]-(b:Dependent) where a.ssn=b.dssn RETURN a.fname as fn, a.minit as mn, a.lname as ln, collect(distinct b.name) as deps
"""
res = g.run(query)

ret=[]
for r in res:
    if(len(r['deps'])>1):
        ret.append(str(r['fn'])+' '+str(r['mn'])+' '+str(r['ln']))
print(ret)