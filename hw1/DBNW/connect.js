    
    function buttonClick() {

        const uname = $("#uname").val();
        const password = $("#psw").val();
        const dbname = $("#dbname").val();
        // console.log('http://127.0.0.1:5000/?query={login(username:"'+uname+'",password:"'+password+'",dbname:"'+dbname+'"){conn}}');

        $.ajax({url: 'http://127.0.0.1:5000/?query={login(username:"'+uname+'",password:"'+password+'",dbname:"'+dbname+'"){table}}',
            // contentType: "application/json",
            // mimeType: "application/json",
            type:'GET',
            // async:false,
            success: function(response) {
                // console.log(response.data.login.conn);
                // htmlCode = response.data.login.conn;
                // $("#abc").html(htmlCode);
                var table = response.data.login;
                htmlcode="<form action='javascript:getSk("+table.length+")'>";
                console.log(table);
                for(i=0;i<table.length;i++)
                {
                    htmlcode += "<label>"+table[i].table+"</label><select id="+table[i].table+">";
                    window['table'+i] = table[i].table; 

                    for(j=0;j<10;j++)
                    {
                        htmlcode += "<option value='"+j+"'>"+j+"</option>";
                    }
                    htmlcode += "</select><br>";
                    // console.log(htmlcode);
                    
                }
                htmlcode += "<button id='getsk' >Get Skeleton</button><input type='reset' value='Reset'></form>"
                $("#databasetables").html(htmlcode);
            },
            error: function(error) {
                alert("ERROR");
                console.log(error);
              }
        });
    }

    function getSk(tl)
    {
        console.log(tl) //
        const uname = $("#uname").val();
        const password = $("#psw").val();
        const dbname = $("#dbname").val();
        // if
        htmlcode="";
        htmlcode2="";
        var flag=0;
        htmlcode += "<form action='javascript:runQ("+tl+")'>";
        for(i=0;i<tl;i++)
        {
            console.log(eval('table'+i));   ///
            console.log($('#'+eval('table'+i)).find(":selected").text());///
            if($('#'+eval('table'+i)).find(":selected").text()>0)
            {
                flag = 1;
                console.log("click");         ///
                console.log(eval('table'+i));  ///
                for(j=0;j<$('#'+eval('table'+i)).find(":selected").text();j++)
                {
                    var n = eval('table'+i);
                    $.ajax({url: 'http://127.0.0.1:5000/?query={params(username:"'+uname+'",password:"'+password+'",dbname:"'+dbname+'",tbname:"'+eval('table'+i)+'"){columns}}',
                    
                                type:'GET',
                                success: function(response) {
                                    console.log("In success "+n);
                                    var cols = response.data.params;
                                    htmlcode += "<table id="+n+">"+
                                                "<tr>"+
                                                "<th>"+n+"</th>";
                                    for(k=0;k<cols.length;k++)
                                    {
                                        console.log(cols[k].columns);
                                        htmlcode +=  "<th>"+cols[k].columns+"</th>";
                                    }
                                    htmlcode += "</tr>"+
                                                "<tr>";
                                    for(k=0;k<cols.length+1;k++)
                                    {            
                                        // window[n+k] = n+k; 
                                        htmlcode += "<td><input type='text' placeholder='-' id="+n+k+"></td>";
                                                
                                    }
                                    htmlcode += "</tr>"+
                                                "</table>";
                                    console.log(htmlcode);

                                    $("#qbe").html(htmlcode); 
                                },
                                error: function(error) {
                                    alert("ERROR");
                                    console.log(error);
                                  }
                            });
                }

                
                
            }
            
        }
        
        if(flag==0)
        {
            $("#qbe").html("No Tables selected");
        }
        else
        {
            htmlcode2 = "<label>Condition</label><input type='text' placeholder='condition' id='condition'>"+
                        "<button>Run Query</button></form>";
                        
        console.log(htmlcode2);
        $("#runq").html(htmlcode2); 
        }

        
    }

    function runQ(tl)
    {
        console.log(tl)
        const uname = $("#uname").val();
        const password = $("#psw").val();
        const dbname = $("#dbname").val();
        htmlcode="";
        for(i=0;i<tl;i++)
        {
            tname=eval('table'+i);
            
        }
    }
