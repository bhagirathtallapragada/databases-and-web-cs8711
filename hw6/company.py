# display screen information for a given movie and city
from py2neo import Graph
import mysql.connector as mysql
from flask import abort
from flask import make_response
from flask import request
from flask import Flask, jsonify
from flask_cors import CORS
import json
import numpy as np
app = Flask(__name__)
CORS(app)



@app.route('/company/departments/', methods=['GET'])
def dep():
    g = Graph(auth=('b','123'))
    query = """
    match (d:Department) return d.number as dnum
    """
    res = g.run(query)
    ret=[]
    for r in res:
        print(r['dnum'])
        ret.append(r['dnum'])
    
    print(jsonify({"departments":ret}))
    return jsonify({"departments":ret})


@app.route('/company/employees/', methods=['GET'])
def emp():
    g = Graph(auth=('b','123'))
    query = """
    match (e:Employee) return e.ssn as ssn
    """
    res = g.run(query)
    ret=[]
    for r in res:
        # print(r['ssn'])
        ret.append(r['ssn'])
    
    print(jsonify({"employees":ret}))
    return jsonify({"employees":ret})
    

@app.route('/company/projects/', methods=['GET'])
def pro():
    g = Graph(auth=('b','123'))
    query = """
    match (p:Project) return p.number as pnum
    """
    res = g.run(query)
    ret=[]
    for r in res:
        print(r['pnum'])
        ret.append(r['pnum'])
    
    print(jsonify({"projects":ret}))
    return jsonify({"projects":ret})


@app.route('/company/pcities/', methods=['GET'])
def cities():
    fin={}
    g = Graph(auth=('b','123'))
    query = """
    match (p:Project) return collect(distinct p.Location) as loc
    """
    res = g.run(query)
    ret=[]
    
    for r in res:
        print(type(r['loc']))
        if type(r['loc'])==list:
            ret.extend(r['loc'])
        else:
            ret.extend([r['loc']])
 
    fin['cities']=list(ret)

    print(fin)
    return jsonify(fin)

@app.route('/company/dcities/', methods=['GET'])
def cities2():
    fin={}
    g = Graph(auth=('b','123'))
    query = """
    match (d:Department) return distinct d.location as loc
    """
    res = g.run(query)
    ret=[]
    
    for r in res:
        print(type(r['loc']))
        if type(r['loc'])==list:
            ret.extend(r['loc'])
        else:
            ret.extend([r['loc']])
 
    fin['cities']=list(ret)

    print(fin)
    return jsonify(fin)


@app.route('/company/cities/', methods=['GET'])
def cities25():
    fin={}
    g = Graph(auth=('b','123'))
    query = """
    match (d:Department) return distinct d.location as loc
    """
    res = g.run(query)
    ret=[]
    
    for r in res:
        print(type(r['loc']))
        if type(r['loc'])==list:
            ret.extend(r['loc'])
        else:
            ret.extend([r['loc']])
 
    fin['cities']=list(ret)

    print(fin)
    return jsonify(fin)


@app.route('/company/supervisees/<string:ssn>/', methods=['GET'])
def superv(ssn):
    g = Graph(auth=('b','123'))
    query = """
    MATCH (e:Employee)-[r:supervisee]->(f) where e.ssn=$ssn1 RETURN f.ssn as fsn
    """
    res = g.run(query,ssn1=ssn)
    ret=[]
    for r in res:
        ret.append(r['fsn'])
        
    print(jsonify({"employees": ret}))
    return jsonify({"employees": ret})

@app.route('/company/department/<int:dno>/', methods=['GET'])
def dept(dno):
    fin={}
    g = Graph(auth=('b','123'))
    query = """
    match (d:Department)-[:controls]-(b)  where d.number=$d return distinct b.name as nam, b.number as num;
    """
    # print(dno)
    res = g.run(query,d=str(dno))
    ret=[]
    for r in res:
        dict={}
        dict['pname']=r['nam']
        dict['pnumber']=r['num']
        ret.append(dict)
    print(ret)
    fin['controlled_projects']= ret
    
    query="""
    match (d:Department) where d.number=$d return d.name as dnm, d.mgrssn as mgr, d.startdate as sdt;
    """
    res = g.run(query,d=str(dno))
    for r in res:
        print(r['mgr'])
    ret=[]
    # ret.append(res['mgr'])
    fin['dname']=res['dnm']
    fin['manager_start_date']=r['sdt']
    fin['mgrssn']=res['mgr']
    # print(r['mgr'])
    #to find employees of the department
    query="""
    match (d:Department)-[r:manages]->(e) where d.number=$d return e.ssn as sn;
    """
    res = g.run(query,d=str(dno))
    
    for r in res:
        ret.append(r['sn'])
    ret.append(fin['mgrssn'])
    fin['employees']=ret

    # To find manager name
    query="""
    match (e:Employee) where e.ssn=$e return e.fname as fn, e.lname as ln
    """
    print(type(str(fin['mgrssn'])))

    res = g.run(query,e=str(fin['mgrssn']))

    for r in res:
        print(r['fn'])
    fin['manager']=str(res['fn'])+str(res['ln'])

    #locations
    query="""
    match (d:Department) where d.number=$d return collect(d.location) as loc
    """
    res = g.run(query,d=str(dno))

    for r in res:
        print(r['loc'])
    fin['locations']=res['loc']

    print(jsonify(fin))

    return jsonify(fin)        

@app.route('/company/employee/<string:ssn>/', methods=['GET'])
def empssn(ssn):
    fin={}
    g = Graph(auth=('b','123'))
    query = """
    MATCH (e:Employee),(dep:Department) WHERE e.ssn='"""+ssn+"""' and e.dnumber=dep.number RETURN distinct e.fname as fn, e.minit as mn, e.lname as ln, e.address as ad, e.bdate as bd, dep.number as dnm, e.sex as sx, dep.name as depnm, e.salary as sal, e.mgr as boss
    """
    res = g.run(query, sn=ssn)
    
    for r in res:
        print(r['ad'])
    fin['address']=res['ad']
    fin['bdate']=res['bd']
    fin['department_name']=res['depnm']
    fin['department_number']=res['dnm']
    fin['fname']=res['fn']
    fin['minit']=res['mn']
    fin['lname']=res['ln']
    fin['gender']=res['sx']
    fin['supervisor']=res['boss']
    fin['salary']=res['sal']
    
    #manages
    query = """
    MATCH (d:Department) where d.mgrssn=$sn RETURN d.name as depnm, d.number as dnm
    """
    res = g.run(query, sn=ssn)
    # for r in res:
    #     print(r['dnm'])
    print(type(res))
    print(res.keys())
    # print(res.values())

    if res.forward():
        fin['manages']={'dname': res['depnm'], 'dnumber': res['dnm']}
    else:
        fin['manages']={'dname': 'null', 'dnumber': -1}

    # for projects
    query = """
    match (e:Employee)-[q:works_on]->(p) where e.ssn=$sn return p.name as pname, p.number as pnum, q.Hours as hrs
    """
    res = g.run(query, sn=ssn)
    ls=[]
    for r in res:
        print(r['pnum'])
        
        print("In pnum")
        print(res['pname'])
        # for i in list(zip(res['hrs'], res['pname'], res['pnum'])):
            # print(i)
        ls.append({'hours':r['hrs'], 'pname':r['pname'], 'pnumber':r['pnum']})
        print("PNUM LS")
        print(ls)
    fin['projects']=ls

    #dependents
    query = """
    match (e:Employee)-[r:Dependent]->(d) where e.ssn=$sn return distinct  d.name as dname, d.birthdate as bdate, d.relationship as relationship, d.sex as gender
    """
    res = g.run(query, sn=ssn)
    ret=[]
    for r in res:
        print(r['dname'])
        ret.append({'dname':res['dname'], 'bdate':res['bdate'], 'relationship':res['relationship'], 'gender':res['gender']})
    print(ret)
    fin['dependents']=ret

    #supervisees
    query="""
    MATCH (e:Employee)-[q:supervisee]->(p) where e.ssn=$sn return collect(p.ssn) as sv
    """
    res = g.run(query, sn=ssn)
    for r in res:
        print(r['sv'])
    fin['supervisees']=res['sv']

    print(jsonify(fin))

    return jsonify(fin)

@app.route('/company/project/<int:pno>/', methods=['GET'])
def proj(pno):
    fin={}
    g = Graph(auth=('b','123'))
    query = """
    MATCH (p:Project)-[r:controlled_by]->(d) where p.number=$p RETURN distinct d.name as dnm, p.name as pnm, p.Location as plocation
    """
    res = g.run(query,p=str(pno))
    for r in res:
        print(r['dnm'])
    
    fin['controlling_dname']=res['dnm']
    fin['pname']=res['pnm']
    fin['plocation']=res['plocation']

    #employees
    query = """
    MATCH (p:Project)-[r:worker]->(d) where p.number=$p RETURN collect(d.ssn) as emp
    """
    res = g.run(query,p=str(pno))
    for r in res:
        print(r['emp'])
    fin['employees']=res['emp']

    #person hours
    query="""
    MATCH (e:Employee)-[r:works_on]->(p) where p.number=$p RETURN sum(toInteger(r.Hours)) as hrs
    """
    res = g.run(query,p=str(pno))

    for r in res:
        print(r['hrs'])
    fin['person_hours']=res['hrs']

    #dept hours
    query="""
    MATCH (e:Employee)-[r:works_on]->(p), (d:Department) where p.number=$p and d.number=e.dnumber RETURN d.name as dnm, sum(toInteger(r.Hours)) as hrs
    """
    res = g.run(query,p=str(pno))
    h1={}
    for r in res:
        h1[res['dnm']]=r['hrs']
    fin['dept_hours']=h1
    print("in project plocation: ")
    print(fin)

    return jsonify(fin)

@app.route('/company/projects/<string:cty>/', methods=['GET'])
def prot(cty):
    fin={}
    g = Graph(auth=('b','123'))
    query = """
    match(p:Project) where p.Location=$city return p.name as nm, p.number as num
    """
    res = g.run(query,city=cty)
    ret=[]
    for r in res:
        ret.append({'pname':r['nm'], 'pnumber':r['num']})
    fin['projects']=ret
    print("Get pro by city")
    print(fin)

    return jsonify(fin)

@app.route('/company/departments/<string:cty>/', methods=['GET'])
def depc(cty):
    fin={}
    g = Graph(auth=('b','123'))
    query = """
    match (d:Department) where any (loc in d.location where loc=$lc) return d.name as dnm, d.number as num
    """
    res = g.run(query,lc=cty)
    ret=[]
    for r in res:
        ret.append({'dname': r['dnm'], 'dnumber':r['num']})
    fin['departments']=ret

    print(jsonify(fin))

    return jsonify(fin)


app.run(debug=True)