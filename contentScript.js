console.log("content.js runs");

// Listener for messages from popup.js or background.js
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.message === "generate") { // Check the 'message' property of the incoming object
        chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
            console.log(tabs[0].url);
            var link = tabs[0].url;

            // XMLHttpRequest to fetch the current page's content
            var oReq = new XMLHttpRequest();
            oReq.open("GET", link, true);
            oReq.onreadystatechange = function() {
                if (oReq.readyState === XMLHttpRequest.DONE) {
                    if (oReq.status === 200) {
                        var result = oReq.responseText; // Use 'var' to declare result
                        // Send the fetched content back to popup.js
                        chrome.runtime.sendMessage({"message": "result", "data": result});
                    } else {
                        console.error("Error fetching URL:", oReq.status, oReq.statusText);
                        chrome.runtime.sendMessage({"message": "result", "data": "Error: Could not fetch page content (Status " + oReq.status + ")"});
                    }
                }
            };
            oReq.onerror = function() {
                console.error("Network error during XMLHttpRequest.");
                chrome.runtime.sendMessage({"message": "result", "data": "Error: Network issue while fetching page content."});
            };
            oReq.send();
        });
    }
    // If you plan to send an asynchronous response using sendResponse, you must return true.
    // In this case, we're sending a new message, so it's not strictly necessary for this specific flow,
    // but it's good practice if you ever modify the behavior to use sendResponse.
    return true; // Indicates an asynchronous response will be sent.
});

// Removed the problematic duplicated XMLHttpRequest block from here.