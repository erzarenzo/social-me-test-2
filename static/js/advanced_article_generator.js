/**
 * Advanced Article Generator JavaScript
 * Handles client-side functionality for the advanced article generator
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const sources = [];
    const sourceCounter = document.getElementById('sourceCounter');
    const selectedSources = document.getElementById('selectedSources');
    const addSourceButton = document.getElementById('addSourceButton');
    const generateButton = document.getElementById('generateButton');
    const progressSection = document.getElementById('progressSection');
    const resultSection = document.getElementById('resultSection');
    const progressBar = document.querySelector('#generationProgress .progress-bar');
    const progressStatus = document.getElementById('progressStatus');
    const articleGeneratorForm = document.getElementById('articleGeneratorForm');
    
    // Sample style profile (in a real implementation, this would come from the previous step)
    const sampleStyleProfile = {
        voice_profile: {
            formality: 0.8,
            technical_level: 0.7,
            persuasiveness: 0.6,
            emotional_tone: "neutral",
            engagement_style: "informative"
        },
        linguistic_patterns: {
            sentence_length: "medium",
            vocabulary_complexity: "high",
            transition_phrases: ["furthermore", "however", "in addition"],
            rhetorical_devices: ["analogy", "rhetorical question"]
        },
        content_structure: {
            intro_style: "question-based",
            paragraph_structure: "claim-evidence-explanation",
            conclusion_style: "summary with call to action"
        }
    };
    
    // Display style profile
    displayStyleProfile(sampleStyleProfile);
    
    // Add source button click handler
    if (addSourceButton) {
        addSourceButton.addEventListener('click', function() {
            const sourceType = document.getElementById('sourceType').value;
            const sourceUrl = document.getElementById('sourceUrl').value;
            
            if (!sourceUrl) {
                alert('Please enter a valid URL');
                return;
            }
            
            // Add to sources array
            sources.push({
                type: sourceType,
                url: sourceUrl,
                title: `Source from ${sourceUrl}`,
                content: "Content will be crawled from this source",
                date: new Date().toISOString().split('T')[0]
            });
            
            // Update counter
            sourceCounter.textContent = sources.length;
            
            // Create source card
            const sourceCard = document.createElement('div');
            sourceCard.className = 'source-card';
            sourceCard.innerHTML = `
                <div class="d-flex justify-content-between">
                    <div>
                        <strong>${getSourceTypeName(sourceType)}</strong>
                        <p class="mb-0">${sourceUrl}</p>
                    </div>
                    <div class="remove-btn" data-url="${sourceUrl}">
                        <i class="fas fa-times"></i>
                    </div>
                </div>
            `;
            
            // Add remove button handler
            const removeBtn = sourceCard.querySelector('.remove-btn');
            removeBtn.addEventListener('click', function() {
                const url = this.getAttribute('data-url');
                const index = sources.findIndex(source => source.url === url);
                if (index !== -1) {
                    sources.splice(index, 1);
                    sourceCounter.textContent = sources.length;
                    sourceCard.remove();
                }
            });
            
            // Add to DOM
            selectedSources.appendChild(sourceCard);
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('addSourceModal'));
            modal.hide();
            
            // Clear form
            document.getElementById('sourceUrl').value = '';
        });
    }
    
    // Form submit handler
    if (articleGeneratorForm) {
        articleGeneratorForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (sources.length < 3) {
                alert('Please add at least 3 sources');
                return;
            }
            
            const topic = document.getElementById('articleTopic').value;
            if (!topic) {
                alert('Please enter an article topic');
                return;
            }
            
            // Show progress section
            progressSection.classList.remove('hidden');
            
            // Start progress animation
            startProgressAnimation();
            
            // Prepare request data
            const requestData = {
                topic: topic,
                style_profile: sampleStyleProfile,
                source_material: sources
            };
            
            // Make API call
            generateArticle(requestData);
        });
    }
    
    // Helper function to get source type name
    function getSourceTypeName(type) {
        const typeMap = {
            'linkedin': 'LinkedIn Profile',
            'twitter': 'Twitter/X Account',
            'blog': 'Blog Article',
            'rss': 'RSS Feed',
            'news': 'News Source',
            'newsletter': 'Newsletter'
        };
        return typeMap[type] || type;
    }
    
    // Display style profile
    function displayStyleProfile(profile) {
        const styleProfileElement = document.getElementById('styleProfile');
        if (!styleProfileElement) return;
        
        let html = '<div class="row">';
        
        // Voice Profile
        html += '<div class="col-md-6 mb-3">';
        html += '<h6>Voice Character Profile</h6>';
        html += '<ul class="list-unstyled">';
        html += `<li>Formality: ${Math.round(profile.voice_profile.formality * 100)}%</li>`;
        html += `<li>Technical Level: ${Math.round(profile.voice_profile.technical_level * 100)}%</li>`;
        html += `<li>Persuasiveness: ${Math.round(profile.voice_profile.persuasiveness * 100)}%</li>`;
        html += `<li>Emotional Tone: ${profile.voice_profile.emotional_tone}</li>`;
        html += `<li>Engagement Style: ${profile.voice_profile.engagement_style}</li>`;
        html += '</ul>';
        html += '</div>';
        
        // Linguistic Patterns
        html += '<div class="col-md-6 mb-3">';
        html += '<h6>Linguistic Patterns</h6>';
        html += '<ul class="list-unstyled">';
        html += `<li>Sentence Length: ${profile.linguistic_patterns.sentence_length}</li>`;
        html += `<li>Vocabulary Complexity: ${profile.linguistic_patterns.vocabulary_complexity}</li>`;
        html += '</ul>';
        html += '</div>';
        
        html += '</div>';
        
        styleProfileElement.innerHTML = html;
    }
    
    // Start progress animation
    function startProgressAnimation() {
        let progress = 0;
        const interval = setInterval(() => {
            progress += 2;
            progressBar.style.width = `${progress}%`;
            
            if (progress <= 20) {
                progressStatus.textContent = 'Analyzing sources...';
            } else if (progress <= 40) {
                progressStatus.textContent = 'Generating article outline...';
            } else if (progress <= 60) {
                progressStatus.textContent = 'Creating article sections...';
            } else if (progress <= 80) {
                progressStatus.textContent = 'Refining content...';
            } else {
                progressStatus.textContent = 'Finalizing article...';
            }
            
            if (progress >= 98) {
                clearInterval(interval);
                progressBar.style.width = '98%';
            }
        }, 200);
        
        return interval;
    }
    
    // Generate article API call
    function generateArticle(requestData) {
        fetch('/api/generate-article', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Complete progress bar
            progressBar.style.width = '100%';
            progressStatus.textContent = 'Article generated successfully!';
            
            // Hide progress section after a short delay
            setTimeout(() => {
                progressSection.classList.add('hidden');
                displayGeneratedArticle(data);
            }, 500);
        })
        .catch(error => {
            console.error('Error generating article:', error);
            progressStatus.textContent = 'Error generating article. Please try again.';
            progressBar.classList.remove('bg-primary');
            progressBar.classList.add('bg-danger');
            
            // Show error message
            alert('Error generating article: ' + error.message);
        });
    }
    
    // Display generated article
    function displayGeneratedArticle(data) {
        const article = data.article || data;
        
        // Set title and subtitle
        document.getElementById('articleTitle').textContent = article.title;
        document.getElementById('articleSubtitle').textContent = article.subtitle || '';
        
        // Build article content
        const articleContent = document.getElementById('articleContent');
        let html = '';
        
        // Introduction
        if (article.introduction) {
            html += `<div class="mb-4">
                <h4>Introduction</h4>
                <p>${article.introduction}</p>
            </div>`;
        }
        
        // Overview
        if (article.overview) {
            html += `<div class="mb-4">
                <h4>Overview</h4>
                <p>${article.overview}</p>
            </div>`;
        }
        
        // Body sections
        if (article.body && Array.isArray(article.body)) {
            article.body.forEach(section => {
                html += `<div class="mb-4">
                    <h4>${section.heading}</h4>
                    <p>${section.content}</p>
                </div>`;
            });
        }
        
        // Conclusion
        if (article.conclusion) {
            html += `<div class="mb-4">
                <h4>Conclusion</h4>
                <p>${article.conclusion}</p>
            </div>`;
        }
        
        // Sources
        if (article.sources && Array.isArray(article.sources)) {
            html += `<div class="mb-4">
                <h4>Sources</h4>
                <ul>`;
            
            article.sources.forEach(source => {
                html += `<li><a href="${source.url}" target="_blank">${source.name}</a></li>`;
            });
            
            html += `</ul>
            </div>`;
        }
        
        // Set content
        articleContent.innerHTML = html;
        
        // Show result section
        resultSection.classList.remove('hidden');
    }
    
    // Regenerate button handler
    const regenerateButton = document.getElementById('regenerateButton');
    if (regenerateButton) {
        regenerateButton.addEventListener('click', function() {
            resultSection.classList.add('hidden');
            progressSection.classList.remove('hidden');
            
            const topic = document.getElementById('articleTopic').value;
            
            // Start progress animation
            startProgressAnimation();
            
            // Prepare request data
            const requestData = {
                topic: topic,
                style_profile: sampleStyleProfile,
                source_material: sources
            };
            
            // Make API call
            generateArticle(requestData);
        });
    }

    // Back button handler
    const backButton = document.getElementById('backButton');
    if (backButton) {
        backButton.addEventListener('click', function() {
            resultSection.classList.add('hidden');
            document.getElementById('formSection').classList.remove('hidden');
        });
    }

    // Preview button handler
    const previewButton = document.getElementById('previewButton');
    if (previewButton) {
        previewButton.addEventListener('click', function() {
            // Store the generated article in sessionStorage for retrieval in the preview page
            try {
                const articleTitle = document.getElementById('articleTitle').textContent;
                const articleSubtitle = document.getElementById('articleSubtitle').textContent;
                const articleContent = document.getElementById('articleContent').innerHTML;
                
                const articleData = {
                    title: articleTitle,
                    subtitle: articleSubtitle,
                    content: articleContent,
                    timestamp: new Date().toISOString()
                };
                
                sessionStorage.setItem('generatedArticle', JSON.stringify(articleData));
                console.log('Article data saved to session storage');
            } catch (e) {
                console.error('Error saving article data:', e);
            }
            
            // Navigate to the preview page
            window.location.href = '/onboarding/article-preview';
        });
    }
});
