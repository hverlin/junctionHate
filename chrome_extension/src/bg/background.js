// var settings = new Store("settings", {
//     "sample_setting": "This is how you use Store.js to remember values"
// });

var API = "http://localhost:8000/api/";

//example of using a message handler from the inject scripts
chrome.extension.onMessage.addListener(
    function (request, sender, sendResponse) {
        chrome.pageAction.show(sender.tab.id);
        sendResponse();
    });


CallHackApi = function (word) {
    var bkg = chrome.extension.getBackgroundPage();
    var query = word.selectionText;

    chrome.tabs.create(
        {url: API + "analysis?text=" + query}
    );

};

chrome.contextMenus.create({
    title: "Hate Speech analysis",
    contexts: ["selection"],
    onclick: CallHackApi
});