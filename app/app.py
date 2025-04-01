import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv(dotenv_path=".env", override=True)

# Set up logging
logging.basicConfig(filename='flask.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'sqlite:///instance/socialme.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    source_type = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
