## Employee numbers and total sales for each employee.

from pymongo import MongoClient
client = MongoClient()

def query(orders, parts, employees, db):
    query = {}
    cond ={}

    cond['$project']={'ENO':1,'_id':0}
    
    ls=list(db.employees.aggregate([cond]))
    ans =[]
    for i in ls:
        query = {}
        cond ={}
        tot=0
        cond['$eq']=i['ENO']
        query['TAKENBY']=cond
        for j in db.orders.find(query,{'ITEMS':1,'_id':0}):
            cond ={}
            cond['$project']={'PNO':1,'PRICE':1,'_id':0}
            for k in j['ITEMS']:
                query = {}
                cond ={}
                cond['$eq']=k['PARTNUMBER']
                query['PNO']=cond
                for l in db.parts.find(query,{'PNO':1,'PRICE':1,'_id':0}):
                    tot +=  k['QUANTITY']*l['PRICE']
        ans.append(str(i['ENO'])+"   "+str(tot))
    
    return ans

def main():
    client = MongoClient()
    db = client.moDB
    ords= db.orders
    parts=db.parts
    emp=db.employees
    result = query(ords, parts, emp, db)

    print('Employee numbers and total sales for each employee.')
    for i in result:
        print(i)

main()