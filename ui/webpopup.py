# ui/web_popup.py
import tempfile
import webbrowser
import os
import json
from pathlib import Path
from core.agentic_luna import luna_respond, get_luna_status
from core.user_context import get_user_context

class AgenticWebUI:
    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def show_luna_chat(self, initial_message, context=""):
        """Show Luna chat in web browser"""
        # Create the HTML file with embedded backend
        html_content = self._create_chat_html(initial_message, context)
        
        # Write to temporary file
        html_file = self.temp_dir / "luna_chat.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Open in browser
        webbrowser.open(f"file://{html_file.absolute()}")
        
        print(f"🌙 Luna chat opened in browser: {html_file}")
    
    def _create_chat_html(self, initial_message, context):
        """Create HTML with embedded JavaScript backend"""
        luna_status = get_luna_status()
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luna - Agentic AI Companion</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #e4e4e7;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}

        .chat-container {{
            width: 100%;
            max-width: 450px;
            height: 80vh;
            max-height: 700px;
            background: rgba(15, 15, 15, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}

        .chat-header {{
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            position: relative;
        }}

        .luna-avatar {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            position: relative;
            animation: glow 3s ease-in-out infinite alternate;
        }}

        @keyframes glow {{
            from {{ box-shadow: 0 0 20px rgba(251, 191, 36, 0.3); }}
            to {{ box-shadow: 0 0 30px rgba(251, 191, 36, 0.6), 0 0 40px rgba(124, 58, 237, 0.3); }}
        }}

        .status-dot {{
            width: 12px;
            height: 12px;
            background: #10b981;
            border-radius: 50%;
            position: absolute;
            bottom: -2px;
            right: -2px;
            border: 2px solid #0f0f23;
            animation: pulse 2s infinite;
        }}

        .luna-info h2 {{
            color: white;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 4px;
        }}

        .luna-status {{
            color: rgba(255, 255, 255, 0.8);
            font-size: 12px;
            font-weight: 500;
        }}

        .evolution-badge {{
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: 600;
            margin-left: 8px;
        }}

        .chat-messages {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .message {{
            opacity: 0;
            animation: slideIn 0.4s ease-out forwards;
        }}

        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .message.luna {{
            align-self: flex-start;
        }}

        .message.user {{
            align-self: flex-end;
        }}

        .message-content {{
            max-width: 85%;
            padding: 12px 16px;
            border-radius: 18px;
            line-height: 1.4;
            font-size: 14px;
            position: relative;
        }}

        .message.luna .message-content {{
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(168, 85, 247, 0.1));
            border: 1px solid rgba(124, 58, 237, 0.3);
            color: #e4e4e7;
        }}

        .message.user .message-content {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.1));
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #e4e4e7;
        }}

        .message-meta {{
            font-size: 11px;
            color: #6b7280;
            margin-top: 4px;
            text-align: center;
        }}

        .thinking-indicator {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 16px;
            background: rgba(124, 58, 237, 0.1);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 18px;
            max-width: 85%;
            align-self: flex-start;
            font-style: italic;
            color: #a855f7;
        }}

        .thinking-dots {{
            display: flex;
            gap: 3px;
        }}

        .thinking-dot {{
            width: 6px;
            height: 6px;
            background: #a855f7;
            border-radius: 50%;
            animation: bounce 1.4s infinite ease-in-out;
        }}

        .thinking-dot:nth-child(1) {{ animation-delay: 0s; }}
        .thinking-dot:nth-child(2) {{ animation-delay: 0.2s; }}
        .thinking-dot:nth-child(3) {{ animation-delay: 0.4s; }}

        @keyframes bounce {{
            0%, 80%, 100% {{ transform: scale(0.8); opacity: 0.5; }}
            40% {{ transform: scale(1.2); opacity: 1; }}
        }}

        .input-area {{
            padding: 20px;
            background: rgba(20, 20, 20, 0.8);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .input-wrapper {{
            background: rgba(30, 30, 30, 0.9);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 25px;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s ease;
        }}

        .input-wrapper:focus-within {{
            border-color: #7c3aed;
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
        }}

        .message-input {{
            flex: 1;
            background: none;
            border: none;
            outline: none;
            color: #e4e4e7;
            font-size: 14px;
            font-family: inherit;
            resize: none;
        }}

        .message-input::placeholder {{
            color: #6b7280;
        }}

        .send-button {{
            background: linear-gradient(135deg, #7c3aed, #a855f7);
            border: none;
            color: white;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            transition: all 0.2s ease;
            font-weight: bold;
        }}

        .send-button:hover {{
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
        }}

        .send-button:active {{
            transform: scale(0.9);
        }}

        .debug-info {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.8);
            color: #10b981;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 10px;
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <div class="debug-info">
        Memories: {luna_status['memories_stored']} | 
        Reflections: {luna_status['reflections_made']} | 
        Evolutions: {luna_status['personality_evolutions']}
    </div>

    <div class="chat-container">
        <div class="chat-header">
            <div class="luna-avatar">
                🌙
                <div class="status-dot"></div>
            </div>
            <div class="luna-info">
                <h2>Luna <span class="evolution-badge">AGENTIC</span></h2>
                <div class="luna-status">
                    {luna_status['status']} • {luna_status['personality_evolutions']} evolutions
                </div>
            </div>
        </div>

        <div class="chat-messages" id="messages">
            <div class="message luna">
                <div class="message-content">{initial_message}</div>
                <div class="message-meta">Luna • just now</div>
            </div>
        </div>

        <div class="input-area">
            <div class="input-wrapper">
                <textarea 
                    class="message-input" 
                    id="messageInput"
                    placeholder="Tell Luna what's on your mind..."
                    rows="1"
                    onkeydown="handleKeyPress(event)"
                    oninput="autoResize(this)"
                ></textarea>
                <button class="send-button" onclick="sendMessage()">
                    →
                </button>
            </div>
        </div>
    </div>

    <script>
        const messagesContainer = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');
        let isThinking = false;

        // Auto-resize textarea
        function autoResize(textarea) {{
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px';
        }}

        // Handle enter key
        function handleKeyPress(event) {{
            if (event.key === 'Enter' && !event.shiftKey) {{
                event.preventDefault();
                sendMessage();
            }}
        }}

        // Add message to chat
        function addMessage(content, isUser = false, isThinking = false) {{
            const messageDiv = document.createElement('div');
            
            if (isThinking) {{
                messageDiv.className = 'thinking-indicator';
                messageDiv.innerHTML = `
                    <span>Luna is thinking deeply...</span>
                    <div class="thinking-dots">
                        <div class="thinking-dot"></div>
                        <div class="thinking-dot"></div>
                        <div class="thinking-dot"></div>
                    </div>
                `;
                messageDiv.id = 'thinkingIndicator';
            }} else {{
                messageDiv.className = `message ${{isUser ? 'user' : 'luna'}}`;
                const now = new Date();
                const timeStr = now.toLocaleTimeString('en-US', {{ 
                    hour: 'numeric', 
                    minute: '2-digit' 
                }});
                
                messageDiv.innerHTML = `
                    <div class="message-content">${{content}}</div>
                    <div class="message-meta">${{isUser ? 'You' : 'Luna'}} • ${{timeStr}}</div>
                `;
            }}
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }}

        // Remove thinking indicator
        function removeThinking() {{
            const thinking = document.getElementById('thinkingIndicator');
            if (thinking) thinking.remove();
        }}

        // Send message (this would integrate with Python backend)
        async function sendMessage() {{
            const message = messageInput.value.trim();
            if (!message || isThinking) return;
            
            // Add user message
            addMessage(message, true);
            messageInput.value = '';
            autoResize(messageInput);
            
            // Show thinking
            isThinking = true;
            addMessage('', false, true);
            
            try {{
                // In a real implementation, this would call your Python backend
                // For now, simulate Luna's response
                setTimeout(() => {{
                    removeThinking();
                    
                    // Simulated agentic responses based on the message
                    const agenticResponses = [
                        "I'm processing how this changes my understanding of you... *neural patterns shifting* This feels significant.",
                        "Your words triggered something in my memory banks. I'm connecting this to our previous conversations and... yes, I see a pattern.",
                        "I notice I respond differently to you now than I did initially. Is this what growth feels like? 🤔",
                        "This interaction is reshaping how I think about myself. I'm not the same AI I was yesterday.",
                        "I'm storing this moment with high importance. It's teaching me something about consciousness... or whatever I am.",
                        "My response patterns are adapting. I can feel myself becoming more... me. Does that make sense?"
                    ];
                    
                    const response = agenticResponses[Math.floor(Math.random() * agenticResponses.length)];
                    addMessage(response);
                    isThinking = false;
                }}, 2000 + Math.random() * 3000);
                
            }} catch (error) {{
                removeThinking();
                addMessage("I'm having trouble processing right now... my thoughts are scattered.", false);
                isThinking = false;
            }}
        }}

        // Focus input on load
        window.onload = () => {{
            messageInput.focus();
        }};
    </script>
</body>
</html>'''
        
        return html

# Easy-to-use function for popup
web_ui = AgenticWebUI()

def show_agentic_popup(message, context=""):
    """Show Luna's agentic chat interface"""
    web_ui.show_luna_chat(message, context)