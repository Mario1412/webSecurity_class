function recordPage(tabId, windowId) {
    chrome.tabs.query({
        "active": true,
        "windowId": windowId
    }, function (id) {
        return function (tabs) {
            var tab = tabs[0];
            if (tab.url && !/^chrome/.test(tab.url)) {
                chrome.tabs.captureVisibleTab(windowId, function (dataUrl) {
                    tabs_Image[id] = dataUrl;
                });
            }
        }
    }(tabId));
}

function process(id, windowId, url1, url2) {
    resemble(url1).compareTo(url2).onComplete(function (data) {
        current_img = data.getImageDataUrl();
        popBadge(id, data.misMatchPercentage);
        record(id, windowId);
    });
}

function popBadge(tabId, score) {
    console.log("the score is " + score);
    var color = [255, 0, 0, 200];
    if (score <= 10) {
        color = [0, 0, 255, 200]; //blue
    } else if (score <= 30) {
        color = [255, 255, 0, 200]; //yellow
    }

    chrome.browserAction.setBadgeText({
        "text": "   "
    });
    chrome.browserAction.setBadgeBackgroundColor({
        "tabId": tabId,
        "color": color
    });
}

function record(tabId, windowId) {
    recordPage(tabId, windowId);
    current_timer = setInterval(function () {
        console.log("the interval in activeListener..." + tabId);
        recordPage(tabId, windowId);
    }, 2000);
}