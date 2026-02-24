import os
from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    </head>
    <body style="background: linear-gradient(135deg, #1a1a2e, #0f3460); font-family: 'Inter', sans-serif; display: flex; justify-content: center; padding: 40px 20px; margin: 0; min-height: 100vh;">
        <div class="container" style="background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px); padding: 40px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); max-width: 800px; width: 100%;">
            
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="background: linear-gradient(to right, #007bff, #00d1b2); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; margin: 0; font-size: 2.2rem; font-weight: 700; letter-spacing: 1.5px;">PRYMAGE</h1>
                <h2 style="color: #ffffff; margin-top: 5px; font-weight: 600; font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase;">Generated Strategy for {client_name}</h2>
            </div>
            
            <div id="pitch-text" style="white-space: pre-wrap; background: rgba(0, 0, 0, 0.2); padding: 35px; border-radius: 8px; border-left: 4px solid #1abc9c; line-height: 1.8; color: #e0e0e0; font-size: 1.05rem; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);">{output_text}</div>
            <br>
            
            <div style="display: flex; gap: 15px; margin-top: 20px;">
                <button onclick="copyPitch()" id="copy-btn" style="flex: 2; padding: 16px; cursor: pointer; background: linear-gradient(to bottom, #3498db, #2980b9); color: white; border: 1px solid #2980b9; border-radius: 8px; font-weight: 700; font-size: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.2); transition: all 0.3s;">Copy to Clipboard</button>
                <a href="/" style="flex: 1; text-decoration: none;">
                    <button style="width: 100%; height: 100%; padding: 16px; cursor: pointer; background: transparent; color: #00d1b2; border: 2px solid #00d1b2; border-radius: 8px; font-weight: 700; font-size: 1rem; transition: all 0.3s;">Back</button>
                </a>
            </div>
            
            <script>
                function copyPitch() {{
                    const textToCopy = document.getElementById("pitch-text").innerText;
                    navigator.clipboard.writeText(textToCopy).then(() => {{
                        const btn = document.getElementById("copy-btn");
                        btn.innerText = "COPIED!";
                        btn.style.background = "linear-gradient(to bottom, #1abc9c, #16a085)";
                        btn.style.borderColor = "#16a085";
                        setTimeout(() => {{
                            btn.innerText = "Copy to Clipboard";
                            btn.style.background = "linear-gradient(to bottom, #3498db, #2980b9)";
                            btn.style.borderColor = "#2980b9";
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