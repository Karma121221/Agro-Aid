document.addEventListener("DOMContentLoaded", function () {
    let welcomePopup = document.getElementById("welcomePopup");

    // Show welcome popup after 2 seconds
    setTimeout(function () {
        welcomePopup.classList.add("show");
    }, 2000);
});

// Function to Close the Welcome Popup
function closePopup() {
    let welcomePopup = document.getElementById("welcomePopup");
    welcomePopup.classList.remove("show");
}

// Function to Toggle the Chatbot Popup
function togglePopup() {
    let chatPopup = document.getElementById("chatPopup");

    // Toggle display of chatbot popup
    if (chatPopup.style.display === "block") {
        chatPopup.style.display = "none";
    } else {
        chatPopup.style.display = "block";
    }
}

