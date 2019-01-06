function switchProxy(proxyInfo) {

    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: proxyInfo[0],
                port: parseInt(proxyInfo[1])
            },
            // bypassList: ["foobar.com"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function () {
    });

    console.log(proxyInfo);
    console.log("enable succeed!")
}


chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        // alert("set proxy!")
        switchProxy(request.proxyInfo)
        sendResponse({farewell: "proxy set call back!"});

    });

// alert("fb")
