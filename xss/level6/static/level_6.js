function setInnerText(element, value) {
    if (element.innerText) {
      element.innerText = value;
    } else {
      element.textContent = value;
    }
}

function includeGadget(url) {
    url = url.replace( /^\s\s*/, '');
    console.log("url = " + url)

    if (url.match(/^\/\//)){
      setInnerText(document.getElementById("log"),
        "Sorry, cannot load a URL starting with \/\/.");
      return;
    }

    urlHead = url.substr(0, 8).toLowerCase()
    console.log("urlHead = " + urlHead)
    
    // This will totally prevent us from loading evil URLs!
    if (urlHead.match(/^https?:\/\//)){
      setInnerText(document.getElementById("log"),
        "Sorry, cannot load a URL containing \"http\".");
      return;
    }

    if (urlHead.match(/^data:/)){
      setInnerText(document.getElementById("log"),
        "Sorry, cannot use a data URL");
      return;
    }

    if (urlHead.match(/^ftp:/)){
      setInnerText(document.getElementById("log"),
        "Sorry, cannot load a URL containing \"ftp\".");
      return;
    }

    if (urlHead.match(/^smtp:/)){
      setInnerText(document.getElementById("log"),
        "Sorry, cannot load a URL containing \"smtp\".");
      return;
    }
    
    var scriptEl = document.createElement('script');

    // Load this awesome gadget
    scriptEl.src = url;

    // Show log messages
    scriptEl.onload = function() { 
      setInnerText(document.getElementById("log"),  
        "Loaded gadget from " + url);
    }
    scriptEl.onerror = function() { 
      setInnerText(document.getElementById("log"),  
        "Couldn't load gadget from " + url);
    }

    document.head.appendChild(scriptEl);
}

// Take the value after # and use it as the gadget filename.
function getGadgetName() { 
    return unescape(window.location.hash.substr(1)) || "/static/gadget.js";
}

includeGadget(getGadgetName());

  //Extra code so that we can communicate with the parent page
  window.addEventListener("message", function(event){
    if (event.source == parent) {
      includeGadget(getGadgetName());
    }
  }, false);
