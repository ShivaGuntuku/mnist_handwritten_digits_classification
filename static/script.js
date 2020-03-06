var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');

var radius = 5;  
var start = 0;
var end = Math.PI * 2;  
var dragging = false;
// window.innerHeight
canvas.width = '450'; 
canvas.height = '450'; 

context.lineWidth = radius * 2; 

var putPoint = function(e){
    if(dragging){
        context.lineTo(e.offsetX, e.offsetY);
        context.stroke();
        context.strokeStyle = '#fff';
        context.beginPath(); 
        context.arc(e.offsetX, e.offsetY, radius, start, end);
        context.fill('#fff');
        context.beginPath();
        context.moveTo(e.offsetX, e.offsetY);
    }
}

var engage = function(e){
    dragging = true;
    putPoint(e);
}

var disengage = function(){
    dragging = false;
    context.beginPath();
}

canvas.addEventListener('mousedown', engage);
canvas.addEventListener('mousemove', putPoint);
canvas.addEventListener('mouseup', disengage);


function downloadImage(filename = 'test.png') {
    var blank = document.createElement('canvas');
    blank.width = canvas.width;
    blank.height = canvas.height;
    blank.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    
    
    if (canvas.toDataURL() == blank.toDataURL())
    {
        alert('It is blank');
    }
    else
    {
        var dataURL = canvas.toDataURL("image/png", 1.0);
        // var a = document.createElement('a');
        // a.href = dataURL;
        // a.download = filename;
        // document.body.appendChild(a);
        // a.click();

        $.post("/canvasData",
            {data: dataURL},
            function(data,status){
                document.getElementById("output_digit").innerHTML = data['digit'];
                document.getElementById("counter").innerHTML = data['count'];
            }
        );
    }
}

function clearCanvas() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById("output_digit").innerHTML = '';
}
