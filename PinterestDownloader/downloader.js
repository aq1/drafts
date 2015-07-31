chrome.runtime.onMessage.addListener(
    function(message, sender, sendResponse) {
        downloadImage(message.imageSrc, sendResponse);
    });


var downloadImage = function(url, callback) {
    chrome.downloads.download({
        url: url
    }, function(downloadId) {
        callback(true);
        console.log('Done', downloadId);
    });
};
