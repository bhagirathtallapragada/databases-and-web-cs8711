import mysql.connector as mysql
from flask import abort
from flask import make_response
from flask import request
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/webforms/insert/', methods=['POST'])
def insert_table():

    sql1 = "INSERT INTO "+request.json['tbname']+" "+request.json['cname']+" values "+request.json['values']
    sql2 = []
    sql3 = []
    if("checkbox" in request.json.keys()):
        for i in request.json['checkbox']:
            if(i['name']!=""):
                sql2.append("INSERT INTO "+i['name']+" values "+i['values'])

    if("multiselect" in request.json.keys()):
        for i in request.json['multiselect']:
            if(i['name']!=""):
                sql3.append("INSERT INTO "+i['name']+" values "+i['values'])

    #print(sql1)
    #print(sql2)
    #print(sql3)
    db = mysql.connect(
        host=request.json['backendHost'],
        database=request.json['database'],
        user=request.json['user'],
        passwd=request.json['pwd'],
        auth_plugin='mysql_native_password'
    )

    cursor = db.cursor()

    try:

        cursor.execute(sql1)

        
        for i in range(len(sql2)):
            #print(sql2[i])
            cursor.execute(sql2[i])
        for i in range(len(sql3)):
            #print(sql3[i])
            cursor.execute(sql3[i])
        db.commit()
        cursor.close()

        db.close()

        result = {"ok": True, "message": "Record successfully added!"}

        return jsonify(result)

    except Exception as e:

        db.rollback()

        cursor.close()

        db.close()

        result = {"ok": False, "message": "Insert request failed!"}

        return jsonify(result)
@app.route('/webforms/display/', methods=['GET','POST','PUT'])
def show_table():

    sql1 = "show tables"

    #print(sql1)

    db = mysql.connect(
        host=request.json['backendHost'],
        database=request.json['database'],
        user=request.json['user'],
        passwd=request.json['pwd'],
        auth_plugin='mysql_native_password'
    )

    cursor = db.cursor()

    cursor.execute(sql1)

    records = cursor.fetchall()

    result = []

    for i in records:


        sql1 = "select * from "+i[0]

        tb = []

        col = []

        row = {}

        try:

            sql2 = "DESCRIBE "+i[0]

            cursor.execute(sql2)

            data = cursor.fetchall()

            for t in data:

                col.append(t[0])

            cursor.execute(sql1)

            data = cursor.fetchall()

            for t in data:

                for c in range(len(col)):

                    row[col[c]] = t[c]

                tb.append(row)

                row = {}

            if len(tb)==0:
                
                for c in range(len(col)):

                    row[col[c]] = ""

                tb.append(row)
            result.append({i[0]:tb})

        except Exception as e:

            db.rollback()

            cursor.close()

            db.close()

            result = {"ok": False, "message": "Request failed!"}

            return jsonify(result)

    cursor.close()

    db.close()

    return jsonify(result)

app.run(debug=True)

    