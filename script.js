let images = [];
let currentIndex = 0;
let responses = {};
let userName = '';

async function fetchImages() {
    // Prompt the user for their name
    userName = prompt("Please enter your name:");
    if (!userName) {
        alert("Name is required to proceed!");
        return;
    }

    const response = await fetch('/images');
    images = await response.json();
    if (images.length > 0) {
        displayImage();
    } else {
        alert("No images found!");
    }
}

function displayImage() {
    const img = document.getElementById("image-display");
    if (currentIndex < images.length) {
        img.src = `/images/${images[currentIndex]}`;
    } else {
        submitResponses();
    }
}

function recordResponse(buttonValue) {
    if (currentIndex < images.length) {
        const imageName = images[currentIndex];
        responses[imageName] = buttonValue;
        currentIndex++;
        displayImage();
    }
}

async function submitResponses() {
    const response = await fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userName, responses })
    });
    if (response.ok) {
        document.getElementById("container").innerHTML = "<h1>Thank you!</h1>";
    } else {
        alert("Failed to submit responses!");
    }
}

window.onload = fetchImages;
