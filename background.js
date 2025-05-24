"user strict";
console.log("background.js runs");

// Changed from chrome.browserAction.onClicked to chrome.action.onClicked for Manifest V3
chrome.action.onClicked.addListener(IconClicked);

function IconClicked(tab) {
    let msg = {
        txt: "Icon Clicked!"
    }
    // You might want to consider if this message is actually used by contentScript.js
    // or if it's just for debugging. The "generate" message is sent from popup.js.
    chrome.tabs.sendMessage(tab.id, msg);
}