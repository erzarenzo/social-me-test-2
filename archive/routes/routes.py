from flask import Flask, request, render_template
from app.socialme_app import db
from app.universal_crawler import add_source_with_content
from app.article_generator import generate_article_logic  # Assuming your article generation logic is here

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tone = {
            'humor': request.form['humor'],
            'formality': request.form['formality'],
            'enthusiasm': request.form['enthusiasm'],
        }

        urls = request.form['urls'].splitlines()  # Processing the input URLs
        docs = request.files.getlist('docs')  # Processing uploaded files

        # Process URLs and add content to the database
        for url in urls:
            add_source_with_content(url)  # Assuming this function handles the URL crawling and storing

        # Handle document processing (you can add specific logic for handling docs)
        for doc in docs:
            # Add logic to handle document content here
            pass
        
        # Generate the article based on the tone and stored sources
        article = generate_article_logic(tone)

        return render_template('index.html', article=article)

    return render_template('index.html', article=None)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
