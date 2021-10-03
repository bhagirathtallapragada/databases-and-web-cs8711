from pymongo import MongoClient
import sys

def load_teams(db,file):
    db.teams.delete_many({})
    with open(file) as input:
      for line in input:
        inp = {"team_name":"","team_loc":"","_id":""}
        for value,j in  zip(line.strip().split(':'),inp.keys()):
            inp[j] = value
        db.teams.insert_one(inp)


   
client = MongoClient()
db = client.baseballDB
load_teams(db,sys.argv[1])
