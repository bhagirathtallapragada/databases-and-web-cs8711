## Get the names of parts that cost less than 20.00

from pymongo import MongoClient
client = MongoClient()

#db.parts.find({PRICE:{$lt: 20}},{PNAME:1,_id:0})

def query(parts,db):
  query = {}
  cond = {}
  cond['$lt']=20
  query['PRICE']=cond
  pname = db.parts.find(query,{'PNAME':1,'_id':0})
  return pname

def main():
  client = MongoClient()
  db = client.moDB
  parts = db.parts
  result = query(parts,db)
  print('Get the names of parts that cost less than 20.00')
  for i in result:
    print(i)

main()