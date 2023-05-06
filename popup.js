document.addEventListener('DOMContentLoaded', function () {
    var loginBtn = document.getElementById('login-btn');
    loginBtn.addEventListener('click', function (event) {
        event.preventDefault();
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        captureImage();
    });
});

console.log("he")
const video = document.getElementById('video');
const errorMessage = document.getElementById('error-message');

navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
    video.srcObject = stream;
}).catch((error) => {
    console.error('Error accessing camera:', error);
    errorMessage.textContent = 'Please grant permission to use the camera.';
}
);


function captureImage() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');

    var ctx = canvas.getContext('2d');

    var count = 0;
    let img_id = 1;
    function sendFrame() {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        var imageData = canvas.toDataURL('image/jpeg', 0.5);
        console.log(String(img_id)) ;

        fetch('http://localhost:5000/', {
            method: 'POST',
            body: JSON.stringify({img_id : String(img_id), frame: imageData }),
            headers: { 'Content-Type': 'application/json' }
        }).then(response => response.json()).then(data => {
            console.log('Data:', data);
            img_id = parseInt(data.data)
            console.log(img_id,data.data, data.name)
            if(data.name != "unknown"){
                alert("Login successful")
                return
            }
            if(img_id < 10 )
            sendFrame();
        }).catch(function (error) {
            console.log(error);
        });
    }
    sendFrame()

}



