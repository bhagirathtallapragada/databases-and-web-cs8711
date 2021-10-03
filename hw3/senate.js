function submitData() {
var letters = /^[A-Za-z]+$/;
var clist = [];
var mslist = [];
var textbox = [];
 var tname = [];
var key = document.getElementsByName('vid')[0].value;var x = document.senate.vid.value;
 var y = document.senate.vid.name;textbox.push(x);
 tname.push(y);



var x = document.senate.vname.value;
 var y = document.senate.vname.name;textbox.push(x);
 tname.push(y);



var box2;
 var box = document.getElementsByName('rankk');
var rname= document.getElementsByName('rankk')[0].name;
var bCount = 0;
for (var i = 0; i < box.length; i++) {
if (box[i].checked) {
console.log(box[i].value);
box2=box[i].value;
 bCount++;}
}
tname.push(rname);
textbox.push(box2);



var cdict_candidate={};
var box1 = [];
 var box = document.getElementsByName('candidate');
var bname = document.getElementsByName('candidate')[0].name;
var bCount = 0;
for (var i = 0; i < box.length; i++) {
if (box[i].checked) {
console.log(box[i].value);
box1.push(box[i].value);
 bCount++;}
else {box1.push(null);}}
var strc="('"+key+"'";
for(i in box1)
{
strc +=",'"+box1[i]+"'";}
 strc +=")";cdict_candidate.name=bname;
cdict_candidate.values=strc;
clist.push(cdict_candidate);


var tn=document.senate.name;strt="(";
for(i in textbox)
{
strt +="'"+textbox[i]+"',";}
strt = strt.slice(0,-1);
strt += ")";

strcnm="(";
for(i in tname)
{
strcnm += tname[i]+",";}
strcnm = strcnm.slice(0,-1);
strcnm += ")";
var fdict = {};
fdict.tbname=tn;
fdict.cname=strcnm;
fdict.values=strt;
if (clist.length>0){fdict.checkbox=clist};
if (mslist.length >0){fdict.multiselect=mslist};
fdict.backendHost="localhost";
fdict.database="p5";
fdict.user="root";
fdict.pwd="login1995";
console.log(fdict);
var myJSON = JSON.stringify(fdict);
console.log(myJSON); 
var url = 'http://localhost:5000/webforms/insert/';
    $.ajax({
      url: url,
      type: 'POST',
      data: myJSON,
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(response) {console.log(response);$('#msg').html(response.message);}
      });

      }
     function validateForm() {
var letters = /^[A-Za-z]+$/;
var x = document.senate.vid.value;
 var y = document.senate.vid.name;if (x == ""| x==null) {alert("vid must be filled out");
 return false;}
if (x.toString().length > 8) {alert("input size exceeds limit");
 return false;}
if (isNaN(x)) {alert("vid must be integer only");
 return false;}



var x = document.senate.vname.value;
 var y = document.senate.vname.name;if (x == ""| x==null) {alert("vname must be filled out");
 return false;}
if (x.toString().length > 20) {alert("input size exceeds limit");
 return false;}
if (!(x.match(letters))) {alert("vname must be string only");
 return false;}



var box2;
 var box = document.getElementsByName('rankk');
var rname= document.getElementsByName('rankk')[0].name;
var bCount = 0;
for (var i = 0; i < box.length; i++) {
if (box[i].checked) {
console.log(box[i].value);
box2=box[i].value;
 bCount++;}
}
if (bCount < 1) {alert("a choice must be selected")
 return false;
}



var box1 = [];
 var box = document.getElementsByName('candidate');
var bname = document.getElementsByName('candidate')[0].name;
var bCount = 0;
for (var i = 0; i < box.length; i++) {
if (box[i].checked) {
console.log(box[i].value);
box1.push(box[i].value);
 bCount++;}
else {box1.push(null);}}
if (bCount < 1) {alert("a choice must be selected")
 return false;
}



submitData();return true }


 function displayData() {
    var url = 'http://localhost:5000/webforms/display/';
    var input =  {"backendHost":"localhost",
    "database":"p5",
    "user":"root",
    "pwd":"login1995"}
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

    } 