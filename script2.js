document.addEventListener("DOMContentLoaded", function () {
    let welcomePopup = document.getElementById("welcomePopup");
    setTimeout(function () {
        welcomePopup.classList.add("show");
    }, 2000);
});

function closePopup() {
    let welcomePopup = document.getElementById("welcomePopup");
    welcomePopup.classList.remove("show");
}

function togglePopup() {
    let chatPopup = document.getElementById("chatPopup");
    let chatButton = document.querySelector(".chatbot-button");
    
    if (chatPopup.style.display === "block") {
        chatPopup.style.display = "none";
        chatButton.style.display = "flex";
    } else {
        chatPopup.style.display = "block";
        chatButton.style.display = "none";
    }
}

