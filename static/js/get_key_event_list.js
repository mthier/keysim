//  Created on : 08.09.2018, 22:47:52
//  Author     : Michael Thiermann
//  Version    : 0.02

//AJAX function to get (GET) the key event buttons from the selected list from the python webserver (Flask)
$(document).ready(function() {
    $(document).on('change','#keyEventList',function() {
        $.ajax({
            url: "/getkeyeventlist", // url definded at python webserver (@webApp.route('/getkeyeventlist', methods=['GET', 'POST']))
            method: "POST",
            data: JSON.stringify($(this).val()),
            contentType: 'application/json;charset=UTF-8',
            success: function(data) {
                if (document.getElementsByClassName("welcome")[0].style.display !=="none")
                {
                    document.getElementsByClassName("welcome")[0].style.display = "none";
                }
                
                document.getElementById("buttonGroupID").innerHTML = data; //set the returned html code from the python webserver 
                //console.log(data)
            }
        });
    });
});
