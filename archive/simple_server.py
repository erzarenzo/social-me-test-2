from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

# Change to the directory containing our HTML files
os.chdir('/root/socialme/social-me-test-2')

# Set up a simple HTTP server
handler = SimpleHTTPRequestHandler
httpd = HTTPServer(('0.0.0.0', 8090), handler)
print("Server started at http://localhost:8090")
print("This server will redirect to the SocialMe application on port 8003")
print("Available files:")
for file in os.listdir('.'):
    if file.endswith('.html'):
        print(f" - {file}")
httpd.serve_forever()
