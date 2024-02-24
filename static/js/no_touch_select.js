//  Created on : 10.09.2018, 22:47:52
//  Author     : Michael Thiermann
//  Version    : 0.01

   window.oncontextmenu = function(event) {
     event.preventDefault();
     event.stopPropagation();
     return false;
   }