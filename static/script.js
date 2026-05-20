async function sendMessage() {

    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    // USER MESSAGE
    chatBox.innerHTML += `
        <div class="message user">${message}</div>
    `;

    input.value = "";

    // BOT MESSAGE CONTAINER
    const botId = "bot-" + Date.now();

    chatBox.innerHTML += `
        <div class="message bot" id="${botId}">
            <span class="dots">Thinking...</span>
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    const botDiv = document.getElementById(botId);

    // STREAM RESPONSE
    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let text = "";

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        text += decoder.decode(value, { stream: true });

        botDiv.innerHTML = text;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// ENTER KEY SUPPORT
document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});