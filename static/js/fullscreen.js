//  Created on : 06.09.2018, 22:47:52
//  Author     : Michael Thiermann
//  Version    : 0.01

function viewFullScreen () {
    var element = document.documentElement;
    toggleFullscreen(element);
};

function toggleFullscreen (element) {
    if(document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement ||   document.msFullscreenElement){
        if(document.exitFullscreen){
            document.exitFullscreen();
        }
        else if(document.mozCancelFullScreen){
			document.mozCancelFullScreen();
        }
        else if(document.webkitExitFullscreen){
			document.webkitExitFullscreen();
		}
        else if(document.msExitFullscreen){
			document.msExitFullscreen();
        }
    }
    else{
        if(document.documentElement.requestFullscreen){
            element.requestFullscreen();
        }else if(document.documentElement.mozRequestFullScreen){
			element.mozRequestFullScreen();
        }else if(document.documentElement.webkitRequestFullscreen){
            element.webkitRequestFullscreen();
        }else if(document.documentElement.msRequestFullscreen){
            element.msRequestFullscreen();
        }
    }
};