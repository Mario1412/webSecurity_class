/**
 * capture the current page, which is stored in the tabs array
 * @param tabId
 * @param windowId
 */
function recordPage(tabId, windowId) {
    chrome.tabs.get(tabId, function (tab) {
        if (chrome.runtime.lastError) {
            return;
        }
        if (tab !== undefined) {
            if (tab.url && !/^chrome/.test(tab.url)) {
                chrome.tabs.captureVisibleTab(windowId, function (dataUrl) {
                    if (chrome.runtime.lastError) {
                        return;
                    }
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
 */
function process(id, windowId) {
    chrome.tabs.query({active: true, windowId: windowId}, function (tabs) {
        var tab = tabs[0];
        if (tab === undefined || !tab.active || tab.id !== id) {
            return;
        }
        chrome.tabs.captureVisibleTab(windowId, function (dataUrl) {
            var baseUrl = tabs_Image[id];
            console.log(baseUrl === dataUrl);
            try {
                resemble(baseUrl).compareTo(dataUrl).onComplete(function (data) {
                    current_img = data.getImageDataUrl();
                    if (data.misMatchPercentage !== 0) {
                        var script = "var img = document.createElement('img');" +
                            "img.src = '" + data.getImageDataUrl() + "';" +
                            "img.setAttribute('style', 'position: fixed; left: 0; top: 0; height: auto; width: auto; width:100%;overflow: hidden; pointer-events: none;');" +
                            "img.setAttribute('id', 'overlay');" +

                            "var d1 = document.createElement('div'); d1.id = 'overlay_div';" +
                            "d1.appendChild(img);" +
                            "document.body.appendChild(d1);" +
                            "document.body.addEventListener('click', function (ev){ " +
                            "var child=document.getElementById('overlay_div');child.parentNode.removeChild(child);},false);";
                    }

                    chrome.tabs.executeScript(id, {
                        "code": script
                    });
                    popBadge(id, windowId, data.misMatchPercentage);
                    record(id, windowId);
                });
            } catch (e) {
                console.log(e);
            }
        });
    });
}

/**
 * display the difference alert in the badge
 * @param tabId
 * @param windowId
 * @param score
 */
function popBadge(tabId, windowId, score) {
    console.log("the score is " + score);
    var color = [255, 0, 0, 200];
    if (score <= 5) {
        color = [0, 0, 255, 200]; //blue
    } else if (score <= 30) {
        color = [248, 204, 0, 200]; //yellow
    }

    chrome.tabs.query({active: true, windowId: windowId}, function (tabs) {
        var tab = tabs[0];
        if (tab === undefined || !tab.active || tab.id !== tabId) {
            return;
        }
        chrome.tabs.get(tabId, function (tab) {
            if (tab.active) {
                chrome.browserAction.setBadgeText({
                    text: score
                });
                chrome.browserAction.setBadgeBackgroundColor({
                    "tabId": tabId,
                    "color": color
                });
            }
        });
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

/**
 * clear the tab interval to make sure every new tab or activated tab has single interval
 */
function clearTheInterval() {
    if (current_timer != null) {
        clearInterval(current_timer);
        current_timer = null;
    }
}