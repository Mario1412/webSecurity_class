var defaultMessage = "Welcome!<br><br>This is your <i>personal</i>"
    + " stream. You can post anything you want here, especially madness";

var DB = new PostDB(defaultMessage);

function displayPosts() {
    var containerEl = document.getElementById("post-container");
    containerEl.innerHTML = "";

    var posts = DB.getPosts();
    for (var i=0; i<posts.length; i++) {
        // encode the posts's message from the second post
        var message;
        (i == 0) ? (message = posts[i].message) : (message = encodeText(posts[i].message));  

        var html = '<table class="message"> <tr> <td valign=top> '
            + '<img src="https://xss-game.appspot.com/static/level2_icon.png"> </td> <td valign=top '
            + ' class="message-container"> <div class="shim"></div>';

        html += '<b>You</b>';
        html += '<span class="date">' + new Date(posts[i].date) + '</span>';
        html += "<blockquote>" + message + "</blockquote";
        html += "</td></tr></table>"
        containerEl.innerHTML += html; 
    }
}

//encoding function
function encodeText(text) {
    var tempText = document.createElement("div");
    (tempText.textContent != null) ? (tempText.textContent = text) : (tempText.innerText = text);
    var output = tempText.innerHTML;
    tempText = null;
    return output;
}


window.onload = function() { 
    document.getElementById('clear-form').onsubmit = function() {
        DB.clear(function() { displayPosts() });
        return false;
    }

    document.getElementById('post-form').onsubmit = function() {
        var message = document.getElementById('post-content').value;
        DB.save(message, function() { displayPosts() } );
        document.getElementById('post-content').value = "";
        return false;
    }

    displayPosts();
}
