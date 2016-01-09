window.addEventListener('load', function(e){

    var canvas = document.getElementById('mainCanvas');
    var ctx = canvas.getContext('2d');

    var getRandomInt = function(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    var drawLines = function(randX, randY){

        var loc = Array(randX, randY);

        console.log(loc[0], loc[1]);
		ctx.lineTo(loc[0], loc[1]);
		ctx.stroke();
		ctx.beginPath();
		ctx.arc(loc[0], loc[1], 1, 0, Math.PI * 2);
		ctx.fill();
		ctx.beginPath();
		ctx.moveTo(loc[0], loc[1]);

    };
    var i = 0

    //drawLines(getRandomInt(0, 500), getRandomInt(0,500));
    i += 1

}, false);