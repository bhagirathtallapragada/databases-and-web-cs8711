function submitData() {
var letters = /^[A-Za-z]+$/;
var clist = [];
var mslist = [];
var textbox = [];
 var tname = [];
var key = document.getElementsByName('sno')[0].value;var x = document.student.sno.value;
 var y = document.student.sno.name;textbox.push(x);
 tname.push(y);



var x = document.student.firstname.value;
 var y = document.student.firstname.name;textbox.push(x);
 tname.push(y);



var x = document.student.lastname.value;
 var y = document.student.lastname.name;textbox.push(x);
 tname.push(y);



var cdict_courses={};
var box1 = [];
 var box = document.getElementsByName('courses');
var bname = document.getElementsByName('courses')[0].name;
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
 strc +=")";cdict_courses.name=bname;
cdict_courses.values=strc;
clist.push(cdict_courses);


var selname = document.getElementsByName('status')[0];
var selected2;
 for (option of selname.options) {
if (option.selected) {selected2=option.innerHTML;}}
textbox.push(selected2);
tname.push(selname.name);



var box2;
 var box = document.getElementsByName('semester');
var rname= document.getElementsByName('semester')[0].name;
var bCount = 0;
for (var i = 0; i < box.length; i++) {
if (box[i].checked) {
console.log(box[i].value);
box2=box[i].value;
 bCount++;}
}
tname.push(rname);
textbox.push(box2);



var tn=document.student.name;strt="(";
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
fdict.database="p3";
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
var x = document.student.sno.value;
 var y = document.student.sno.name;if (x == ""| x==null) {alert("sno must be filled out");
 return false;}
if (x.toString().length > 9) {alert("input size exceeds limit");
 return false;}
if (isNaN(x)) {alert("sno must be integer only");
 return false;}



var x = document.student.firstname.value;
 var y = document.student.firstname.name;if (x == ""| x==null) {alert("firstname must be filled out");
 return false;}
if (x.toString().length > 20) {alert("input size exceeds limit");
 return false;}
if (!(x.match(letters))) {alert("firstname must be string only");
 return false;}



var x = document.student.lastname.value;
 var y = document.student.lastname.name;if (x == ""| x==null) {alert("lastname must be filled out");
 return false;}
if (x.toString().length > 20) {alert("input size exceeds limit");
 return false;}
if (!(x.match(letters))) {alert("lastname must be string only");
 return false;}



var box1 = [];
 var box = document.getElementsByName('courses');
var bname = document.getElementsByName('courses')[0].name;
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



var selname = document.getElementsByName('status')[0];
var selected2;
 for (option of selname.options) {
if (option.selected) {selected2=option.innerHTML;}}
if(selected2 == undefined){alert("an option must be selected"); return false};



var box2;
 var box = document.getElementsByName('semester');
var rname= document.getElementsByName('semester')[0].name;
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



submitData();return true }


 function displayData() {
    var url = 'http://localhost:5000/webforms/display/';
    var input =  {"backendHost":"localhost",
    "database":"p3",
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