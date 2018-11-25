var a = chrome.extension.getBackgroundPage().current_img;
if (a != null) {
    document.getElementById("inserter").src = a;
}
