

// Captcha functionality
function generateCaptcha() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';
    for (let i = 0; i < 6; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

// Initialize components
const urlInput = document.getElementById('urlInput');
const captchaDiv = document.getElementById('captcha');
const captchaInput = document.getElementById('captchaInput');
const shortenBtn = document.getElementById('shortenBtn');
const resultContainer = document.getElementById('result');
const shortUrlInput = document.getElementById('shortUrl');
const copyBtn = document.getElementById('copyBtn');

let currentCaptcha = '';

// Generate initial captcha
function refreshCaptcha() {
    currentCaptcha = generateCaptcha();
    captchaDiv.textContent = currentCaptcha;
}

refreshCaptcha();

// URL shortening process
shortenBtn.addEventListener('click', () => {
    const url = urlInput.value.trim();
    const captchaValue = captchaInput.value.trim();

    // Validation
    if (!url) {
        alert('Please enter a URL');
        return;
    }

    try {
        new URL(url);
    } catch {
        alert('Please enter a valid URL');
        return;
    }

    if (captchaValue.toUpperCase() !== currentCaptcha) {
        alert('Invalid verification code');
        refreshCaptcha();
        captchaInput.value = '';
        return;
    }


    // Reset form
    refreshCaptcha();
    captchaInput.value = '';
});

// Copy functionality
copyBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(shortUrlInput.value);
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
        }, 2000);
    } catch (err) {
        alert('Failed to copy URL');
    }
});

// Smooth scrolling for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

document.getElementById("shortenBtn").addEventListener("click", function () {
    let urlInput = document.getElementById("urlInput").value;

    if (!urlInput) {
        alert("Please enter a valid URL.");
        return;
    }

    fetch("/quicklink", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: urlInput }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.Short_url) {
            let shortUrl = `${window.location.origin}/quicklink/${data.Short_url}`;
            document.getElementById("shortUrl").value = shortUrl;
            document.getElementById("result").classList.remove("hidden");
        } else {
            alert("Error: " + JSON.stringify(data));
        }
    })
    .catch(error => console.error("Error:", error));
});

document.getElementById("copyBtn").addEventListener("click", function () {
    let shortUrlField = document.getElementById("shortUrl");
    shortUrlField.select();
    document.execCommand("copy");
    alert("Short URL copied to clipboard!");
});