//  Created on : 06.09.2018, 22:47:52
//  Author     : Michael Thiermann
//  Version    : 0.01

//AJAX function to send (post) the key event from the pressed button to the python webserver (Flask)
$(document).ready(function() {
    $(document).on('click','#keyEventButton',function() {
        $.ajax({
            url: "/sendkeyevent", // url definded at python webserver (@webApp.route('/sendkeyevent', methods=['GET', 'POST']))
            method: "POST",
            data: JSON.stringify($(this).attr("value")),
            contentType: 'application/json;charset=UTF-8',
            success: function(data) {
                //console.log(data);
            }
        });
    });
});