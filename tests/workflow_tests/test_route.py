from flask import Flask

app = Flask(__name__)

@app.route('/test')
def test():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SocialMe Test Page</title>
    </head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>SocialMe Test Page</h1>
        <p>If you can see this, the browser preview is working!</p>
        <button onclick="alert('JavaScript is working!')">Click Me</button>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003, debug=True)
