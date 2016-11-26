// var settings = new Store("settings", {
//     "sample_setting": "This is how you use Store.js to remember values"
// });


//example of using a message handler from the inject scripts
chrome.extension.onMessage.addListener(
  function (request, sender, sendResponse) {
    chrome.pageAction.show(sender.tab.id);
    console.log("here")
    sendResponse();
  });


CallHackApi = function (word) {
  var query = word.selectionText;
  chrome.tabs.create(
    { url: "http://hackhate.huguesverlin.fr/api/facebook_posts?page_name=" + query }
  );
};

chrome.contextMenus.create({
  title: "Hate Speech analysis",
  contexts: ["selection"],
  onclick: CallHackApi
});