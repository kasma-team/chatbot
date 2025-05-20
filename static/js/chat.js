document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatMessages = document.getElementById("chat-messages");

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const query = chatInput.value.trim();
        if (!query) return;

        // Display user message
        const userMessage = document.createElement("div");
        userMessage.classList.add("message", "user");
        userMessage.textContent = query;
        chatMessages.appendChild(userMessage);

        // Call API
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });
        const data = await response.json();

        // Display bot response
        const botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot");
        botMessage.textContent = data.response;
        chatMessages.appendChild(botMessage);

        // Clear input
        chatInput.value = "";
    });
});