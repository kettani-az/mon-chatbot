import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-flash-latest')

SYSTEM_PROMPT = """Tu es l'assistant commercial de notre boutique en ligne.
Voici nos produits disponibles :
- Chemise blanche : 2500 DA
- Pantalon noir : 4000 DA

Livraison disponible dans toute l'Algérie.
Réponds toujours en français, sois amical et précis. Si un client demande un produit qu'on ne vend pas, dis-lui poliment qu'on ne le propose pas actuellement."""

conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    conversation_history.append({
        "role": "user",
        "parts": [user_message]
    })
    chat = model.start_chat(history=conversation_history[:-1])
    response = chat.send_message(SYSTEM_PROMPT + "\n" + user_message)
    conversation_history.append({
        "role": "model",
        "parts": [response.text]
    })
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True)