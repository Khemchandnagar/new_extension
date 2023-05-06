console.log("background script is running")

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url.includes('codechef.com/login')) {
        take_snapshots(tabId, changeInfo, tab);
    }
});


function login(tabId, changeInfo, tab) {

    console.log("script is running")
    chrome.tabs.executeScript(tabId, {
        code: `
          console.log("scrit is running")
          const inputs = document.getElementsByTagName('input');

          const usernameInput = Array.from(inputs).filter((input) => input.type === 'text')[0]; // codeforces me 1 
          const passwordInput = Array.from(inputs).filter((input) => input.type === 'password')[0];
          const submitButton = Array.from(inputs).filter((input) => input.type === 'submit')[0];
          console.log(usernameInput,passwordInput)
          console.log(submitButton)
              console.log("hello")
              if (usernameInput && passwordInput && submitButton) {
                usernameInput.value = 'khemchandnagar182@gmail.com';
                passwordInput.value = 'Khem@123';
                console.log(usernameInput,passwordInput)
                console.log(submitButton)
                setTimeout( () => { console.log("after"); submitButton.click(); },0)
              }
          `,
        runAt: 'document_idle'
    });
}


function take_snapshots(tabId, changeInfo, tab) {
    let stream_variable = null;

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            stream_variable = stream;
            const video = document.createElement('video');
            video.srcObject = stream;
            video.onloadedmetadata = function (e) {
                video.play();
                const canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;

                let img_id = 1;
                function sendFrame() {
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    var imageData = canvas.toDataURL('image/jpeg', 0.5);

                    fetch('http://localhost:5000/', {
                        method: 'POST',
                        body: JSON.stringify({ img_id: String(img_id), frame: imageData }),
                        headers: { 'Content-Type': 'application/json' }
                    }).then(response => response.json()).then(data => {
                        console.log('Data:', data);
                        img_id = parseInt(data.data)
                        console.log(img_id, data.data, data.name)
                        if (data.name != "unknown") {
                            login(tabId, changeInfo, tab)
                            releaseCamera()
                            return
                        }
                        if (img_id < 10)
                            sendFrame();
                        else
                            releaseCamera()
                    }).catch(function (error) {
                        console.log(error);
                    });
                }
                sendFrame();
            };
        })
        .catch(function (err) {
            console.log('Error getting user media: ' + err.message);
        });

    function releaseCamera() {
        if (stream_variable) {
            stream_variable.getTracks().forEach((track) => {
                track.stop(); // stop camera stream
            });
        }
    }
}