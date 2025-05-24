document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('replacely-form');
    const summaryText = document.getElementById('summarytext');
    let isProcessing = false;
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (isProcessing) {
                summaryText.textContent = 'Already processing, please wait...';
                return;
            }
            
            isProcessing = true;
            
            // Show loading message
            summaryText.textContent = 'Getting transcript and generating summary...';
            
            // Get current tab URL
            chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                if (tabs[0] && tabs[0].url) {
                    const currentUrl = tabs[0].url;
                    
                    // Check if it's a YouTube URL
                    if (currentUrl.includes('youtube.com/watch')) {
                        // Extract video ID
                        const urlParams = new URLSearchParams(new URL(currentUrl).search);
                        const videoId = urlParams.get('v');
                        
                        if (videoId) {
                            // Call your Flask API
                            const apiUrl = `http://127.0.0.1:5000/summarize/api?youtube_url=${encodeURIComponent(currentUrl)}&full_transcript=true`;
                            
                            fetch(apiUrl)
                                .then(response => {
                                    if (!response.ok) {
                                        return response.json().then(err => Promise.reject(err));
                                    }
                                    return response.json();
                                })
                                .then(data => {
                                    if (data.responseText) {
                                        summaryText.textContent = data.responseText;
                                    } else {
                                        summaryText.textContent = 'No summary generated.';
                                    }
                                })
                                .catch(error => {
                                    console.error('Error:', error.message || JSON.stringify(error));
                                    if (error.error) {
                                        summaryText.textContent = `Error: ${error.error}`;
                                    } else {
                                        summaryText.textContent = `Error: ${error.message || 'Unknown error'}. Make sure the Flask server is running.`;
                                    }
                                })
                                .finally(() => {
                                    isProcessing = false;
                                });
                        } else {
                            summaryText.textContent = 'Could not extract video ID from URL.';
                            isProcessing = false;
                        }
                    } else {
                        summaryText.textContent = 'Please navigate to a YouTube video page.';
                        isProcessing = false;
                    }
                } else {
                    summaryText.textContent = 'Could not get current tab information.';
                    isProcessing = false;
                }
            });
        });
    }
});