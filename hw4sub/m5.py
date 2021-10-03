## Total sale in order 1024

from pymongo import MongoClient
client = MongoClient()

# db.orders.aggregate({$project: {'ITEMS':1,_id:0}})

def query(orders, parts, db):
    query = {}
    cond ={}

    cond['$eq']=1024
    query['ONO']=cond
    ls=list(db.orders.find(query, {'ITEMS':1,'_id':0}))
    
    tot = 0
    cond['$project']={'PNO':1,'PRICE':1,'_id':0}
    for i in ls[0]['ITEMS']:
        query = {}
        cond ={}

        cond['$eq']=i['PARTNUMBER']
        query['PNO']=cond
        for j in db.parts.find(query,{'PNO':1,'PRICE':1,'_id':0}):
          tot +=  i['QUANTITY']*j['PRICE']

    return tot

def main():
    client = MongoClient()
    db = client.moDB
    ords= db.orders
    parts=db.parts
    result = query(ords, parts, db)

    print('Total sale in order 1024.')
    # for i in result:
    print(result)

main()