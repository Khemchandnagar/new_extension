console.log("background script is running")

const userId = 4014;

let promise = new Promise(function (resolve, reject) {
    fetch('http://localhost:5000/getWebsites', {
        method: 'POST',
        body: JSON.stringify({ id: String(userId) }),
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json()).then(data => {
        resolve(data)
    }).catch(function (error) {
        reject(error)
    });
})

promise.then(data => {
    data.forEach((website) => {
        console.log(website)
        chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
            if (changeInfo.status === 'complete' && tab.url.includes(website['name'])) {
                take_snapshots(tabId, changeInfo, tab, website['webId']);
            }
        });
    })
});


function login(tabId, changeInfo, tab,data) {

    console.log("script is running in login")
    chrome.tabs.executeScript(tabId, {
        code: `
          console.log("scrit is running")
          const inputs = document.getElementsByTagName('input');
          const buttons = document.getElementsByTagName('button');

          let usernameInput = Array.from(inputs).filter((input) => input.type === 'email')[0];
          const passwordInput = Array.from(inputs).filter((input) => input.type === 'password')[0];
          const submitButton1 = Array.from(inputs).filter((input) => input.type === 'submit')[0];
          if(!usernameInput)
            usernameInput = inputs[7];
          const submitButton = buttons[0];
          console.log(usernameInput,passwordInput)
          console.log(submitButton)
              console.log("hello")
              if (usernameInput && passwordInput &&(submitButton || submitButton1)) {
                usernameInput.value = '${data['username']}';
                passwordInput.value = '${data['password']}';
                console.log(usernameInput,passwordInput)
                console.log(submitButton)
                if(submitButton1){
                    setTimeout( () => { console.log("after"); submitButton1.click(); },0)
                }
                else
                    setTimeout( () => { console.log("after"); submitButton.click(); },0)
              }
          `,
        runAt: 'document_idle'
    });
}


function take_snapshots(tabId, changeInfo, tab,webId) {
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
                            console.log('face match')
                            getCredentials(userId,webId).then( (data) => {
                                console.log(data)
                                login(tabId, changeInfo, tab,data[0])
                            })
                            releaseCamera()
                            return
                        }
                        if (img_id < 5)
                            sendFrame();
                        else {
                            releaseCamera()
                            alert("auto login failed! try manually or refresh the page")
                        }
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

function getCredentials(userId, webId) {
    return new Promise((resolve, reject) => {
        fetch('http://localhost:5000/getCredentials', {
            method: 'POST',
            body: JSON.stringify({ user_id: String(userId), web_id: String(webId), }),
            headers: { 'Content-Type': 'application/json' }
        }).then(response => response.json()).then(data => {
            resolve(data)
        }).catch(function (error) {
            reject(error)
        });
    })
}
