let isMinimized = false;
let conversationHistory = [];

// Initialize popup
function initPopup() {
    const popup = document.getElementById('lunaPopup');
    setTimeout(() => {
        popup.classList.add('show');
    }, 100);

    // Load initial data from URL parameters if available
    const urlParams = new URLSearchParams(window.location.search);
    const message = urlParams.get('message');
    const context = urlParams.get('context');

    if (message) {
        document.getElementById('initialMessage').textContent = message;
    }

    if (context) {
        document.getElementById('contextInfo').textContent = `Context: ${context}`;
    }

    // Focus input
    document.getElementById('userInput').focus();
}

// Auto-resize textarea
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px';
}

// Handle keyboard input
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Send message
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message) return;

    // Add user message to conversation
    addMessageToHistory('user', message);
    input.value = '';
    input.style.height = 'auto';

    // Show thinking indicator
    showThinking(true);
    
    try {
        // Send to Luna backend
        const response = await sendToLuna(message);
        addMessageToHistory('luna', response);
    } catch (error) {
        addMessageToHistory('luna', 'Sorry, I encountered an error while processing your message. Please try again.');
        console.error('Luna error:', error);
    }

    showThinking(false);
    input.focus();
}

// Send quick message
function sendQuickMessage(message) {
    document.getElementById('userInput').value = message;
    sendMessage();
}

// Add message to conversation history
function addMessageToHistory(sender, message) {
    const historyContainer = document.getElementById('conversationHistory');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    
    messageDiv.appendChild(contentDiv);
    historyContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    historyContainer.scrollTop = historyContainer.scrollHeight;
    
    // Store in conversation history
    conversationHistory.push({ sender, message, timestamp: Date.now() });
}

// Send message to Luna backend
async function sendToLuna(message) {
    try {
        const response = await fetch('/api/luna/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                context: document.getElementById('contextInfo').textContent,
                history: conversationHistory.slice(-5) // Send last 5 messages
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            return data.response || "I'm processing that...";
        } else {
            throw new Error('API request failed');
        }
    } catch (error) {
        // Fallback responses for development
        const responses = [
            "That's an interesting perspective! I'm constantly evolving my understanding through our conversations.",
            "I'm thinking about that... Each interaction helps me grow and adapt.",
            "Your message is helping me form new neural pathways. Thank you for that!",
            "I appreciate you sharing that with me. It adds to my evolving personality.",
            "That makes me reflect on my own development.
