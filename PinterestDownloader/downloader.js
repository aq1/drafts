chrome.runtime.onMessage.addListener(function(message) {
    chrome.downloads.download({url: message.imageSrc}, function(downloadId) {
        console.log('Done', downloadId);
    });
});
