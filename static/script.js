
window.addEventListener('load', function(){
    var imgs = {

        'princess_room':'http://www.berlinwallpaper.com/Murals/EGMurals/Princess-Castle-room-after.jpg',
        'princess_staircase':'http://previews.123rf.com/images/dazdraperma/dazdraperma1302/dazdraperma130200019/17924417-Luxury-staircase-in-the-magic-palace-Stock-Vector-castle-princess-interior.jpg',
        'princess_auoras_castle':'http://content.crealotu.com/2015/05/01/disney-princess-castle-693e91f.jpg',


    }
    var c = document.getElementById('mainCanvas');
    var ctx = c.getContext('2d');
    var myImage = new Image(100, 200);
    myImage.src = imgs['princess_auoras_castle'];
    myImage.onload = function(){

        var i = 0
        var x = window.setInterval(function() {
            if(i<1){
                ctx.drawImage(myImage,0,0,1310,650,0,0,1310,500);
                ctx.font = "24px Verdana";
                ctx.fillText("hello Princess Lexi!!!!", 550, 100);
                i +=50
            }else{
                console.log('clear');
                clearInterval(x);
            }

        },200);



    }

    window.addEventListener('click',function(){
        if(myImage.src === imgs['princess_auoras_castle']){
            myImage.src = imgs['princess_staircase'];
            myImage.onload = function(){
            ctx.drawImage(myImage,0,0,1310,650,0,0,1310,500);
                ctx.font = "24px Verdana";
                ctx.fillText("<-- Go to the Table", 10, 500);
                ctx.fillText("Go to the Kitchen -->", 1000, 500);
            }
        }else if (myImage.src === imgs['princess_staircase']){
            myImage.src = imgs['princess_room'];
            myImage.onload = function(){
            ctx.drawImage(myImage,0,0,1310,650,0,0,1310,500);
            }
        }
    },false);


}, false);
