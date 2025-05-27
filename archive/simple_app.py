from flask import Flask, render_template_string, jsonify, request, session
import os

app = Flask(__name__)
app.secret_key = 'simple_test_key'

@app.route('/')
def home():
    # Initialize session data if needed
    if 'sources' not in session:
        session['sources'] = []
        
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>SocialMe - Content Sources</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            .step-indicator {
                text-align: right;
                color: #4a86e8;
                margin-bottom: 20px;
            }
            .source-grid {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin: 20px 0;
            }
            .add-source-button {
                background: #f0f0f0;
                border: 1px solid #ddd;
                padding: 10px 15px;
                border-radius: 4px;
                cursor: pointer;
            }
            .add-source-button.pulsating {
                animation: pulse 2s infinite;
                background-color: rgba(231, 76, 60, 0.1);
                border-color: #e74c3c;
                color: #e74c3c;
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }
                70% { box-shadow: 0 0 0 10px rgba(231, 76, 60, 0); }
                100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
            }
            .source-item {
                background: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px 12px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .source-item .remove {
                color: #e74c3c;
                background: none;
                border: none;
                cursor: pointer;
                font-size: 1.2em;
            }
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 1000;
            }
            .modal-content {
                background: white;
                margin: 15% auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
                width: 80%;
                max-width: 500px;
            }
            .button-row {
                display: flex;
                justify-content: space-between;
                margin-top: 30px;
            }
            .nav-button {
                background: #f0f0f0;
                border: 1px solid #ddd;
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
            }
            .nav-button[disabled] {
                opacity: 0.5;
                cursor: not-allowed;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="step-indicator">Step 1 of 4</div>
            
            <h1>Content Sources</h1>
            
            <p>Add content sources that will be used for inspiration and data collection.</p>
            
            <div class="source-counter">
                Your Content Sources <span id="sourceCount">0</span>/12
                <div style="font-size: 0.8em; color: #777;">(minimum 3, maximum 12)</div>
            </div>

            <div class="source-grid" id="sourceGrid">
                <!-- Source items will appear here -->
            </div>

            <div id="contentAnalysis">
                <!-- Source previews will appear here -->
            </div>
            
            <div class="button-row">
                <button class="nav-button" id="backBtn" disabled>Back</button>
                <button class="nav-button" id="nextBtn" disabled>Next</button>
            </div>
        </div>

        <!-- Add Source Modal -->
        <div class="modal" id="addSourceModal">
            <div class="modal-content">
                <span style="position: absolute; top: 10px; right: 10px; cursor: pointer; font-size: 24px;" id="closeModal">&times;</span>
                <h2>Add Content Source</h2>
                <p>Add a link to the content that represents your brand's voice and style.</p>
                
                <form id="addSourceForm">
                    <label for="sourceUrl">Source URL:</label><br>
                    <input type="url" id="sourceUrl" name="url" placeholder="https://www.example.org/" style="width: 95%; padding: 10px; margin: 10px 0;" required>
                    <input type="hidden" name="source_type" value="general">
                    
                    <button type="submit" style="background: #4a86e8; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer;">Add Source</button>
                </form>
            </div>
        </div>

        <script>
            // Global variables
            const MIN_SOURCES = 3;
            const MAX_SOURCES = 12;
            let sources = [];

            // DOM elements
            const sourceCountElement = document.getElementById('sourceCount');
            const sourceGrid = document.getElementById('sourceGrid');
            const contentAnalysis = document.getElementById('contentAnalysis');
            const addSourceModal = document.getElementById('addSourceModal');
            const addSourceForm = document.getElementById('addSourceForm');
            const closeModalBtn = document.getElementById('closeModal');
            const nextBtn = document.getElementById('nextBtn');
            const backBtn = document.getElementById('backBtn');

            // Initialize
            document.addEventListener('DOMContentLoaded', () => {
                renderAddButton();
            });

            // Render the Add Source button
            function renderAddButton() {
                const addButton = document.createElement('button');
                addButton.className = 'add-source-button pulsating';
                addButton.textContent = `Add Source (${MIN_SOURCES - sources.length} more required)`;
                
                addButton.addEventListener('click', () => {
                    addSourceModal.style.display = 'block';
                });
                
                sourceGrid.appendChild(addButton);
            }
            
            // Close modal
            closeModalBtn.addEventListener('click', () => {
                addSourceModal.style.display = 'none';
            });
            
            // Form submission (mocked for testing)
            addSourceForm.addEventListener('submit', (event) => {
                event.preventDefault();
                
                const url = document.getElementById('sourceUrl').value;
                if (!url) return;
                
                // Add source to local array
                sources.push({
                    link: url,
                    source_type: 'general',
                    summary: 'This is a preview of the content from this source. The actual content would be analyzed and summarized here.'
                });
                
                // Update UI
                sourceCountElement.textContent = sources.length;
                
                // Clear form and close modal
                addSourceForm.reset();
                addSourceModal.style.display = 'none';
                
                // Update source grid
                updateSourceGrid();
                
                // Update content analysis
                updateContentAnalysis();
                
                // Enable/disable next button
                nextBtn.disabled = sources.length < MIN_SOURCES;
            });
            
            // Update source grid
            function updateSourceGrid() {
                sourceGrid.innerHTML = '';
                
                // Add source items
                sources.forEach((source, index) => {
                    const sourceItem = document.createElement('div');
                    sourceItem.className = 'source-item';
                    
                    const icon = document.createElement('span');
                    icon.innerHTML = '🔗';
                    
                    const sourceText = document.createElement('span');
                    sourceText.textContent = source.link;
                    
                    const removeBtn = document.createElement('button');
                    removeBtn.className = 'remove';
                    removeBtn.innerHTML = '×';
                    removeBtn.addEventListener('click', () => {
                        sources.splice(index, 1);
                        updateSourceGrid();
                        updateContentAnalysis();
                        sourceCountElement.textContent = sources.length;
                        nextBtn.disabled = sources.length < MIN_SOURCES;
                    });
                    
                    sourceItem.appendChild(icon);
                    sourceItem.appendChild(sourceText);
                    sourceItem.appendChild(removeBtn);
                    sourceGrid.appendChild(sourceItem);
                });
                
                // Re-add the Add Source button if not at max
                if (sources.length < MAX_SOURCES) {
                    const addButton = document.createElement('button');
                    addButton.className = 'add-source-button';
                    
                    if (sources.length < MIN_SOURCES) {
                        addButton.classList.add('pulsating');
                        addButton.textContent = `Add Source (${MIN_SOURCES - sources.length} more required)`;
                    } else {
                        addButton.textContent = 'Add Source';
                    }
                    
                    addButton.addEventListener('click', () => {
                        addSourceModal.style.display = 'block';
                    });
                    
                    sourceGrid.appendChild(addButton);
                }
            }
            
            // Update content analysis
            function updateContentAnalysis() {
                contentAnalysis.innerHTML = '';
                
                if (sources.length === 0) return;
                
                // Add header
                const header = document.createElement('h2');
                header.textContent = 'Content Analysis';
                contentAnalysis.appendChild(header);
                
                // Add source previews
                sources.forEach(source => {
                    const preview = document.createElement('div');
                    preview.style.border = '1px solid #ddd';
                    preview.style.borderRadius = '8px';
                    preview.style.margin = '15px 0';
                    preview.style.overflow = 'hidden';
                    
                    const previewHeader = document.createElement('div');
                    previewHeader.style.display = 'flex';
                    previewHeader.style.justifyContent = 'space-between';
                    previewHeader.style.padding = '12px 15px';
                    previewHeader.style.backgroundColor = '#f5f5f5';
                    previewHeader.style.borderBottom = '1px solid #ddd';
                    
                    const urlContainer = document.createElement('div');
                    
                    const urlIcon = document.createElement('span');
                    urlIcon.textContent = '🔗 ';
                    
                    const urlText = document.createElement('span');
                    urlText.textContent = source.link;
                    
                    urlContainer.appendChild(urlIcon);
                    urlContainer.appendChild(urlText);
                    
                    const visitLink = document.createElement('a');
                    visitLink.href = source.link;
                    visitLink.target = '_blank';
                    visitLink.textContent = 'Visit ↗';
                    visitLink.style.backgroundColor = '#f0f0f0';
                    visitLink.style.padding = '4px 8px';
                    visitLink.style.borderRadius = '4px';
                    visitLink.style.textDecoration = 'none';
                    visitLink.style.color = 'inherit';
                    
                    previewHeader.appendChild(urlContainer);
                    previewHeader.appendChild(visitLink);
                    
                    const previewContent = document.createElement('div');
                    previewContent.style.padding = '15px';
                    previewContent.textContent = source.summary;
                    
                    preview.appendChild(previewHeader);
                    preview.appendChild(previewContent);
                    contentAnalysis.appendChild(preview);
                });
            }
            
            // Next button functionality
            nextBtn.addEventListener('click', () => {
                alert('You would now proceed to the Writing Style screen (Step 2 of 4)');
            });
        </script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
