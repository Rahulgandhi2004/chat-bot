from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chatbot</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
            .container { width: 100%; max-width: 600px; margin: 0 auto; padding: 20px; }
            textarea { width: 100%; height: 100px; padding: 10px; margin-bottom: 10px; }
            button { padding: 10px 20px; }
            .chat-box { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: scroll; margin-bottom: 10px; }
            .chat-message { margin-bottom: 10px; }
            .user-message { font-weight: bold; }
            .bot-response { margin-left: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Chat with AI</h1>
            <div class="chat-box" id="chat-box"></div>
            <textarea id="message" placeholder="Type your message..."></textarea>
            <button onclick="sendMessage()">Send</button>
        </div>
        <script>
            async function sendMessage() {
                const message = document.getElementById('message').value;
                if (!message) return;
                
                const chatBox = document.getElementById('chat-box');
                chatBox.innerHTML += `<div class="chat-message user-message">You: ${message}</div>`;
                
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message })
                });
                
                const data = await response.json();
                chatBox.innerHTML += `<div class="chat-message bot-response">Bot: ${data.response}</div>`;
                document.getElementById('message').value = '';
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    bot_response = generate_response(user_message)
    return jsonify({"response": bot_response})

def generate_response(message):
    # Simple rule-based response for demonstration
    responses = {
        "what is my name":"your name is prem Rajesh",
        "hi": "Hello! How can I help you today?",
        "hello": "Hi there! What can I do for you?",
        "bye": "Goodbye! Have a great day!",
        "thanks": "You're welcome!"
    }
    return responses.get(message.lower(), "I didn't understand that. Can you please rephrase?")

if __name__ == '__main__':
    app.run(debug=True)
