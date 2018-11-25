/**
 * capture the current page, which is stored in the tabs array
 * @param tabId
 * @param windowId
 */
function recordPage(tabId, windowId) {
    chrome.tabs.get(tabId, function (tab) {
        if (tab.active) {
            if (tab.url && !/^chrome/.test(tab.url)) {
                chrome.tabs.captureVisibleTab(windowId, function (dataUrl) {
                    tabs_Image[tabId] = dataUrl;
                });
            }
        }
    });
}

/**
 * compare two image and calculate the scores
 * @param id
 * @param windowId
 * @param url1
 * @param url2
 */
function process(id, windowId) {
    chrome.tabs.captureVisibleTab(windowId, function (dataUrl) {
        var baseUrl = tabs_Image[id];
        console.log(baseUrl === dataUrl);
        try {
            resemble(baseUrl).compareTo(dataUrl).onComplete(function (data) {
                current_img = data.getImageDataUrl();
                popBadge(id, data.misMatchPercentage);
                record(id, windowId);
            });
        } catch (e) {
            console.log(e);
        }
    });

}

/**
 * display the difference alert in the badge
 * @param tabId
 * @param score
 */
function popBadge(tabId, score) {
    console.log("the score is " + score);
    var color = [255, 0, 0, 200];
    if (score <= 5) {
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

/**
 * regularly record the image of current page
 * @param tabId
 * @param windowId
 */
function record(tabId, windowId) {
    clearTheInterval();
    try {
        recordPage(tabId, windowId);
        current_timer = setInterval(function () {
            console.log("the interval in activeListener..." + tabId);
            recordPage(tabId, windowId);
        }, 2000);
    } catch (e) {
        console.log(e)
    }

}

function clearTheInterval() {
    if (current_timer != null) {
        clearInterval(current_timer);
        current_timer = null;
    }
}