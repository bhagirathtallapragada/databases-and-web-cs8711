## Get the names of customers who have ordered parts only from employees living in Wichita.

from pymongo import MongoClient
client = MongoClient()

#db.employees.find({"CITY": {$eq: "Wichita"}},{"ENO":1,"_id":0})

def query(customers, orders, employees, db):
    query = {}
    cond ={}

    cond['$eq']="Wichita"
    query['CITY']=cond

    # print(query)

    e=list(db.employees.find(query,{"ENO":1,"_id":0}))
    # print(e)

    cond={}
    cond['$project']={"CNO":1,"CNAME":1, "_id":0}
    c = list(db.customers.aggregate([cond]))
    fin=[]

    for i in c:
        ct=[]
        cond2={}
        cond2['$project']={"CUSTOMER":1,"TAKENBY":1, "_id":0}
        for k in db.orders.aggregate([cond2]):
            if(k['CUSTOMER'] == i['CNO']):
                ct.append(k['TAKENBY'])


        fin.append({'cname':i['CNAME'],'CUSTOMER':i['CNO'],'eno':ct})
    
    fin2=[]
    for i in e:
        for j in fin:
            count=0
            for k in j['eno']:
                if i['ENO'] == k:
                    count+=1
            if (count == len(j['eno'])):
                fin2.append({'cname': j['cname']})
            
    return fin2

def main():
    client = MongoClient()
    db = client.moDB
    cust = db.customers
    ords= db.orders
    emp= db.employees
    result = query(cust, ords, emp, db)

    print('Get the names of customers who have ordered parts only from employees living in Wichita.')
    for i in result:
        print(i)

main()