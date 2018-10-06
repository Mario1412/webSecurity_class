$(document).ready(function () {
    $("#tab1").click(function () {
        chooseTab(1);
    });
    $("#tab2").click(function () {
        chooseTab(2);
    });
    $("#tab3").click(function () {
        chooseTab(3);
    });
});

function html2Escape(sHtml) {
    return sHtml.replace(/[<>&"]/g, function (c) {
        return {'<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;'}[c];
    });
}

function chooseTab(num) {
    // Dynamically load the appropriate image.
    // var html = "Image " + parseInt(num) + "<br>";
    // console.log(html2Escape(num));
    // html += "<img src='https://xss-game.appspot.com/static/level3/cloud" + html2Escape(num) + ".jpg' />";

    // Although I think the professor want us to do 'escape' here, which I state in upper code, but here the code
    // received is int type. So my method is filtering the number directly.
    var numT = parseInt(num);
    if (isNaN(numT))
        return;
    var html = "Image " + numT + "<br>";
    html += "<img src='https://xss-game.appspot.com/static/level3/cloud" + numT + ".jpg' />";


    $('#tabContent').html(html);

    window.location.hash = numT;

    // Select the current tab
    var tabs = document.querySelectorAll('.tab');
    for (var i = 0; i < tabs.length; i++) {
        if (tabs[i].id == "tab" + numT) {
            tabs[i].className = "tab active";
        } else {
            tabs[i].className = "tab";
        }
    }

    // Tell parent we've changed the tab
    top.postMessage(self.location.toString(), "*");
}

window.onload = function () {
    chooseTab(unescape(unescape(self.location.hash.substr(1)) || "1"));
}