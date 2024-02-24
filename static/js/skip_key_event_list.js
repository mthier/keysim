//  Created on : 24.03.2019, 19:47:52
//  Author     : Michael Thiermann
//  Version    : 0.01

function skipKeyEvent(direction) {
    
    var numOfItems = document.getElementById("keyEventList").length;
    var currentListNr = $('#keyEventList').find(":selected").index();
    
    if(direction==="right"){
        if(currentListNr<numOfItems-1){
            $("#keyEventList").prop('selectedIndex', currentListNr+1).change();
        }
        else{
            $("#keyEventList").prop('selectedIndex', 1).change();
        }
    }
    
    if(direction==="left"){
        if(currentListNr>1){
            $("#keyEventList").prop('selectedIndex', currentListNr-1).change();
        }
        else{
            $("#keyEventList").prop('selectedIndex', numOfItems-1).change();
        }
    }
    
};
