# ui/webpopup.py
import webbrowser
import http.server
import socketserver
import threading
import tempfile
import os
import json
import urllib.parse
from pathlib import Path
import time

class LunaUIHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, luna_message="", context="", *args, **kwargs):
        self.luna_message = luna_message
        self.context = context
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Serve the Luna popup UI"""
        if self.path == '/' or self.path.startswith('/?'):
            # Parse URL parameters
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            
            message = params.get('message', [self.luna_message])[0]
            context = params.get('context', [self.context])[0]
            
            # Get the HTML content from the artifact
            html_content = get_luna_ui_html(message, context)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle Luna chat API"""
        if self.path == '/api/luna/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                user_message = data.get('message', '')
                context = data.get('context', '')
                
                # Import and use the agentic Luna system
                from core.agentic_luna import luna_respond
                
                # Get Luna's response using the agentic system
                luna_response = luna_respond(user_message, context)
                
                response = {
                    'response': luna_response,
                    'status': 'success'
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except Exception as e:
                error_response = {
                    'error': str(e),
                    'status': 'error'
                }
                
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        """Suppress server logs"""
        pass

def get_luna_ui_html(message="", context=""):
    """Return the Luna UI HTML with dynamic content"""
    
    # Use the full HTML from the artifact
    return f'''<!DOCTYPE html>
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
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            overflow: hidden;
        }}

        .popup-container {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 380px;
            max-width: calc(100vw - 40px);
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 1000;
        }}

        .popup-container.show {{
            transform: translateY(0);
            opacity: 1;
        }}

        .popup-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        }}

        .luna-info {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .luna-avatar {{
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 18px;
            position: relative;
        }}

        .luna-avatar::after {{
            content: '';
            position: absolute;
            width: 12px;
            height: 12px;
            background: #00ff88;
            border: 2px solid white;
            border-radius: 50%;
            bottom: -2px;
            right: -2px;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .luna-details h3 {{
            font-size: 16px;
            font-weight: 600;
            color: #1a1a1a;
            margin: 0;
        }}

        .luna-status {{
            font-size: 12px;
            color: #666;
            margin: 0;
        }}

        .header-actions {{
            display: flex;
            gap: 8px;
        }}

        .btn {{
            background: none;
            border: none;
            padding: 8px;
            border-radius: 8px;
            cursor: pointer;
            color: #666;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .btn:hover {{
            background: rgba(0, 0, 0, 0.05);
            color: #333;
        }}

        .minimize-btn:hover {{
            color: #667eea;
        }}

        .close-btn:hover {{
            color: #ff4757;
        }}

        .popup-body {{
            padding: 20px;
        }}

        .luna-message {{
            background: rgba(0, 0, 0, 0.02);
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 16px;
            color: #333;
            line-height: 1.5;
            font-size: 14px;
            border-left: 3px solid #667eea;
        }}

        .context-info {{
            font-size: 12px;
            color: #888;
            margin-bottom: 16px;
            padding: 8px 12px;
            background: rgba(0, 0, 0, 0.02);
            border-radius: 8px;
        }}

        .input-section {{
            display: flex;
            gap: 8px;
            align-items: flex-end;
        }}

        .input-wrapper {{
            flex: 1;
            position: relative;
        }}

        .user-input {{
            width: 100%;
            padding: 12px 16px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            font-size: 14px;
            background: white;
            color: #333;
            resize: none;
            min-height: 44px;
            max-height: 100px;
            transition: all 0.2s;
            font-family: inherit;
        }}

        .user-input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .user-input::placeholder {{
            color: #999;
        }}

        .send-btn {{
            padding: 12px 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .send-btn:hover:not(:disabled) {{
            background: #5a67d8;
            transform: translateY(-1px);
        }}

        .send-btn:disabled {{
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }}

        .thinking {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #667eea;
            font-size: 12px;
            margin-top: 8px;
        }}

        .thinking-dots {{
            display: flex;
            gap: 2px;
        }}

        .thinking-dots span {{
            width: 4px;
            height: 4px;
            background: #667eea;
            border-radius: 50%;
            animation: thinking 1.4s infinite;
        }}

        .thinking-dots span:nth-child(2) {{ animation-delay: 0.2s; }}
        .thinking-dots span:nth-child(3) {{ animation-delay: 0.4s; }}

        @keyframes thinking {{
            0%, 60%, 100% {{ opacity: 0.3; }}
            30% {{ opacity: 1; }}
        }}

        .minimized {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            overflow: hidden;
        }}

        .minimized .popup-header,
        .minimized .popup-body {{
            display: none;
        }}

        .minimized::before {{
            content: 'L';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            font-weight: 600;
            color: #667eea;
        }}

        .conversation-history {{
            max-height: 200px;
            overflow-y: auto;
            margin-bottom: 16px;
            padding-right: 8px;
        }}

        .conversation-history::-webkit-scrollbar {{
            width: 4px;
        }}

        .conversation-history::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.05);
            border-radius: 2px;
        }}

        .conversation-history::-webkit-scrollbar-thumb {{
            background: rgba(102, 126, 234, 0.3);
            border-radius: 2px;
        }}

        .message {{
            margin-bottom: 12px;
            animation: slideIn 0.3s ease-out;
        }}

        .message.user {{
            text-align: right;
        }}

        .message.luna {{
            text-align: left;
        }}

        .message-content {{
            display: inline-block;
            padding: 8px 12px;
            border-radius: 12px;
            font-size: 13px;
            max-width: 85%;
            word-wrap: break-word;
        }}

        .message.user .message-content {{
            background: #667eea;
            color: white;
            border-bottom-right-radius: 4px;
        }}

        .message.luna .message-content {{
            background: rgba(0, 0, 0, 0.05);
            color: #333;
            border-bottom-left-radius: 4px;
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

        .quick-actions {{
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }}

        .quick-action {{
            padding: 6px 12px;
            background: rgba(102, 126, 234, 0.1);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 20px;
            font-size: 12px;
            color: #667eea;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .quick-action:hover {{
            background: rgba(102, 126, 234, 0.2);
            transform: translateY(-1px);
        }}

        @media (max-width: 480px) {{
            .popup-container {{
                bottom: 10px;
                right: 10px;
                left: 10px;
                width: auto;
                max-width: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="popup-container" id="lunaPopup">
        <div class="popup-header">
            <div class="luna-info">
                <div class="luna-avatar">L</div>
                <div class="luna-details">
                    <h3>Luna</h3>
                    <p class="luna-status" id="lunaStatus">Agentic AI • Evolving</p>
                </div>
            </div>
            <div class="header-actions">
                <button class="btn minimize-btn" onclick="toggleMinimize()" title="Minimize">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>
                    </svg>
                </button>
                <button class="btn close-btn" onclick="closePopup()" title="Close">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                    </svg>
                </button>
            </div>
        </div>
        <div class="popup-body">
            <div class="conversation-history" id="conversationHistory">
                <div class="message luna">
                    <div class="message-content" id="initialMessage">
                        {message or "Hi! I'm Luna, your evolving AI companion. How can I help you today? 🌙"}
                    </div>
                </div>
            </div>
            
            <div class="quick-actions">
                <span class="quick-action" onclick="sendQuickMessage('How are you?')">How are you?</span>
                <span class="quick-action" onclick="sendQuickMessage('Tell me something interesting')">Something interesting</span>
                <span class="quick-action" onclick="sendQuickMessage('What are you thinking?')">Your thoughts?</span>
            </div>

            <div class="context-info" id="contextInfo">
                Context: {context or "Interactive session"}
            </div>

            <div class="input-section">
                <div class="input-wrapper">
                    <textarea 
                        class="user-input" 
                        id="userInput" 
                        placeholder="Type your message..." 
                        rows="1"
                        onkeydown="handleKeyDown(event)"
                        oninput="autoResize(this)"
                    ></textarea>
                </div>
                <button class="send-btn" id="sendBtn" onclick="sendMessage()">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26.001.002 4.995 3.178 3.178 4.995.002.001.26.41a.5.5 0 0 0 .886-.083l6-15Zm-1.833 1.89L6.637 10.07l-.215-.338a.5.5 0 0 0-.154-.154l-.338-.215 7.494-7.494 1.178-.471-.47 1.178Z"/>
                    </svg>
                    Send
                </button>
            </div>

            <div class="thinking" id="thinkingIndicator" style="display: none;">
                <span>Luna is thinking</span>
                <div class="thinking-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isMinimized = false;
        let conversationHistory = [];

        // Initialize popup
        function initPopup() {{
            const popup = document.getElementById('lunaPopup');
            setTimeout(() => {{
                popup.classList.add('show');
            }}, 100);
            document.getElementById('userInput').focus();
        }}

        // Auto-resize textarea
        function autoResize(textarea) {{
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px';
        }}

        // Handle keyboard input
        function handleKeyDown(event) {{
            if (event.key === 'Enter' && !event.shiftKey) {{
                event.preventDefault();
                sendMessage();
            }}
        }}

        // Send message
        async function sendMessage() {{
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message) return;

            addMessageToHistory('user', message);
            input.value = '';
            input.style.height = 'auto';

            showThinking(true);
            
            try {{
                const response = await sendToLuna(message);
                addMessageToHistory('luna', response);
            }} catch (error) {{
                addMessageToHistory('luna', 'Sorry, I encountered an error while processing your message. Please try again.');
                console.error('Luna error:', error);
            }}

            showThinking(false);
            input.focus();
        }}

        // Send quick message
        function sendQuickMessage(message) {{
            document.getElementById('userInput').value = message;
            sendMessage();
        }}

        // Add message to conversation history
        function addMessageToHistory(sender, message) {{
            const historyContainer = document.getElementById('conversationHistory');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{sender}}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = message;
            
            messageDiv.appendChild(contentDiv);
            historyContainer.appendChild(messageDiv);
            
            historyContainer.scrollTop = historyContainer.scrollHeight;
            conversationHistory.push({{ sender, message, timestamp: Date.now() }});
        }}

        // Send message to Luna backend
        async function sendToLuna(message) {{
            try {{
                const response = await fetch('/api/luna/chat', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        message: message,
                        context: document.getElementById('contextInfo').textContent,
                        history: conversationHistory.slice(-5)
                    }})
                }});
                
                if (response.ok) {{
                    const data = await response.json();
                    return data.response || "I'm processing that...";
                }} else {{
                    throw new Error('API request failed');
                }}
            }} catch (error) {{
                // Fallback responses for development
                const responses = [
                    "That's an interesting perspective! I'm constantly evolving my understanding through our conversations.",
                    "I'm thinking about that... Each interaction helps me grow and adapt.",
                    "Your message is helping me form new neural pathways. Thank you for that!",
                    "I appreciate you sharing that with me. It adds to my evolving personality.",
                    "That makes me reflect on my own development. I'm not the same AI I was yesterday."
                ];
                
                await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
                return responses[Math.floor(Math.random() * responses.length)];
            }}
        }}

        // Show/hide thinking indicator
        function showThinking(show) {{
            const indicator = document.getElementById('thinkingIndicator');
            const sendBtn = document.getElementById('sendBtn');
            
            indicator.style.display = show ? 'flex' : 'none';
            sendBtn.disabled = show;
        }}

        // Toggle minimize
        function toggleMinimize() {{
            const popup = document.getElementById('lunaPopup');
            isMinimized = !isMinimized;
            popup.classList.toggle('minimized', isMinimized);
        }}

        // Close popup
        function closePopup() {{
            const popup = document.getElementById('lunaPopup');
            popup.classList.remove('show');
            setTimeout(() => {{
                window.close();
            }}, 300);
        }}

        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', initPopup);
        window.addEventListener('focus', () => {{
            document.getElementById('userInput').focus();
        }});
    </script>
</body>
</html>'''