// DOM Elements
const longUrlInput = document.getElementById('longUrl'); // Input field for the long URL
const shortenBtn = document.getElementById('shortenBtn'); // Button to trigger URL shortening
const result = document.getElementById('result'); // Container to display the result
const shortUrlDiv = document.getElementById('shortUrl'); // Div to display the shortened URL
const loader = document.getElementById('loader'); // Loader element to show during API call
const copyNotification = document.getElementById('copyNotification'); // Notification for copy action

// Auto theme switch based on local time (7pm to 8am => dark mode; 8am to 7pm => light mode)
// If user has manually set a theme, respect that instead.
function autoSwitchTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        // Use saved manual override
        if (savedTheme === 'dark') {
            document.body.classList.add('dark');
            themeSwitch.checked = true;
        } else {
            document.body.classList.remove('dark');
            themeSwitch.checked = false;
        }
    } else {
        const now = new Date();
        const hour = now.getHours();
        if (hour >= 19 || hour < 8) {
            document.body.classList.add('dark');
            themeSwitch.checked = true;
        } else {
            document.body.classList.remove('dark');
            themeSwitch.checked = false;
        }
    }
}
autoSwitchTheme(); // call on page load

// Theme Toggle with manual override storage in localStorage
const themeSwitch = document.getElementById('themeSwitch');

themeSwitch.addEventListener('change', () => {
    document.body.classList.toggle('dark');
    // Save manual override based on state
    if (document.body.classList.contains('dark')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});

/**
 * Shortens the URL by making an API call
 */
async function shortenUrl() {
    const longUrl = longUrlInput.value.trim(); // Get the value from the input field and trim whitespace
    
    if (!longUrl) { // Check if the input is empty
        alert('Please enter a valid URL'); // Alert the user if the input is empty
        return; // Exit the function
    }

    // Show loader, hide button
    toggleLoadingState(true); // Show the loader and hide the button

    try {
        const response = await fetch('/api/shorten', { // Make a POST request to the API
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Set the content type to JSON
            },
            body: JSON.stringify({ longURL: longUrl }) // Send the long URL in the request body as 'longURL'
        });

        if (!response.ok) { // Check if the response is not ok
            throw new Error('API response was not ok'); // Throw an error if the response is not ok
        }

        const data = await response.json(); // Parse the JSON response
        
        // Show result
        displayShortUrl(data.shortCode); // Display the shortened URL

    } catch (error) {
        console.error('Error:', error); // Log the error to the console
        alert('Something went wrong. Please try again.'); // Alert the user if there is an error
    } finally {
        toggleLoadingState(false); // Hide the loader and show the button
    }
}

/**
 * Toggles the loading state of the UI
 * @param {boolean} isLoading 
 */
function toggleLoadingState(isLoading) {
    loader.style.display = isLoading ? 'block' : 'none'; // Show or hide the loader
    shortenBtn.style.display = isLoading ? 'none' : 'block'; // Show or hide the button
}

/**
 * Displays the shortened URL in the UI
 * @param {string} shortCode 
 */
function displayShortUrl(shortCode) {
    result.classList.add('show'); // Add the 'show' class to the result container
    const shortUrl = `${window.location.origin}/api/redirect/${shortCode}`; // Construct the shortened URL
    shortUrlDiv.textContent = shortUrl; // Set the text content of the shortUrlDiv to the shortened URL
    shortUrlDiv.setAttribute('data-url', shortUrl); // Set the data-url attribute to the shortened URL
}

/**
 * Shows a notification when URL is copied
 */
function showCopyNotification() {
    copyNotification.style.display = 'block'; // Show the copy notification
    setTimeout(() => {
        copyNotification.style.display = 'none'; // Hide the copy notification after 2 seconds
    }, 2000);
}

/**
 * Handles clicking on the shortened URL
 * Copies to clipboard if possible, otherwise redirects
 */
async function handleShortUrlClick() {
    const url = shortUrlDiv.getAttribute('data-url'); // Get the URL from the data-url attribute
    try {
        await navigator.clipboard.writeText(url); // Try to copy the URL to the clipboard
        showCopyNotification(); // Show the copy notification
    } catch (err) {
        window.location.href = url; // Redirect to the URL if copying fails
    }
}

// Event Listeners
shortenBtn.addEventListener('click', shortenUrl); // Add click event listener to the shorten button

longUrlInput.addEventListener('keypress', (e) => { // Add keypress event listener to the input field
    if (e.key === 'Enter') { // Check if the Enter key is pressed
        shortenUrl(); // Call the shortenUrl function
    }
});

shortUrlDiv.addEventListener('click', handleShortUrlClick); // Add click event listener to the shortUrlDiv