## For each customer, find a list of Order Numbers they have placed.

from pymongo import MongoClient
client = MongoClient()

#db.customers.aggregate({$project: {"CNO":1,"_id":0}})
#db.orders.find({"CUSTOMER": {$in: [1111,2222,3333]}},{"CUSTOMER":1,"ONO":1,"_id":0})

def query(customers, orders, db):
    query = {}

    query['$project']={"CNO":1,"_id":0}
    # print(query)

    c=list(db.customers.aggregate([query]))
    c1=[]
    for k in range(len(c)):
        c1.append(c[k]['CNO'])
    
    print(c1)
    res=[]
    for i in c1:

        query = {}
        cond = {}
        l1=[]
        cond['$eq']=i
        query['CUSTOMER']=cond
        for j in db.orders.find(query,{'CUSTOMER':1,'ONO':1,'_id':0}):
            l1.append(j['ONO'])  

        res.append({'cno':i,'orders':l1})
    
    # print(res)
    return res

def main():
    client = MongoClient()
    db = client.moDB
    cust = db.customers
    ords= db.orders
    result = query(cust, ords, db)

    print('For each customer, find a list of Order Numbers they have placed.')
    for i in result:
        print(i)

main()