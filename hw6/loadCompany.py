import sys
import csv
from py2neo import Graph, Node, Relationship, NodeMatcher

def loadDepartments(g,fname, fname2):
  with open(fname, 'r') as f:
    rows = list(csv.reader(f))
  with open(fname2, 'r') as f1:
    rows2 = list(csv.reader(f1))

  for row in rows:
    r = row[0].split(':')
    for row2 in rows2:
      r2=row2[0].split(':')
      if (r[1]==r2[0]):
        if (len(r2)>2):
          n = Node("Department", name=r[0], number=r[1], mgrssn=r[2], startdate=r[3], location=r2[1:])
        elif (len(r2)==2):
          n = Node("Department", name=r[0], number=r[1], mgrssn=r[2], startdate=r[3], location=r2[1])
        g.create(n)

def loadDependents(g,fname):
  with open(fname, 'r') as f:
    rows = list(csv.reader(f))
  for row in rows:
    r = row[0].split(':')
    n = Node("Dependent", dssn=r[0], name=r[1], sex=r[2], birthdate=r[3], relationship=r[4]) 
    g.create(n)

def loadProjects(g,fname):
  with open(fname, 'r') as f:
    rows = list(csv.reader(f))
  for row in rows:
    r = row[0].split(':')
    n = Node("Project", name=r[0], number=r[1], Location=r[2], dept=r[3]) 
    g.create(n)

def loadEmployees(g,fname):
  with open(fname, 'r') as f:
    rows = list(csv.reader(f,delimiter=":"))
  matcher = NodeMatcher(g)
  print(rows[0])
  for r in rows:
    # r = row[0].split(':')
    n = Node("Employee", fname=r[0], minit=r[1], lname=r[2], ssn=r[3], bdate=r[4], address=r[5], sex=r[6], salary=r[7], mgr=r[8],dnumber=r[9])
    g.create(n)

def loadDependentsOf(g,fname):
  with open(fname, 'r') as f:
    rows = list(csv.reader(f))
  matcher = NodeMatcher(g)
  for row in rows:
    r = row[0].split(':')
    query = """
      MATCH (e:Employee),(d:Dependent)
      WHERE e.ssn = $eid AND d.dssn = $eid
      CREATE (d)-[r:Dependents_of]->(e)
      CREATE (e)-[q:Dependent]->(d)
      RETURN q.name
    """
    g.run(query,eid=r[0])

#use project.dat
def loadControlledby(g,fname):
  ## load shows using cypher statement; other method does not add 
  ## multiple relationships with same name between two nodes
  ## Bug in py2neo
  with open(fname, 'r') as f:
    rows = list(csv.reader(f, delimiter=":"))
  matcher = NodeMatcher(g)
  for r in rows:
    # print(r)
    # r = row[0].split(':')
    query = """
      MATCH (p:Project),(d:Department)
      WHERE p.dept = $did AND d.number = $did
      CREATE (p)-[r:controlled_by]->(d)
      CREATE (d)-[q:controls]->(p)
      RETURN q.name
    """
    g.run(query,did=r[3])

def loadWorksOn(g,fname):
  ## load shows using cypher statement; other method does not add 
  ## multiple relationships with same name between two nodes
  ## Bug in py2neo
  with open(fname, 'r') as f:
    rows = list(csv.reader(f, delimiter=":"))
    # print(rows)
  matcher = NodeMatcher(g)
  for r in rows:
    # r = row[0].split(':')
    query = """
      MATCH (e:Employee),(p:Project)
      WHERE e.ssn = $eid AND p.number = $pid
      CREATE (e)-[r:works_on{Hours:$hrs}]->(p)
      CREATE (p)-[q:worker]->(e)
      RETURN q.name
    """
    g.run(query,eid=r[0],pid=r[1], hrs=r[2])

#use employees.dat
def loadSupervisor(g,fname):
  with open(fname, 'r') as f:
    rows = list(csv.reader(f, delimiter=":"))
  matcher = NodeMatcher(g)
  for r in rows:
    # r = row[0].split(':')
    query = """
      MATCH (e:Employee), (e2:Employee)
      WHERE e.ssn = $eid and e2.ssn=$mid
      CREATE (e)-[r:supervisor]->(e2)
      CREATE (e2)-[q:supervisee]->(e)
      RETURN q.name
    """
    g.run(query,eid=r[3],mid=r[8])

def loadManages(g,fname):
  with open(fname, 'r') as f:
    rows = list(csv.reader(f))
  matcher = NodeMatcher(g)
  for row in rows:
    r = row[0].split(':')
    query = """
      MATCH (d:Department),(e:Employee)
      WHERE d.mgrssn = $did AND e.mgr = $did
      CREATE (d)-[r:manages{Startdate:$sd}]->(e)
      CREATE (e)-[q:managed_by]->(d)
      RETURN q.name
    """
    g.run(query,did=r[2],sd=r[2])

#use employees.dat
def loadWorksFor(g,fname):
  with open(fname, 'r') as f:
    rows = list(csv.reader(f,delimiter=":"))
  matcher = NodeMatcher(g)

  for row in rows:
    # r = row[0].split(':')
    query = """
      MATCH (e:Employee),(d:Department)
      WHERE d.number = $did AND e.dnumber = $did
      CREATE (d)-[r:employs]->(e)
      CREATE (e)-[q:works_for]->(d)
      RETURN q.name
    """
    g.run(query,did=rows[9])
  # for r in rows:
  #   # r = row[0].split(':')
  #   if r[9] != 'null':
  #     print(r[9])
  #     t = matcher.match("Employee", id=r[9]).first()
  #     s = matcher.match("Department", id=r[9]).first()
  #     rel = Relationship(t, "works_for", s)
  #     g.create(rel)
  #     rel = Relationship(s, "employs", t)
  #     g.create(rel)

def main():
  g = Graph(auth=('b','123'))
  g.delete_all()
  loadEmployees(g,sys.argv[1]+"/EMPLOYEES.dat")
  loadDepartments(g,sys.argv[1]+"/DEPARTMENTS.dat", sys.argv[1]+"/DEPT_LOCATIONS.dat")
  loadProjects(g,sys.argv[1]+"/PROJECTS.dat")
  loadDependents(g,sys.argv[1]+"/DEPENDENTS.dat")
  loadWorksFor(g,sys.argv[1]+"/EMPLOYEES.dat")
  loadManages(g,sys.argv[1]+"/DEPARTMENTS.dat")
  loadWorksOn(g,sys.argv[1]+"/WORKS_ON.dat")
  loadDependentsOf(g,sys.argv[1]+"/DEPENDENTS.dat")
  loadControlledby(g,sys.argv[1]+"/PROJECTS.dat")
  loadSupervisor(g,sys.argv[1]+"/EMPLOYEES.dat")
main()