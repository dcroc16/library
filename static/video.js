window.addEventListener('DOMContentLoaded',function(err){

       var video = document.getElementById('video'),
       videoObj = {'video': true },
       errBack = function(err){
           console.log("video capture error: ", err.code);
       };

    //put video listener into place
    if(navigator.getUserMedia){
        navigator.getUserMedia(videoObj, function(stream){
           video.src = stream;
           video.play();
        }, errBack);
    }else if(navigator.webkitGetUserMedia){
        navigator.webkitGetUserMedia(videoObj, function(stream){
            video = window.webkitURL.createObjectURL(stream);
            video.play();
        }, errBack);
    }else if(navigator.mozGetUserMedia){
        navigator.mozGetUserMedia(videoObj, function(stream){
        
            video.src = window.URL.createObjectURL(stream);
            video.play();
        
        }, errBack);
    } 
},false);
