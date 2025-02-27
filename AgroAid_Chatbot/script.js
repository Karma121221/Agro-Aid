document.addEventListener("DOMContentLoaded", function () {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendButton = document.querySelector("button");

  let voicesLoaded = false;
  let voices = [];

  function loadVoices() {
    voices = window.speechSynthesis.getVoices();
  }

  function sendMessage() {
    let message = userInput.value.trim();
    if (message === "") return; // Ignore empty messages

    // Display user message in chat
    let userMessage = document.createElement("div");
    userMessage.classList.add("chat-message", "user");
    userMessage.textContent = message;
    chatBox.appendChild(userMessage);
    userInput.value = ""; // Clear input field

    // Scroll chat to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send message to Flask backend
    fetch("http://127.0.0.1:5500/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => response.json())
      .then((data) => {
        let botMessageContainer = document.createElement("div");
        botMessageContainer.classList.add("chat-response");

        let botMessage = document.createElement("div");
        botMessage.classList.add("chat-message", "bot");
        botMessage.innerHTML = data.reply.replace(/\n/g, "<br>"); // Preserve formatting

        let speakButton = document.createElement("button");
        speakButton.classList.add("speak-button");
        speakButton.onclick = function () {
          speakText(data.reply);
        };

        botMessageContainer.appendChild(botMessage);
        botMessageContainer.appendChild(speakButton);
        chatBox.appendChild(botMessageContainer);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
      })
      .catch((error) => console.error("Error:", error));
  }

  // Enable sending message on Enter key press
  userInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") sendMessage();
  });

  // Attach sendMessage function to button click
  sendButton.addEventListener("click", sendMessage);

  // Ensure voices are loaded before speaking
  window.speechSynthesis.onvoiceschanged = function () {
    loadVoices();
  };

  // ✅ Voice assistant function (Fixes Hindi voice selection)
  function speakText(text) {
    let speech = new SpeechSynthesisUtterance();
    speech.text = text;

    // Detect Hindi text (if it contains Hindi characters)
    let isHindi = /[\u0900-\u097F]/.test(text);
    speech.lang = isHindi ? "hi-IN" : "en-US"; // Set language dynamically

    speech.rate = 1; // Normal speed
    speech.pitch = 1; // Normal pitch

    // Load available voices
    let voices = window.speechSynthesis.getVoices();

    if (isHindi) {
      let hindiVoice = voices.find((voice) => voice.lang === "hi-IN");
      if (hindiVoice) {
        speech.voice = hindiVoice;
      } else {
        console.warn("Hindi voice not found. Using default voice.");
      }
    } else {
      let englishVoice = voices.find((voice) => voice.lang === "en-US");
      if (englishVoice) {
        speech.voice = englishVoice;
      }
    }

    window.speechSynthesis.speak(speech);
  }

  // ✅ FIX: Ensure voices are properly loaded before use
  window.speechSynthesis.onvoiceschanged = function () {
    console.log("Voices loaded successfully.");
  };
});
