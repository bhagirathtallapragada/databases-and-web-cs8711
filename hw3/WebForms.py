import sys
import json
from jsonschema import validate
import jsonschema

def generate_html(form):
    name = form['name']
    caption = form['caption']
    ele  = form['elements']
    text = '''
    <html>
                <body>
                <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
                <script type='text/javascript' src=\''''+name+'''.js'></script>
                    <h1>'''+caption+'''</h1>
                <form name = \''''+name+'''' action="javascript:validateForm()">
            '''
    for x in ele:
        etype = x["etype"]
        ename = x["ename"]
        _caption = x["caption"]
        required = "false"
        maxlength = "524288"
        size = "20"
        if "required" in x:
            required = x["required"]
        if "size" in x:
                size = x["size"]
        if "maxlength" in x:
                maxlength = x["maxlength"]

        if etype == "textbox":
            text += "<label>"+_caption+"</label> <input type='"+etype+"' name ='"+ename+"' size='"+size+"' maxlength ='"+maxlength+"' required="+required+"/><br/><br/>"
        elif etype == "multiselectlist":
            if "size" not in form:
                size = "4"
            text += "<label>"+_caption+"</label> <br/><br/> <select name ='"+ename+"' size='"+size+"' required="+required+" multiple><br/><br/>"
            for g in x['group']:
                text += "<option value ='"+g['value']+"' >"+g['caption']+"</option><br/><br/>"
            text += "</select><br/><br/>"
        elif etype == "selectlist":
            if "size" not in form:
                size = "1"
            text += "<label>"+_caption+"</label> <br/><br/> <select name ='"+ename+"' size='"+size+"' required="+required+"><br/><br/>"
            for g in x['group']:
                text += "<option value ='"+g['value']+"' >"+g['caption']+"</option><br/><br/>"
            text += "</select><br/><br/>"
        elif etype in ["checkbox","radiobutton"]:
                text += "<label>"+_caption+"</label><br/><br/>"
                if etype == "radiobutton":
                    etype = "radio"
                for g in x['group']:
                    if "checked" in g:
                        text += "<label>"+g['caption']+"</label> <input type='"+etype+"' name ='"+ename+"' checked value ='"+g['value']+"'/><br/><br/>"
                    else:
                        text += "<label>"+g['caption']+"</label> <input type='"+etype+"' name ='"+ename+"' value ='"+g['value']+"'/><br/><br/>"
        elif etype == "submit":
            text += "<input type='"+etype+"' name ='"+ename+"' value ='"+_caption+"' ><h2><div id='msg'> </div></h2></input><br/><br/>"
        elif etype == "reset":
            text += "<input type='"+etype+"' name ='"+ename+"' value ='"+_caption+"'/><br/><br/>"
        
    text += "</form><h3></h3></body></html>"
    file = open(name+".html","w")
    file.write(text)
    file.close()
    # pass

def generate_js(form):
    name = form['name']
    caption = form['caption']
    ele  = form['elements']

    #submit form
    text="function submitData() {\n"
    text+="var letters = /^[A-Za-z]+$/;\n"
    text+="var clist = [];\nvar mslist = [];\n"
    text+="var textbox = [];\n var tname = [];\n"
    for i in ele:
        if 'key' in i:
            text += "var key = document.getElementsByName('"+i["ename"]+"')[0].value;"
    for i in ele:
        etype = i["etype"]
        ename = i["ename"]
        if etype == "textbox":
            text+="var x = document."+name+"."+ename+".value;\n var y = document."+name+"."+ename+".name;"
            # text+="if (x == \"\"| x==null) {alert(\""+ename+" must be filled out\");\n return false;}\n"
            # text+="if (x.toString().length > "+i['size']+") {alert(\"input size exceeds limit\");\n return false;}\n"
            # if i['datatype'] == "integer":
                # text+="if (isNaN(x)) {alert(\""+ename+" must be integer only\");\n return false;}\n"
            # elif i['datatype'] == "string":
                # text+="if (!(x.match(letters))) {alert(\""+ename+" must be string only\");\n return false;}\n"
            text += "textbox.push(x);\n tname.push(y);\n"
            text += "\n\n\n"

        elif etype == "multiselectlist":
            text += "var msdict_"+ename+"={};\n"
            text += "var selname = document.getElementsByName('"+ename+"')[0];\n"
            text += "var selected1 = [];\n for (var option of selname.options) {"
            text += "if (option.selected) {selected1.push(option.innerHTML);}\n else {selected1.push(null);}}\n"
            # text += "if(selected1.length <1){alert(\"atleast one option must be selected\"); return false};\n"
            text += "var strm=\"('\"+key+\"'\";\nfor(i in selected1)\n{\nstrm +=\",'\"+selected1[i]+\"'\";}\nstrm += \")\";"
            text += "seln1=selname.name;\nmsdict_"+ename+".name=seln1;\nmsdict_"+ename+".values=strm;\n"
            text += "mslist.push(msdict_"+ename+");"
            text += "\n\n\n"

        elif etype == "selectlist":
            text += "var selname = document.getElementsByName('"+ename+"')[0];\n"
            text += "var selected2;\n for (option of selname.options) {\n"
            text += "if (option.selected) {selected2=option.innerHTML;}}\n"
            # text += "if(selected2 == undefined){alert(\"an option must be selected\"); return false};\n"
            text += "textbox.push(selected2);\ntname.push(selname.name);\n"
            text += "\n\n\n"
            
        elif etype == "checkbox":
            text += "var cdict_"+ename+"={};\n"
            text += "var box1 = [];\n var box = document.getElementsByName('"+ename+"');\n"
            text += "var bname = document.getElementsByName('"+ename+"')[0].name;\n"
            text += "var bCount = 0;\n"
            text +="for (var i = 0; i < box.length; i++) {\nif (box[i].checked) {\nconsole.log(box[i].value);\nbox1.push(box[i].value);\n bCount++;}\n"
            text += "else {box1.push(null);}}\n"
            # text +="if (bCount < 1) {alert(\"a choice must be selected\")\n return false;\n}\n"
            text += "var strc=\"('\"+key+\"'\";\nfor(i in box1)\n{\nstrc +=\",'\"+box1[i]+\"'\";}\n strc +=\")\";"
            text += "cdict_"+ename+".name=bname;\ncdict_"+ename+".values=strc;\n"
            text += "clist.push(cdict_"+ename+");"
            text += "\n\n\n"
        
        elif etype == "radiobutton":
            text += "var box2;\n var box = document.getElementsByName('"+ename+"');\n"
            text += "var rname= document.getElementsByName('"+ename+"')[0].name;\n"
            text += "var bCount = 0;\n"
            text +="for (var i = 0; i < box.length; i++) {\nif (box[i].checked) {\nconsole.log(box[i].value);\nbox2=box[i].value;\n bCount++;}\n}\n"
            # text +="if (bCount < 1) {alert(\"a choice must be selected\")\n return false;\n}\n"
            text += "tname.push(rname);\ntextbox.push(box2);\n"
            text += "\n\n\n"

        elif etype in ["submit","reset"]:
            pass

    
    text += "var tn=document."+name+".name;"
    text += "strt=\"(\";\nfor(i in textbox)\n{\nstrt +=\"'\"+textbox[i]+\"',\";}\nstrt = strt.slice(0,-1);\nstrt += \")\";\n\n"
    text += "strcnm=\"(\";\nfor(i in tname)\n{\nstrcnm += tname[i]+\",\";}\nstrcnm = strcnm.slice(0,-1);\nstrcnm += \")\";\n"
    # text += "\nclist.push(cdict);\nmslist.push(msdict);"
    text += "var fdict = {};\n"

    text += "fdict.tbname=tn;\nfdict.cname=strcnm;\nfdict.values=strt;\n"
    text += "if (clist.length>0){fdict.checkbox=clist};\n"
    text += "if (mslist.length >0){fdict.multiselect=mslist};\n"
    text += "fdict.backendHost=\""+form["backendHost"]+"\";\n"
    text += "fdict.database=\""+form["mysqlDB"]+"\";\n"
    text += "fdict.user=\""+form["mysqlUserID"]+"\";\n"
    text += "fdict.pwd=\""+form["mysqlPWD"]+"\";\n"
    text += "console.log(fdict);\nvar myJSON = JSON.stringify(fdict);\nconsole.log(myJSON); \n"

    text += "var url = 'http://localhost:5000/webforms/insert/';"
    text += '''
    $.ajax({
      url: url,
      type: 'POST',
      data: myJSON,
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(response) {console.log(response);$('#msg').html(response.message);}
      });

      }
     '''

    #validate form
    text+="function validateForm() {\n"
    text+="var letters = /^[A-Za-z]+$/;\n"

    for i in ele:
        etype = i["etype"]
        ename = i["ename"]
        if etype == "textbox":
            text+="var x = document."+name+"."+ename+".value;\n var y = document."+name+"."+ename+".name;"
            text+="if (x == \"\"| x==null) {alert(\""+ename+" must be filled out\");\n return false;}\n"
            text+="if (x.toString().length > "+i['size']+") {alert(\"input size exceeds limit\");\n return false;}\n"
            if i['datatype'] == "integer":
                text+="if (isNaN(x)) {alert(\""+ename+" must be integer only\");\n return false;}\n"
            elif i['datatype'] == "string":
                text+="if (!(x.match(letters))) {alert(\""+ename+" must be string only\");\n return false;}\n"
            text += "\n\n\n"

        elif etype == "multiselectlist":
            text += "var selname = document.getElementsByName('"+ename+"')[0];\n"
            text += "var selected1 = [];\n for (var option of selname.options) {"
            text += "if (option.selected) {selected1.push(option.innerHTML);}}\n"
            text += "if(selected1.length <1){alert(\"atleast one option must be selected\"); return false};\n"
            text += "\n\n\n"

        elif etype == "selectlist":
            text += "var selname = document.getElementsByName('"+ename+"')[0];\n"
            text += "var selected2;\n for (option of selname.options) {\n"
            text += "if (option.selected) {selected2=option.innerHTML;}}\n"
            text += "if(selected2 == undefined){alert(\"an option must be selected\"); return false};\n"
            text += "\n\n\n"
            
        elif etype == "checkbox":
            text += "var box1 = [];\n var box = document.getElementsByName('"+ename+"');\n"
            text += "var bname = document.getElementsByName('"+ename+"')[0].name;\n"
            text += "var bCount = 0;\n"
            text +="for (var i = 0; i < box.length; i++) {\nif (box[i].checked) {\nconsole.log(box[i].value);\nbox1.push(box[i].value);\n bCount++;}\n"
            text += "else {box1.push(null);}}\n"
            text +="if (bCount < 1) {alert(\"a choice must be selected\")\n return false;\n}\n"
            text += "\n\n\n"
        
        elif etype == "radiobutton":
            text += "var box2;\n var box = document.getElementsByName('"+ename+"');\n"
            text += "var rname= document.getElementsByName('"+ename+"')[0].name;\n"
            text += "var bCount = 0;\n"
            text +="for (var i = 0; i < box.length; i++) {\nif (box[i].checked) {\nconsole.log(box[i].value);\nbox2=box[i].value;\n bCount++;}\n}\n"
            text +="if (bCount < 1) {alert(\"a choice must be selected\")\n return false;\n}\n"
            text += "\n\n\n"

        elif etype in ["submit","reset"]:
            pass

    text += "submitData();"
    text+="return true }\n\n\n"
    text+=''' function displayData() {
    var url = 'http://localhost:5000/webforms/display/';
    var input =  {"backendHost":"'''+form["backendHost"]+'''",
    "database":"'''+form["mysqlDB"]+'''",
    "user":"'''+form["mysqlUserID"]+'''",
    "pwd":"'''+form["mysqlPWD"]+'''"}
    $.ajax({
      url: url,
      type: 'PUT',
      data: JSON.stringify(input),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(response) {
        console.log(response);
        htmlcode = "";
        for(i in response)
        {
            // console.log(i);
            obj = response[i];
            // console.log(Object.keys(obj)[0])
            htmlcode += "<table name ='"+Object.keys(obj)[0]+"'><h3>"+Object.keys(obj)[0]+"</h3>";
            for(j in obj)
            {
                console.log(obj[j]);
                obj2 = obj[j];
                htmlcode +="<tr>";
                for(n in Object.keys(obj2[0]))
                    {
                        htmlcode += "<th>"+Object.keys(obj2[0])[n]+"</th>";
                    }
                    htmlcode +="</tr>";
                for(l in obj2){
                    obj3 = obj2[l];
                    htmlcode += "<tr>";
                    for(n in obj3){
                        // console.log(obj3[n])
                        htmlcode +="<td>"+obj3[n]+"</td>"
                    }
                    htmlcode +="</tr>"
            }

            }
            htmlcode += "</table>"
            console.log(htmlcode)
            $("#dis").html(htmlcode)
            // htmlcode += "<table name='"+response[i].keys+"'>";
            // console.log(htmlcode);
            
        }
        
      }
    });

    } '''
    file = open(form['name']+".js","w")
    file.write(text)
    file.close()



    

def generate_sql(form):
    name = form['name']
    caption = form['caption']
    ele  = form['elements']
    primary = []
    text1=""
    text = "SET FOREIGN_KEY_CHECKS = 0;\n"
    text += "DROP TABLE IF EXISTS "+name+";\n"
    text += "SET FOREIGN_KEY_CHECKS = 1;\n"
    text += "CREATE TABLE "
    text += name +"(\n"

    for i in ele:
        etype = i["etype"]
        ename = i["ename"]
        if etype not in ["multiselectlist","checkbox","submit","reset"]:
            datatype = i["datatype"]
            if datatype == "integer":
                text+=ename+" "+datatype+",\n"
            elif datatype == "string":
                if 'maxlength' in i:
                    text+=ename+" "+"varchar("+i['maxlength']+"),\n"
                else:
                    text+=ename+" "+"varchar(255),\n"
            if 'key' in i:
                primary.append(ename)
                primary.append(datatype)
                text+="PRIMARY KEY("+ename+"),\n"
        
        elif etype in ["multiselectlist","checkbox"]:
            datatype = i["datatype"]
            text1 += "DROP TABLE IF EXISTS "+ename+";\n"
            text1 += "\nCREATE TABLE "
            text1+=ename+"(\n"
            groups=i['group']
            text1+=primary[0]+" "+primary[1]+",\n"
            for j in groups:
                if datatype == "integer":
                    text1+="c_"+j['value']+" "+datatype+",\n"
                elif datatype == "string":
                    if 'maxlength' in i:
                        text1+="c_"+j['value']+" "+"varchar("+i['maxlength']+"),\n"
                    else:
                        text1+="c_"+j['value']+" "+"varchar(255),\n"
            
            text1+="FOREIGN KEY ("+primary[0]+") REFERENCES "+name+"("+primary[0]+"),\n"
            text1=text1[:-2]
            text1+=");\n\n"
    
    text=text[:-2]
    text+=");\n\n"
    
    text += text1       
    file = open(form['name']+".sql","w")
    file.write(text)
    file.close()

def generate_py(form):
    name = form['name']
    #
    text = '''import mysql.connector as mysql\nfrom flask import abort\nfrom flask import make_response\nfrom flask import request\nfrom flask import Flask, jsonify\nfrom flask_cors import CORS\napp = Flask(__name__)\nCORS(app)\n
@app.route('/webforms/insert/', methods=['POST'])\ndef insert_table():

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
@app.route('/webforms/display/', methods=['GET','POST','PUT'])\ndef show_table():\n
    sql1 = "show tables"\n
    #print(sql1)\n
    db = mysql.connect(
        host=request.json['backendHost'],
        database=request.json['database'],
        user=request.json['user'],
        passwd=request.json['pwd'],
        auth_plugin='mysql_native_password'
    )\n
    cursor = db.cursor()\n
    cursor.execute(sql1)\n
    records = cursor.fetchall()\n
    result = []\n
    for i in records:\n

        sql1 = "select * from "+i[0]\n
        tb = []\n
        col = []\n
        row = {}\n
        try:\n
            sql2 = "DESCRIBE "+i[0]\n
            cursor.execute(sql2)\n
            data = cursor.fetchall()\n
            for t in data:\n
                col.append(t[0])\n
            cursor.execute(sql1)\n
            data = cursor.fetchall()\n
            for t in data:\n
                for c in range(len(col)):\n
                    row[col[c]] = t[c]\n
                tb.append(row)\n
                row = {}\n
            if len(tb)==0:
                
                for c in range(len(col)):

                    row[col[c]] = ""

                tb.append(row)
            result.append({i[0]:tb})\n
        except Exception as e:\n
            db.rollback()\n
            cursor.close()\n
            db.close()\n
            result = {"ok": False, "message": "Request failed!"}\n
            return jsonify(result)\n
    cursor.close()\n
    db.close()\n
    return jsonify(result)\n
app.run(debug=True)\n
    '''

    file = open(name+".py","w")
    file.write(text)
    file.close()

def generate_display_html(form):
    name = form["name"]
    text = '''
    <html>
    <head>
    <title> Display Tables</title><script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script src="'''+name+'''.js"></script>
    <style>
    table, th, td {
    border: 1px solid black;}
    </style></head>
    <body></script>
    <p><button name="display" onclick = "displayData()">Display Tables</button></p>
    <div id="dis"></div>
    </body>
    <html>'''
    file = open(name+"_display.html","w")
    file.write(text)
    file.close()

def validateJson(jsonData,sch):
    try:
        validate(instance=jsonData, schema=sch)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

def main():
    studentSchema = {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "$ref": "#/definitions/Welcome10",
        "definitions": {
            "Welcome10": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {
                        "type": "string",
                        "format": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "caption": {
                        "type": "string"
                    },
                    "backendURL": {
                        "type": "string",
                        "format": "uri",
                        "qt-uri-protocols": [
                            "http"
                        ]
                    },
                    "backendHost": {
                        "type": "string"
                    },
                    "backendPort": {
                        "type": "string",
                        "format": "integer"
                    },
                    "mysqlUserID": {
                        "type": "string"
                    },
                    "mysqlPWD": {
                        "type": "string"
                    },
                    "mysqlDB": {
                        "type": "string"
                    },
                    "elements": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/Element"
                        }
                    }
                },
                "required": [
                    "backendHost",
                    "backendPort",
                    "backendURL",
                    "caption",
                    "elements",
                    "mysqlDB",
                    "mysqlPWD",
                    "mysqlUserID",
                    "name"
                ],
                "title": "Welcome10"
            },
        "Element": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "etype": {
                        "type": "string"
                    },
                    "ename": {
                        "type": "string"
                    },
                    "datatype": {
                        "type": "string"
                    },
                    "key": {
                        "type": "string"
                    },
                    "caption": {
                        "type": "string"
                    },
                    "size": {
                        "type": "string",
                        "format": "integer"
                    },
                    "maxlength": {
                        "type": "string",
                        "format": "integer"
                    },
                    "required": {
                        "type": "string",
                        "format": "boolean"
                    },
                    "group": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/Group"
                        }
                    }
                },
                "required": [
                    "caption",
                    "ename",
                    "etype"
                ],
                "title": "Element"
            },
            "Group": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "checked": {
                        "type": "string"
                    },
                    "value": {
                        "type": "string"
                    },
                    "caption": {
                        "type": "string"
                    }
                },
                "required": [
                    "caption",
                    "value"
                ],
                "title": "Group"
            }
        }

    }
    with open(sys.argv[1],'r') as fp:
        form = json.load(fp)
    
    isvalid = validateJson(form,studentSchema)
    if(isvalid):
        print("Json file validated")
    else:
        print("Json file validation fails with the defined schema")
    generate_html(form)
    generate_sql(form)
    generate_js(form)
    generate_py(form)
    generate_display_html(form)

main()