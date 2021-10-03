from flask import abort
from flask import make_response
from flask import request
from flask import Flask, jsonify
from flask_cors import CORS
import pymongo
from pymongo import MongoClient
import sys
app = Flask(__name__)
CORS(app)

@app.route('/baseball/standings/', methods=['GET'])
def baseball_standings():
    client=MongoClient()
    db=client.baseballDB
    result={}
    row=[]
    for i in db.teams.find():
        w=0
        l=0
        t=0
        
        for j in db.games.find({'$or': [{'visiting_team_code':i['_id']},{'home_team_code':i['_id']}]}):
            if(j['visiting_team_code']==i['_id']):
                if(int(j['visiting_team_score']) < int(j['home_team_score'])):
                    w+=1
                elif(int(j['visiting_team_score']) > int(j['home_team_score'])):
                    l+=1
                else:
                    t+=1
            elif(j['home_team_code']==i['_id']):
                if(int(j['visiting_team_score']) < int(j['home_team_score'])):
                    l+=1
                elif(int(j['visiting_team_score']) > int(j['home_team_score'])):
                    w+=1
                else:
                    t+=1
        row.append({'losses':l, 'percent':round(((w+0.5*t)/(w+l+t)),3), 'tcode':i['_id'], 'ties':t, 'tname': i['team_name'], 'wins':w})
    result['standings']=row
    return jsonify(result)

@app.route('/baseball/results/<string:tcode>/', methods=['GET'])
def baseball_results(tcode):
    client=MongoClient()
    db=client.baseballDB
    result={}

    row=[]
    res=""

    for i in db.games.find({'$or': [{'visiting_team_code':tcode},{'home_team_code':tcode}]}).sort([('game_date',1)]):
        if(i['visiting_team_code']==tcode):
            if(int(i['visiting_team_score']) > int(i['home_team_score'])):
                res='WIN'
            elif(int(i['visiting_team_score']) < int(i['home_team_score'])):
                res='LOSS'
            else:
                res='TIE'
            row.append({'gdate': i['game_date'], 'opponent': "at "+i['home_team_code'], 'result':res, 'them':i['home_team_score'], 'us': i['visiting_team_score']})
        elif(i['home_team_code']==tcode):
            if(int(i['visiting_team_score']) > int(i['home_team_score'])):
                res='LOSS'
            elif(int(i['visiting_team_score']) < int(i['home_team_score'])):
                res='WIN'
            else:
                res='TIE'
            row.append({'gdate': i['game_date'], 'opponent': i['visiting_team_code'], 'result':res, 'them':i['visiting_team_score'], 'us': i['home_team_score']})
    result['results']=row
    result['tloc']=db.teams.find({'_id':tcode},{'team_loc':1})[0]['team_loc']
    result['tname']=db.teams.find({'_id':tcode},{'team_name':1})[0]['team_name']

    return jsonify(result)

app.run(debug=True)