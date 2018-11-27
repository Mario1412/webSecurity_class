var tabs_Image = {};
var current_timer;
var current_img = null;

/**
 * when the tab is activated
 */
chrome.tabs.onActivated.addListener(function (activeInfo) {
    clearTheInterval();
    console.log("Tab activated: " + activeInfo.tabId);
    chrome.extension.getBackgroundPage().current_img = null;
    console.log(current_img);

    chrome.tabs.get(activeInfo.tabId, function (tab) {
        if (chrome.runtime.lastError) {
            return;
        }
        if (tab.active && tab.status === "complete") {
            if (tabs_Image[tab.id] !== undefined) {
                if (tab.active) {
                    console.log(tab.id + "existed..." + tab.url);
                    if (tab.url && !/^chrome/.test(tab.url)) {
                        setTimeout(function () {
                            process(tab.id, tab.windowId)
                        }, 250)
                    }
                }
            }
        }
    });
});

/**
 * when the tab is updated
 */
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {

    if (tab.active && changeInfo.status === "complete") {
        clearTheInterval();

        if (tab === undefined || tab.url === undefined) {
            return;
        }

        try {
            chrome.tabs.get(tabId, function (tab) {
                if (tab.active) {
                    chrome.browserAction.setBadgeText({
                        text: "0"
                    });
                    chrome.browserAction.setBadgeBackgroundColor({
                        "tabId": tabId,
                        "color": [0, 0, 255, 200] //blue
                    });
                }
                record(tab.id, tab.windowId);
            });

        } catch (err) {
            console.log(err)
        }
    }
});

/**
 * when the tab is closed
 */
chrome.tabs.onRemoved.addListener(function (tabId, removeInfo) {
    clearTheInterval();
    delete tabs_Image[tabId];
});


