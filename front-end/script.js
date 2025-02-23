// DOM Elements
const longUrlInput = document.getElementById('longUrl');
const shortenBtn = document.getElementById('shortenBtn');
const result = document.getElementById('result');
const shortUrlDiv = document.getElementById('shortUrl');
const loader = document.getElementById('loader');
const copyNotification = document.getElementById('copyNotification');

/**
 * Shortens the URL by making an API call
 */
async function shortenUrl() {
    const longUrl = longUrlInput.value.trim();
    
    if (!longUrl) {
        alert('Please enter a valid URL');
        return;
    }

    // Show loader, hide button
    toggleLoadingState(true);

    try {
        const response = await fetch('/api/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: longUrl })
        });

        if (!response.ok) {
            throw new Error('API response was not ok');
        }

        const data = await response.json();
        
        // Show result
        displayShortUrl(data.shortCode);

    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    } finally {
        toggleLoadingState(false);
    }
}

/**
 * Toggles the loading state of the UI
 * @param {boolean} isLoading 
 */
function toggleLoadingState(isLoading) {
    loader.style.display = isLoading ? 'block' : 'none';
    shortenBtn.style.display = isLoading ? 'none' : 'block';
}

/**
 * Displays the shortened URL in the UI
 * @param {string} shortCode 
 */
function displayShortUrl(shortCode) {
    result.classList.add('show');
    const shortUrl = `${window.location.origin}/api/redirect/${shortCode}`;
    shortUrlDiv.textContent = shortUrl;
    shortUrlDiv.setAttribute('data-url', shortUrl);
}

/**
 * Shows a notification when URL is copied
 */
function showCopyNotification() {
    copyNotification.style.display = 'block';
    setTimeout(() => {
        copyNotification.style.display = 'none';
    }, 2000);
}

/**
 * Handles clicking on the shortened URL
 * Copies to clipboard if possible, otherwise redirects
 */
async function handleShortUrlClick() {
    const url = shortUrlDiv.getAttribute('data-url');
    try {
        await navigator.clipboard.writeText(url);
        showCopyNotification();
    } catch (err) {
        window.location.href = url;
    }
}

// Event Listeners
shortenBtn.addEventListener('click', shortenUrl);

longUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        shortenUrl();
    }
});

shortUrlDiv.addEventListener('click', handleShortUrlClick);