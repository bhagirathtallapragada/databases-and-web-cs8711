function submitData() {
var letters = /^[A-Za-z]+$/;
var clist = [];
var mslist = [];
var textbox = [];
 var tname = [];
var key = document.getElementsByName('sid')[0].value;var x = document.interests.sid.value;
 var y = document.interests.sid.name;textbox.push(x);
 tname.push(y);



var x = document.interests.sname.value;
 var y = document.interests.sname.name;textbox.push(x);
 tname.push(y);



var cdict_pls={};
var box1 = [];
 var box = document.getElementsByName('pls');
var bname = document.getElementsByName('pls')[0].name;
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
 strc +=")";cdict_pls.name=bname;
cdict_pls.values=strc;
clist.push(cdict_pls);


var selname = document.getElementsByName('degree')[0];
var selected2;
 for (option of selname.options) {
if (option.selected) {selected2=option.innerHTML;}}
textbox.push(selected2);
tname.push(selname.name);



var msdict_hobbies={};
var selname = document.getElementsByName('hobbies')[0];
var selected1 = [];
 for (var option of selname.options) {if (option.selected) {selected1.push(option.innerHTML);}
 else {selected1.push(null);}}
var strm="('"+key+"'";
for(i in selected1)
{
strm +=",'"+selected1[i]+"'";}
strm += ")";seln1=selname.name;
msdict_hobbies.name=seln1;
msdict_hobbies.values=strm;
mslist.push(msdict_hobbies);


var tn=document.interests.name;strt="(";
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
fdict.database="p4";
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
var x = document.interests.sid.value;
 var y = document.interests.sid.name;if (x == ""| x==null) {alert("sid must be filled out");
 return false;}
if (x.toString().length > 4) {alert("input size exceeds limit");
 return false;}
if (isNaN(x)) {alert("sid must be integer only");
 return false;}



var x = document.interests.sname.value;
 var y = document.interests.sname.name;if (x == ""| x==null) {alert("sname must be filled out");
 return false;}
if (x.toString().length > 20) {alert("input size exceeds limit");
 return false;}
if (!(x.match(letters))) {alert("sname must be string only");
 return false;}



var box1 = [];
 var box = document.getElementsByName('pls');
var bname = document.getElementsByName('pls')[0].name;
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



var selname = document.getElementsByName('degree')[0];
var selected2;
 for (option of selname.options) {
if (option.selected) {selected2=option.innerHTML;}}
if(selected2 == undefined){alert("an option must be selected"); return false};



var selname = document.getElementsByName('hobbies')[0];
var selected1 = [];
 for (var option of selname.options) {if (option.selected) {selected1.push(option.innerHTML);}}
if(selected1.length <1){alert("atleast one option must be selected"); return false};



submitData();return true }


 function displayData() {
    var url = 'http://localhost:5000/webforms/display/';
    var input =  {"backendHost":"localhost",
    "database":"p4",
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