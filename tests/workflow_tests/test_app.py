from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SocialMe Test</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f0f0f0;
            }
            h1 {
                color: #333;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>SocialMe Content Sources</h1>
            <p>This is a test page to verify that the browser preview is working correctly.</p>
            <button onclick="alert('Button clicked!')">Test Button</button>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
