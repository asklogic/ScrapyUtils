


window.addEventListener("message", function (event) {
    // 我们只接受来自我们自己的消息

    // alert("invoke!");
    var proxyInfo = event.data.text;
    console.log("内容脚本接收到：" + event.data.text);

    proxyInfo = proxyInfo.split(':');

    chrome.runtime.sendMessage({proxyInfo: proxyInfo}, function (response) {
        console.log(response.farewell);
        // alert(response.farewell);
        console.log("end!")
    });
}, false);


// alert("sb")
