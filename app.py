import os
from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv

# 1. Open the vault
load_dotenv()

app = Flask(__name__)

# 2. Grab the hidden key securely
secure_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=secure_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_pitch():
    client_name = request.form.get('client', 'Client')
    industry = request.form.get('industry', 'Enterprise')
    problem = request.form.get('problem', 'Operational Efficiency')
    software = request.form.get('software', 'Software Solutions')
    pitch_tone = request.form.get('tone', 'Professional') 
    
    my_name = "Leslie"
    my_phone = "055 123 4567" 
    my_email = "leslie@prymage.com" 
    
    prompt = f"""
    You are {my_name}, a senior enterprise software consultant at Prymage Consultancy Ltd. 
    Write a persuasive pitch proposal for a prospective client.
    
    Client Name: {client_name}
    Industry: {industry}
    Main Problem: {problem}
    Proposed Software Solution: {software}
    
    Strict Writing Rules:
    1. TONE: The writing must be exactly this: {pitch_tone}.
    2. NO MARKDOWN FORMATTING. Output plain text with standard paragraph breaks.
    3. Write like a clear-thinking human speaking to another smart human. 
    4. Sign off the email exactly like this:
       {my_name}
       Senior Enterprise Software Consultant
       Prymage Consultancy Ltd.
       {my_phone}
       {my_email}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        output_text = response.text
    except Exception as e:
        output_text = f"AI ERROR: {str(e)}"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container" style="max-width: 800px;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #3498db; margin: 0; font-size: 1.2rem;">PRYMAGE</h1>
            </div>
            <h2>Generated Strategy for {client_name}</h2>
            <div id="pitch-text" style="white-space: pre-wrap; background: #f8f9fa; padding: 30px; border-radius: 12px; border: 1px solid #e1e8ed; line-height: 1.8; color: #2c3e50;">{output_text}</div>
            <br>
            <div style="display: flex; gap: 15px;">
                <button onclick="copyPitch()" id="copy-btn" style="flex: 2; padding: 15px; cursor: pointer; background: #2ecc71; color: white; border: none; border-radius: 10px; font-weight: 700; font-size: 1rem;">Copy to Clipboard</button>
                <a href="/" style="flex: 1; text-decoration: none;">
                    <button style="width: 100%; padding: 15px; cursor: pointer; background: #3498db; color: white; border: none; border-radius: 10px; font-weight: 700;">Back</button>
                </a>
            </div>
            
            <script>
                function copyPitch() {{
                    const textToCopy = document.getElementById("pitch-text").innerText;
                    navigator.clipboard.writeText(textToCopy).then(() => {{
                        const btn = document.getElementById("copy-btn");
                        btn.innerText = "COPIED!";
                        btn.style.background = "#1abc9c";
                        setTimeout(() => {{
                            btn.innerText = "Copy to Clipboard";
                            btn.style.background = "#2ecc71";
                        }}, 2000);
                    }});
                }}
            </script>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)