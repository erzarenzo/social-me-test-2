import os
import sys
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("workflow_test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("socialme_workflow")

# Workflow State Management
class WorkflowState:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all workflow state"""
        self.data_sources = []
        self.writing_style = None
        self.content_strategy = None
        self.article_details = None
        self.current_step = 0

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize workflow state
workflow = WorkflowState()

@app.route('/')
def index():
    """Landing page"""
    return render_template('landing.html')

@app.route('/onboarding')
def onboarding_start():
    """Start onboarding workflow"""
    workflow.reset()
    return render_template('socialme_onboarding.html')

@app.route('/onboarding/step1', methods=['GET', 'POST'])
def onboarding_step1():
    """Step 1: Data Sources"""
    if request.method == 'POST':
        sources = request.json.get('sources', [])
        workflow.data_sources = sources
        workflow.current_step = 1
        return jsonify({
            "success": True, 
            "next_step": "/onboarding/step2",
            "sources": sources
        })
    return render_template('onboarding/step1_data_sources.html')

@app.route('/onboarding/step2', methods=['GET', 'POST'])
def onboarding_step2():
    """Step 2: Writing Style"""
    if request.method == 'POST':
        writing_style = request.json
        workflow.writing_style = writing_style
        workflow.current_step = 2
        return jsonify({
            "success": True, 
            "next_step": "/onboarding/step3",
            "writing_style": writing_style
        })
    return render_template('onboarding/step2_writing_style.html')

@app.route('/onboarding/step3', methods=['GET', 'POST'])
def onboarding_step3():
    """Step 3: Content Strategy"""
    if request.method == 'POST':
        content_strategy = request.json
        workflow.content_strategy = content_strategy
        workflow.current_step = 3
        return jsonify({
            "success": True, 
            "next_step": "/onboarding/step4",
            "content_strategy": content_strategy
        })
    return render_template('onboarding/step3_content_strategy.html')

@app.route('/onboarding/step4', methods=['GET', 'POST'])
def onboarding_step4():
    """Step 4: Article Generation"""
    if request.method == 'POST':
        article_details = request.json
        workflow.article_details = article_details
        workflow.current_step = 4
        
        # Placeholder for article generation logic
        generated_article = {
            "title": article_details.get('title', 'Generated Article'),
            "content": "Article generation placeholder",
            "sources": workflow.data_sources,
            "writing_style": workflow.writing_style,
            "content_strategy": workflow.content_strategy
        }
        
        return jsonify({
            "success": True, 
            "article": generated_article,
            "redirect": "/results"
        })
    return render_template('onboarding/step4_article_generation.html')

@app.route('/results')
def show_results():
    """Display generated article results"""
    if workflow.current_step < 4:
        return redirect(url_for('onboarding_start'))
    
    return render_template('results.html', 
                           article=workflow.article_details, 
                           workflow_data=workflow)

@app.route('/workflow/reset')
def reset_workflow():
    """Reset the entire workflow"""
    workflow.reset()
    return redirect(url_for('onboarding_start'))

if __name__ == '__main__':
    app.run(debug=True, port=8003)
