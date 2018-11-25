var tabs_Image = {};
var current_timer;
var current_img = null;

chrome.tabs.onActivated.addListener(function (activeInfo) {
    clearInterval(current_timer);
    current_timer = null;
    chrome.extension.getBackgroundPage().current_img = null;
    console.log("Tab activated: " + activeInfo.tabId);

    chrome.tabs.get(activeInfo.tabId, function (tab) {
        if (tabs_Image[activeInfo.tabId] !== undefined) {
            console.log("tabId existed..." + tab.url);
            if (tab.url && !/^chrome/.test(tab.url)) {
                chrome.tabs.captureVisibleTab(function (dataUrl) {
                    process(activeInfo.tabId, activeInfo.windowId, tabs_Image[activeInfo.tabId], dataUrl);
                });
            }
        } else {
            clearInterval(current_timer);
            current_timer = null;
            record(tab.id, tab.windowId);
        }
    });
});

chrome.tabs.onRemoved.addListener(function (tabId, removeInfo) {
    if (removeInfo.isWindowClosing) {
        clearInterval(current_timer);
        current_timer = null;
    }
    delete tabs_Image[tabId];
});
