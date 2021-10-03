## Get the names and cities of employees who have taken orders for parts costing less than 15.00.

from pymongo import MongoClient
client = MongoClient()

def query(parts, employees, orders, db):
    query = {}
    cond = {}
    cond['$lt']=15
    query['PRICE']=cond
    pno = db.parts.find(query,{'PNO':1,'_id':0})
    l1=[]
    for i in pno:
        l1.append(i['PNO'])
        print(i['PNO'])
    query={}
    cond={}
    cond['$in']=l1
    query['ITEMS.PARTNUMBER']=cond
    print(query)
    items=[]
    for p in db.orders.find(query,{'TAKENBY':1,'ITEMS.PARTNUMBER':1,'_id':0}):
        print(p)
        items.append(p['TAKENBY'])
    print(items)

    query = {}
    cond = {}
    cond['$in']=items
    query['ENO']=cond
    print(query)
    res=db.employees.find(query,{"ENAME":1,"CITY":1,"_id":0})
    
    return res

def main():
  client = MongoClient()
  db = client.moDB
  parts = db.parts
  emp = db.employees
  ords= db.orders
  result = query(parts, emp, ords, db)
  print(result)
  print('Get the names and cities of employees who have taken orders for parts costing less than 15.00.')
  for i in result:
    print(i)

main()