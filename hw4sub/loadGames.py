from pymongo import MongoClient
import sys

def games(db,file):
    db.games.delete_many({})
    with open(file) as input:
      for l in input:
        inp = {"game_date":"","visiting_team_code":"","home_team_code":"","visiting_team_score":"","home_team_score":""}
        for value,j in  zip(l.strip().split(':'),inp.keys()):
            inp[j] = value
        if(len(list(db.teams.find({"_id":inp["visiting_team_code"]},{"_id":1}))) == 0  or len(list(db.teams.find({"_id":inp["home_team_code"]},{"_id":1}))) == 0):
            print("Insertion failed")
        else:
            db.games.insert_one(inp)

     
client = MongoClient()
db = client.baseballDB
games(db,sys.argv[1])
