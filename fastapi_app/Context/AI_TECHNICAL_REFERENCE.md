# AI-OPTIMIZED TECHNICAL REFERENCE

## DEVELOPMENT_BEST_PRACTICES
```best_practices
# Git Workflow
Branch_Strategy:
  - main: Stable production code
  - dev-improved-article-generation: Main development branch
  - feature-*: Feature-specific branches

Commit_Guidelines:
  - Commit small, logical changes
  - Use descriptive commit messages
  - Verify changes work before committing
  - Update documentation with code changes

# Project Organization
File_Structure:
  - /fastapi_app/Context/: Central documentation location
  - /static/archive/: Legacy HTML files
  - /archive/: Deprecated project files (prefer archiving over deletion)

Server_Management:
  - Always use start_workflow_server.sh to manage the server
  - Check server status: ps aux | grep uvicorn
  - Kill processes on port: fuser -k 8001/tcp
  - Server logs: /tmp/workflow_server.log

# Testing Protocol
Before_Deployment:
  - Backup current state
  - Update CHANGELOG.md
  - Test all workflow steps end-to-end
  - Verify API endpoints with curl
  - Check console for JavaScript errors (F12)
```

## STATIC_FILE_CONFIGURATION
```static_files
Primary_Static_Dir: /root/socialme/social-me-test-2/fastapi_app/static/
Project_Root_Static: /root/socialme/social-me-test-2/static/
Access_URL_Pattern: http://localhost:8001/static/{filename}

API_Configuration:
  - Base_URL: http://localhost:8001/api
  - Health_URL: http://localhost:8001/api/workflow/health
  - Diagnostics_URL: http://localhost:8001/api/workflow/diagnostics
  - NOTE: Although FastAPI reports root_path="/dev", API endpoints use direct /api/... paths

Workflow_UI_Access:
  - Direct_API_Endpoint: http://localhost:8001/workflow-ui (RECOMMENDED)
  - Redirect_HTML: /static/workflow.html
  - Legacy_HTML_Files: Archived in /static/archive/

Common_Issues:
  - Wrong server running (use start_workflow_server.sh)
  - File in wrong static directory (HTML files must be in fastapi_app/static/)
  - Inconsistent API URL configuration in HTML files
  - "Pretty Print, Not Found" error indicates incorrect API URL
  - Server process checks: ps aux | grep uvicorn
  - Port conflicts: fuser 8001/tcp
```

## SYSTEM_ARCHITECTURE
```architecture
Project: SocialMe Article Generator
Root: /root/socialme/social-me-test-2/
Primary_API_Framework: FastAPI
Secondary_Framework: Flask (legacy components)
Database: File-based JSON storage (no SQL)
External_Dependencies: 
  - OpenAI API (GPT-4 for tone analysis and article generation)
  - tls-client (for enhanced web crawling)
Virtual_Environments:
  - /fastapi_app/venv/ (primary)
  - /myenv/ (legacy)
  - /venv/ (project root, legacy)
```

## DEPLOYMENT_CONFIGURATION
```deployment
Port: 8001 (CRITICAL - always use this port)
Host: 0.0.0.0 (bind to all interfaces)
Standard_Run_Command: cd /root/socialme/social-me-test-2/fastapi_app && uvicorn simple_app:app --host 0.0.0.0 --port 8001
Production_Run_Command: cd /root/socialme/social-me-test-2/fastapi_app && nohup uvicorn simple_app:app --host 0.0.0.0 --port 8001 > /tmp/uvicorn.log 2>&1 &
Process_Management:
  - Check_Running: lsof -i :8001
  - Kill_Process: fuser -k 8001/tcp
  - View_Logs: tail -f /tmp/uvicorn.log
```

## CORE_COMPONENT_RELATIONSHIPS
```components
1. simple_app.py (Main FastAPI application)
   ↓
2. workflow_api.py (Article generation workflow API)
   ↓
3. enhanced_article_generator.py (Advanced article generation)
   ↓
4. quantum_crawler.py (Web content extraction)
   ↓
5. tone_adaptation/ (Tone analysis components)
   ├── __init__.py (Core initialization)
   ├── openai_tone_analyzer.py (OpenAI-based tone analysis)
   ├── hybrid_tone_adapter.py (Combines OpenAI and local analyzers)
   └── local_tone_analyzer.py (Legacy non-API analyzer)
```

## VIRTUAL_ENVIRONMENT_HANDLING
```virtual_env
Check_Active_Env: echo $VIRTUAL_ENV
Should_Show: /root/socialme/social-me-test-2/fastapi_app/venv

Activate_Primary_Env: source /root/socialme/social-me-test-2/fastapi_app/venv/bin/activate
Deactivate_Env: deactivate

Env_Dependencies_File: /root/socialme/social-me-test-2/requirements.txt
Install_Dependencies: pip install -r requirements.txt
```

## API_KEY_MANAGEMENT
```api_keys
OpenAI_Key_Location: /root/socialme/social-me-test-2/config/api_keys.json
Update_Key_Script: /root/socialme/social-me-test-2/update_api_key.sh
Validate_Key: python /root/socialme/social-me-test-2/check-openai-key.py
```

## WORKFLOW_SEQUENCE
```sequence
1. Topic_Selection (User input)
   - Primary topic + optional secondary topics
   - Auto-generated title based on topic

2. URL_Submission (Data sources)
   - Enhanced quantum crawler with 18,000+ word capacity
   - Multiple URLs with depth configuration

### 3. Tone Analysis System

#### Universal Voice Pattern Extraction System (May 2025)

The tone analysis system has been upgraded to provide comprehensive, style-agnostic voice profiling that can analyze any writing style without bias. The system supports multiple input methods:

1. **Direct text input**: Submit sample writing for analysis
2. **URL analysis**: Extract and analyze tone from web content using QuantumUniversalCrawler
3. **Document upload**: Process and analyze documents

The system now implements the "Universal Voice Pattern Extraction" framework with ten comprehensive analysis categories designed to reverse-engineer complete style guides from any content:

#### 1. Persona & Positioning
- Core Identity: Determines the implicit persona behind the writing
- Professional Positioning: Identifies implied expertise and relationship to the topic
- Key Writing Characteristics: Lists 5-7 defining characteristics of the writing style
- Distinctive Elements: Notes unusual or signature elements that set the writing apart

#### 2. Voice & Tone Specifications
- Core Voice Attributes: Lists paired attributes (e.g., "authoritative but accessible")
- Dominant Tone: Identifies the prevailing emotional tone
- Credibility Establishment: How the writer establishes expertise/authority
- Reader Relationship: How the writer relates to and addresses the audience
- Personality Elements: Distinctive personality markers in the writing

#### 3. Linguistic Patterns
- Sentence Structure: Typical patterns, length variety, and complexity
- Paragraph Construction: Typical length, structure, and transition patterns
- Question Usage: How and when questions are employed
- Voice: Active vs. passive voice preferences and patterns
- Pronoun Usage: Patterns in first/second/third person usage
- Contrast Elements: How opposing ideas or solutions are presented
- Specificity Level: Detail level in examples, data, and concepts

#### 4. Tonal Elements
- Directness Level: How straightforwardly ideas are presented
- Statement Strength: Bold claims vs. hedged statements
- Formality Spectrum: Formal to casual language patterns
- Perspective Framing: How insights and opinions are presented
- Opening Approaches: Typical ways sections or ideas are introduced
- Metaphor Usage: Types and frequency of analogies or metaphors
- Memorable Phrasing: Patterns in creating standout statements

#### 5. Content Structure
- Overall Framework: The typical organizational pattern of the content
- Section Organization: How individual components are structured
- Information Hierarchy: How primary and supporting points are arranged
- Evidence Integration: How facts, data, and support are incorporated
- Problem-Solution Patterns: How issues and resolutions are presented
- Conclusion Approaches: How points and sections are typically closed

#### 6. Formatting Conventions
- Header Usage: Style and frequency of section breaks and titles
- List Presentations: How and when lists are employed
- Emphasis Techniques: Methods used for highlighting key points
- White Space Utilization: Paragraph breaks and visual spacing patterns
- Special Formatting: Any unique formatting elements

#### 7. Signature Linguistic Devices
- Opening Styles: Specific opening patterns with examples
- Transition Phrases: Characteristic ways of moving between ideas
- Explanatory Patterns: How complex ideas are typically explained
- Data Presentation: How numbers, statistics and evidence are shown
- Example Formats: How examples and illustrations are structured
- Conclusion Styles: Characteristic ways of ending sections/pieces

#### 8. Content Transformation Technique
- Specific techniques for transforming generic content into the analyzed voice
- Before/after examples showing how basic content would be rewritten
- Key modifications that would most effectively capture the voice

#### 9. Topic-Specific Adaptations
- How the voice might adapt to different topics while maintaining consistency
- Topic-specific patterns visible in the sample

#### 10. Vocabulary & Phrasing Guide
- Power Words & Phrases: Distinctive terminology and phrases
- Terms & Phrases to Avoid: Language that would break the voice pattern
- Characteristic jargon or specialized vocabulary

**Technical Implementation Notes:**

- Successfully integrated with enhanced QuantumUniversalCrawler for robust content extraction
- Validated with multiple content types:
  - Technical article (1,685 words extracted)
  - Children's educational book (741 words extracted)
  - Healthcare domain content (31,064 words from 6 sources)
- Creates complete style guides that enable precise voice replication
- System adapts to drastically different writing styles without bias
- Multiple sources can be combined into a single coherent analysis
- System outputs source summary with word counts and source listing
- End-to-end workflow validation from topic → key data sources → tone analysis → article generation

#### Enhanced Tone Analysis and Article Generation Integration (May 2025)

The integration between the Universal Voice Pattern Extraction system and the article generation process has been significantly improved:

##### Tone Analysis to Voice Pattern Mapping

- Implemented precise mapping from 10-part tone analysis structure to the EnhancedArticleGenerator's expected format
- Each part of the Universal Voice Pattern (persona, tone specifications, linguistic patterns, etc.) is correctly transferred
- Added robust fallbacks for missing tone elements to ensure generation quality even with partial analysis
- Enhanced logging for tone mapping to facilitate debugging and quality assurance

##### Prioritized Enhanced Generation

- Modified `generate_advanced_article` to prioritize the EnhancedArticleGenerator
- Added dynamic import mechanism to ensure the enhanced generator is available
- Implemented explicit `use_enhanced_tone` flag to trigger the detailed voice-guided generation
- Created structured fallback chain to maintain service reliability

##### Validation Results

- Successfully generated articles reflecting the detailed tone and style characteristics
- End-to-end testing confirmed proper application of voice patterns from analysis to generation
- Metadata shows `enhanced_openai` provider usage rather than fallback generators
- Performance optimization allows for article generation with proper style in under 60 seconds

#### Section-Based Article Generation System (May 2025)

A sophisticated section-based article generation system has been implemented to produce longer, more comprehensive articles with rich content elements:

##### Four-Stage Generation Process

1. **Outline Generation**: Creates a detailed outline with main sections and subsections based on the topic
2. **Section-by-Section Content**: Generates content for each section independently with dedicated token allocations
3. **Article Assembly**: Combines all sections into a cohesive draft with proper structure
4. **Content Enhancement**: Adds case studies, expert quotes, statistics, and bullet points based on tone requirements

##### Technical Implementation

```python
# The four-stage generation process in EnhancedArticleGenerator
def generate_article(self, article_input):
    # Extract critical inputs from article_input
    topic = article_input.get('topic', '')
    title = article_input.get('title', f'Comprehensive Guide to {topic}')
    target_word_count = article_input.get('target_word_count', 4000)  # Default increased to 4000
    system_prompt = self._create_system_prompt(article_input)
    voice_elements = self._extract_voice_pattern(article_input)
    
    # STEP 1: Generate the detailed outline first
    outline = self._generate_article_outline(topic, title, system_prompt, voice_elements)
    
    # STEP 2: Generate content for each section based on the outline
    section_contents = []
    for i, section in enumerate(outline['sections']):
        section_content = self._generate_section_content(
            topic,
            section['title'],
            i + 1,
            len(outline['sections']),
            system_prompt,
            voice_elements
        )
        section_contents.append(section_content)
    
    # STEP 3: Assemble the article by combining the sections
    assembled_article = self._assemble_article(outline, section_contents)
    
    # STEP 4: Enhance with rich content elements
    enhanced_article = self._enhance_article(assembled_article, voice_elements)
    
    return enhanced_article
```

##### Section Outline Generation Method

```python
def _generate_article_outline(self, topic, title, system_prompt, voice_elements):
    outline_prompt = f"""Create a detailed outline for a comprehensive article about {topic} with the title: '{title}'.
    This outline should include:
    
    1. An engaging introduction that sets the context and importance of {topic}
    2. 5-7 main sections that explore different aspects of {topic} in depth
    3. A compelling conclusion that summarizes key points and offers future perspectives
    
    For each main section, include 2-3 subsection topics that will be covered.
    Format the outline with proper markdown headings (# for title, ## for main sections, ### for subsections).
    The final article will be approximately 4,000 words."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": outline_prompt}
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        outline_text = response.choices[0].message.content
        
        # Process the outline text into a structured format
        sections = self._parse_outline(outline_text)
        
        return {
            "title": title,
            "sections": sections
        }
    except Exception as e:
        logger.error(f"Error generating article outline: {str(e)}")
        # Fallback to a basic outline if generation fails
        return {
            "title": title,
            "sections": [
                {"title": "Introduction", "subsections": []},
                {"title": f"Understanding {topic}", "subsections": []},
                {"title": f"Key Aspects of {topic}", "subsections": []},
                {"title": f"Practical Applications of {topic}", "subsections": []},
                {"title": f"Future of {topic}", "subsections": []},
                {"title": "Conclusion", "subsections": []}
            ]
        }
```

##### Context-Aware Section Generation

- Each section gets specific instructions based on its position and purpose
- Introduction sections focus on establishing context and importance
- Body sections emphasize detailed information, examples, and data
- Conclusion sections focus on summarization and calls to action
- All sections include directives for incorporating case studies, quotes, and statistics

```python
def _generate_section_content(self, topic, section_title, section_num, total_sections, system_prompt, voice_elements):
    # Customize the prompt based on section position (intro, body, conclusion)
    if section_num == 1:
        # Introduction-specific instructions
        section_type_instructions = """This is the introduction section. Focus on:
        - Establishing the importance and relevance of the topic
        - Setting the context and background information
        - Providing a brief overview of what the article will cover
        - Including an engaging hook to capture reader interest"""
    elif section_num == total_sections:
        # Conclusion-specific instructions
        section_type_instructions = """This is the conclusion section. Focus on:
        - Summarizing the key points discussed in the article
        - Reinforcing the main insights and takeaways
        - Offering future perspectives or predictions
        - Ending with a strong call to action or thought-provoking statement"""
    else:
        # Body section-specific instructions
        section_type_instructions = f"""This is body section {section_num} of {total_sections-2}. Focus on:
        - Providing in-depth information about this specific aspect of the topic
        - Including relevant data, statistics, and research findings
        - Sharing detailed examples and case studies
        - Explaining concepts clearly with well-structured arguments"""

    # Enhanced section prompt with rich content elements
    section_prompt = f"""Write detailed content for the '{section_title}' section of an article about {topic}.
    
    {section_type_instructions}
    
    Be sure to include:
    - At least one mini case study or practical example
    - At least one expert quote or insight (attribute to a credible expert in the field)
    - Relevant statistics or data points where appropriate
    - Well-organized bullet points for complex information
    
    Format the content using proper markdown, with ### for subsection headings.
    Write approximately 600-800 words for this section."""
```

##### Dynamic Token Allocation

- Each section receives an independent token allocation (up to 4,000 tokens per section)
- Allows for more detailed content in each section without hitting token limits
- More efficient use of the total token budget compared to a single large generation
- Enables rich content elements that wouldn't fit in a single-pass generation
- Sections typically generate 600-800 words each (5-7 sections = 3,000-5,600 words total)

##### Key Technical Advantages

1. **Scalability**: The section-based approach can easily scale to produce articles of virtually any length by adding more sections

2. **Error Resilience**: If one section fails to generate properly, only that section needs to be regenerated

3. **Content Quality Control**: Each section can be evaluated and regenerated independently if needed

4. **Memory Efficiency**: Generating sections independently requires less context memory than a single large generation

5. **Structural Consistency**: The outline-first approach ensures logical flow and comprehensive coverage

6. **Rich Content Elements**: Each section consistently includes case studies, expert quotes, statistics, and bullet points

7. **Prompt Specialization**: Different prompts for introduction, body, and conclusion sections optimize for their unique purposes

##### Results

- Articles now average 3,600+ words (276% longer than previous 1,300-word articles)
- Comprehensive structure with proper introduction, 5-7 body sections, and conclusion
- Professional formatting with consistent markdown headings (H1-H3) and bullet points
- Rich content elements throughout, including detailed case studies and expert insights
- Tone consistency through proper voice pattern integration in all sections
  - Statistical data supporting key points
  - Bullet points for enhanced readability
  - Strong calls to action in conclusions
- Maintained consistent tone and style throughout extended articles
- Improved article structure with proper section hierarchy and organization

#### QuantumUniversalCrawler Enhancements (May 2025)

##### Topic-Based URL Enrichment System

The QuantumUniversalCrawler has been enhanced with a sophisticated topic-based URL enrichment system that increases the autonomy of content gathering by automatically finding relevant content sources based on the user's topic:

1. **Autonomous URL Discovery**
   - System intelligently enriches generic domain URLs with topic-specific paths
   - Finds entirely new, relevant URLs based on the user's topic
   - Eliminates need for users to provide specific article URLs
   - Integrated directly into the content extraction workflow

2. **Multi-Source URL Generation**
   - Implements domain-specific path generation for 13+ major content domains
   - Uses search APIs for finding topic-relevant content
   - Integrates with Wikipedia's API to find high-quality reference articles
   - Combines and deduplicates results from multiple enrichment sources

3. **Implementation Details**
   ```python
   def extract_from_urls(self, urls: List[str], min_word_target: int = 12000, topic: Optional[str] = None):
       # Enrich URLs based on topic if provided
       if topic and urls:
           logger.info(f"Enriching URLs with topic: {topic}")
           enriched_urls = self.enrich_urls_with_topic(urls, topic)
           # Combine original and enriched URLs, prioritizing enriched ones
           all_urls = list(enriched_urls) + [url for url in urls if url not in enriched_urls]
           logger.info(f"Added {len(enriched_urls) - len(set(urls).intersection(enriched_urls))} topic-specific URLs")
   ```

4. **Domain-Specific Path Generation**
   - Customized path templates for each domain (e.g., search, tag, category pages)
   - Creates topic slugs and query parameters for each domain's URL structure
   - Examples: 
     - ibm.com/topics/{topic-slug}
     - medium.com/tag/{topic-slug}
     - wikipedia.org/wiki/{Topic_Title}

5. **Search API Integration**
   - Uses multiple search methods with fallbacks for reliability
   - Implements DuckDuckGo HTML search for broad result gathering
   - Includes alternative search APIs with appropriate error handling
   - Filters and normalizes URLs to ensure quality content sources

6. **Workflow Integration**
   - Modified workflow_api.py to pass the user's topic to the crawler
   - Processes all URLs in batch mode to maximize enrichment benefits
   - Maintains backward compatibility with topic-less extraction
   - Includes robust fallback to individual URL processing if batch fails

##### Domain-Level URL Handling

The QuantumUniversalCrawler has been enhanced to properly handle domain-level URLs without explicit paths:

1. **Automatic Protocol Handling**
   - URLs without protocol prefixes (http:// or https://) are automatically prefixed with https://
   - Prevents "invalid URL scheme" errors when users provide only domain names
   - Implemented in the `_extract_with_fallbacks` method with protocol detection

2. **Robust Redirect Handling**
   - Implemented `allow_redirects=True` for both TLS client and httpx requests
   - Follows HTTP 301/302 redirects from domain roots to proper landing pages
   - Tracks and logs final URLs after redirects for better content attribution
   - Updates the source URL to the final destination for accurate metadata

3. **Optimized Content-Rich URL Targeting**
   - Identified optimal paths for domain-level content extraction
   - Examples of high-yield URLs that provide 5,000+ words each:
     - wikipedia.org/wiki/Artificial_intelligence_in_healthcare
     - nature.com/articles/s41746-020-00333-z
     - ncbi.nlm.nih.gov/pmc/articles/PMC8285156
   - Successfully extracted 31,064 words across 6 sources for AI in healthcare

4. **Enhanced Error Handling**
   - Improved logging for URL processing and connection issues
   - Added graceful fallbacks for TLS client failures
   - Better error reporting for HTTP status codes
   - Detailed word count tracking per source

#### OpenAI API Integration Improvements (May 2025)

##### API Key Management

The system has been enhanced to support multiple OpenAI API key management approaches:

1. **Environment Variable Method** (Recommended for Production)
   - API keys stored in environment variables via `.env` file or OS environment
   - Set `OPENAI_API_KEY` environment variable for automatic detection
   - Accessed via `os.environ.get('OPENAI_API_KEY')` with fallback option

2. **Hardcoded Key Method** (Prototype Development Only)
   - API key hardcoded in `api_config.py` for simplified prototyping
   - Implementation in `get_openai_api_key()` function returns string directly
   - WARNING: Not recommended for production due to security concerns

3. **Setup Script Integration**
   - Support for `setup_api_keys.sh` that configures keys for the current session
   - Creates a JSON config file with restricted permissions (600)
   - Exports environment variables for immediate use

##### API Error Resolution

Several critical API integration issues were resolved:

1. **Module Import Errors**
   - Fixed `No module named 'app.config'` errors by correcting import paths
   - Changed from relative imports to absolute imports using proper namespace
   - Example: `from fastapi_app.app.config.api_config import get_openai_api_key`

2. **Variable Scope Issues**
   - Resolved `local variable 'openai' referenced before assignment` errors
   - Moved `import openai` to module level for global availability
   - Eliminated redundant imports within functions causing variable shadowing

3. **API Authentication**
   - Enhanced validation for project-based API keys
   - Added proper error handling for API authentication failures
   - Implemented graceful fallbacks for token limit and rate limit scenarios

4. **GPT-4o Integration**
   - Updated system to use the GPT-4o model for tone analysis
   - Specified JSON response format for consistent parsing
   - Optimized prompts for more detailed and structured responses

### 4. Style_Sample_Generation (NEW - May 2025)
   - Generate multiple writing style samples based on tone analysis
   - User reviews and provides feedback on samples
   - Machine learning to refine style based on feedback

5. Article_Generation
   - 4,700+ word articles with professional structure
   - Implementation roadmap section
   - Technical details with component extraction
   - WHAT IF scenarios with alternatives
   - FAQ addressing common objections
   - Proper markdown formatting (H1/H2/H3)

6. Article_Editing (Optional)
   - Section-by-section editing
   - Version history tracking

7. Article_Approval
   - Content validation
   - Final approval status

8. Export_Options
   - Multiple format support (Markdown, HTML, JSON, Text)
   - Download with metadata
   - Export with metadata

API_State_Storage: in-memory + file-based persistence
Workflow_IDs: UUID-based unique identifiers
```

## ERROR_RESOLUTION_PROCEDURES
```error_handling
1. Port_In_Use:
   - Run: fuser -k 8001/tcp
   - Then restart server

2. OpenAI_API_Key_Invalid:
   - Check: cat /root/socialme/social-me-test-2/config/api_keys.json
   - Update: bash /root/socialme/social-me-test-2/update_api_key.sh

3. Missing_Dependencies:
   - Activate venv: source /root/socialme/social-me-test-2/fastapi_app/venv/bin/activate
   - Install: pip install -r requirements.txt
   - Specific for OpenAI tone analyzer: pip install openai tls-client

4. Server_Not_Responding:
   - Check logs: cat /tmp/uvicorn.log
   - Restart: kill and relaunch

5. Article_Not_Found:
   - Check workflow ID format (should be timestamp-based)
   - Verify workflow state file exists

6. Style_Samples_Generation_Failing:
   - Check OpenAI API key validity
   - Check for correct module loading (direct file loading)
   - Verify workflow state persistence (save_workflows function)
```

## FILESYSTEM_ORGANIZATION
```filesystem
/root/socialme/social-me-test-2/
  ├── fastapi_app/         # Main application code
  │   ├── app/             # Core application components
  │   │   ├── tone_adaptation/  # NEW: Tone analysis components
  │   │   │   ├── __init__.py
  │   │   │   ├── openai_tone_analyzer.py  # OpenAI-powered analyzer
  │   │   │   ├── hybrid_tone_adapter.py   # Combined analyzer approach
  │   │   │   └── local_tone_analyzer.py   # Legacy analyzer (fallback)
  │   ├── Context/         # Documentation and technical info (current folder)
  │   ├── enhanced_crawler/ # Enhanced web content extraction
  │   ├── static/          # Static files for web frontend
  │   ├── templates/       # HTML templates
  │   ├── venv/            # Virtual environment (primary)
  │   ├── simple_app.py    # FastAPI application entry point
  │   └── workflow_api.py  # Workflow API implementation
  ├── tests/               # Testing and verification scripts
  │   ├── demo_openai_tone_workflow.py      # NEW: Demo script for OpenAI tone analyzer
  │   ├── verify_openai_tone_adapter.py     # NEW: Verification script
  │   ├── test_openai_tone_analyzer.py      # NEW: Unit tests for OpenAI analyzer
  │   └── test_tone_adaptation_workflow.py  # NEW: Integration tests
  ├── backups/             # System backups
  ├── config/              # Configuration files including API keys
  ├── requirements.txt     # Project dependencies
  └── static/              # Global static assets
      └── complete-workflow-enhanced.html  # New enhanced UI
```

## FRONTEND_IMPLEMENTATION
```frontend
Main_Workflow_UI_Endpoint: /workflow-ui (Direct API endpoint)
Access_URL: http://localhost:8001/workflow-ui
Redirect_URL: http://localhost:8001/static/workflow.html
Implementation: Pure JavaScript + HTML/CSS (no framework)
Backend_Communication: Fetch API with async/await

Key_Components:
  - Article editor with markdown preview
  - Section-by-section editor
  - Version history tracker
  - Format selection for downloads
  - NEW: Style sample review interface with upvote/downvote options
  - NEW: Multiple writing style comparisons
```

## RECENTLY_IMPLEMENTED_FEATURES
```recent_features
1. OpenAI_Tone_Analyzer (NEW - May 2025):
   - Complete implementation in app/tone_adaptation/openai_tone_analyzer.py
   - Modern class-based implementation with direct OpenAI API integration
   - Style sample generation capability (2-5 samples per request)
   - User feedback processing for style refinement
   - Detailed writing style characteristic extraction

2. Style_Sample_Endpoints (NEW - May 2025):
   - POST /api/workflow/{workflow_id}/style-samples
     * Generates 2-5 writing style samples based on provided text
     * Returns detailed style characteristics and sample paragraphs
   - POST /api/workflow/{workflow_id}/style-sample-feedback
     * Processes user feedback on style samples (upvote/downvote)
     * Can regenerate new samples based on feedback
     * Machine learning approach to refine writing style

3. Hybrid_Tone_Adapter (NEW - May 2025):
   - Implementation in app/tone_adaptation/hybrid_tone_adapter.py
   - Combined approach using OpenAI analyzer with local fallback
   - Graceful degradation when API is unavailable
   - Consistent interface regardless of analyzer used

4. Enhanced_Tone_Analysis (May 2025): POST /api/workflow/{workflow_id}/tone-analysis
   - Multi-source input support (text, URL, document)
   - QuantumToneCrawler integration for URL analysis
   - Advanced neural tone mapping with style fingerprinting
   - UI tab interface for different input methods

5. Article_Editing_API: POST /api/workflow/{workflow_id}/article/edit
   - Section-by-section editing
   - Version history tracking

6. Article_Approval_API: POST /api/workflow/{workflow_id}/article/approve
   - Content validation
   - Final approval status

7. Enhanced_Download_API: GET /api/workflow/{workflow_id}/article/download
   - Multiple format support
   - Metadata inclusion

8. Frontend_UI_Enhancements: Direct API endpoint at /workflow-ui
   - Dark-themed interface with numbered steps
   - Advanced editing capabilities
   - Improved user feedback with status messages
   - Multi-source tone analysis UI
```

## DIAGNOSTIC_COMMANDS
```diagnostics
# Check if server is running
lsof -i :8001

# View recent server logs
tail -f /tmp/uvicorn.log
tail -f /tmp/workflow_server.log  # For the standard startup script

# Check OpenAI API key
cat /root/socialme/social-me-test-2/config/api_keys.json | grep -o "sk-[a-zA-Z0-9]*"

# Test tone analysis endpoint
curl -X POST "http://localhost:8001/api/workflow/test-workflow-id/tone-analysis" -H "Content-Type: application/json" -d '{"sample_text":"This is a test of the tone analysis system.","source_type":"text"}'

# Test style samples endpoint
curl -X POST "http://localhost:8001/api/workflow/test-workflow-id/style-samples" -H "Content-Type: application/json" -d '{"sample_text":"This is a test of the style samples generation.","num_samples":2}'

# Test article generation endpoint
curl -X POST "http://localhost:8001/api/workflow/test-workflow-id/article/generate" -H "Content-Type: application/json" -d '{"topic":"AI Testing","settings":{"target_word_count":2000}}'

# Run demonstration workflow with style samples
python /root/socialme/social-me-test-2/tests/demo_openai_tone_workflow.py

# Kill all Python processes (emergency only)
pkill -9 python
```

## CRITICAL_OPERATIONAL_NOTES
```operational_notes
1. ALWAYS run on port 8001 - frontend code has hardcoded references to this port

2. When restarting server:
   - First kill existing process: fuser -k 8001/tcp
   - PREFERRED: Use /root/socialme/social-me-test-2/start_workflow_server.sh

3. Requirements file is at project root, not in fastapi_app directory

4. API key validation must occur before article generation

5. File-based storage: workflow states persist between restarts, but in-memory cache is lost

6. Enhanced article generator requires 4GB+ RAM for optimal performance

7. NEW: OpenAI tone analyzer requires valid API key in config/api_keys.json

8. NEW: After adding new API endpoints, always restart the server to register them
```

## TROUBLESHOOTING_DECISION_TREE
```decision_tree
Issue: Server won't start
├── Port in use? → fuser -k 8001/tcp
├── VirtualEnv active? → source /root/socialme/social-me-test-2/fastapi_app/venv/bin/activate
└── Missing dependencies? → pip install -r requirements.txt

Issue: Article generation fails
├── OpenAI API key invalid? → Update in config/api_keys.json
├── Network connectivity? → Check ping api.openai.com
└── Source content extraction failed? → Check error logs in /tmp/uvicorn.log

Issue: Frontend can't connect to backend
├── Server running? → lsof -i :8001
├── Correct port? → Must be 8001
└── CORS issues? → Check browser console

Issue: Style samples generation fails
├── OpenAI API key valid? → Check config/api_keys.json
├── Import errors? → Check for direct file loading approach (bypassing __init__.py)
├── Workflow state errors? → Verify save_workflows function used (not save_workflow_state)
└── Server needs restart? → Use start_workflow_server.sh
```

## OPENAI_TONE_ANALYZER_IMPLEMENTATION
```openai_tone_analyzer
Implementation Files:
  - /fastapi_app/app/tone_adaptation/openai_tone_analyzer.py (Main analyzer)
  - /fastapi_app/app/tone_adaptation/hybrid_tone_adapter.py (Combined approach)

API Endpoints:
  - POST /api/workflow/{workflow_id}/tone-analysis
    * Used for initial writing style analysis
  - POST /api/workflow/{workflow_id}/style-samples
    * Generates multiple writing style samples (2-5)
    * Returns detailed style characteristics
  - POST /api/workflow/{workflow_id}/style-sample-feedback
    * Processes user feedback on samples
    * Can regenerate new samples based on preferences

Key Features:
  - GPT-4 integration for deep writing style analysis
  - Detailed writing style characteristics extraction
  - Generation of multiple writing style samples
  - Machine learning approach to refine style based on feedback
  - Style adaptation for article generation
  - Bypasses spaCy dependencies issues using direct file loading
  - Graceful fallbacks to local analyzer when needed

API Key Configuration (IMPORTANT):
  - API keys are loaded in the following order of precedence:
    1. Environment variables (OPENAI_API_KEY) - Set in start_workflow_server.sh
    2. .env file in /fastapi_app/.env
    3. Config file at /config/api_keys.json
  - Supported OpenAI key formats:
    * Standard keys (sk-...)
    * Project-based keys (sk-proj-...)
    * Service account keys (sk-svcacct-...)
  - Best practice: Always set the API key in start_workflow_server.sh
  - Verify key with: python /root/socialme/social-me-test-2/check-openai-key.py

Testing & Verification:
  - demo_openai_tone_workflow.py: End-to-end demo of complete workflow
  - verify_openai_tone_adapter.py: Specific verification of feedback processing
  - test_openai_tone_analyzer.py: Unit tests for analyzer methods
  - test_tone_adaptation_workflow.py: Integration tests for workflow

Common Issues:
  - OpenAI API key validation failures (check key format and environment variables)
  - Module import errors (resolved with direct file loading)
  - Workflow state persistence issues (use save_workflows)
  - Server restart required after endpoint additions
  - API key format mismatches (ensures code handles different key formats)
```

## AI_INTERACTION_METADATA
```ai_metadata
Last_Major_Update: 2025-05-09
Implementation_Focus: OpenAI tone analyzer and style sample generation
Key_Contributors: Cascade AI, Human developers
System_Purpose: Generate comprehensive articles with style adaptation
Data_Sources: Web crawling, direct text input, OpenAI API
Content_Architecture: 4,700+ word articles with professional formatting
  - Implementation roadmap
  - Technical details
  - WHAT IF scenarios
  - FAQ addressing objections
  - Style-adapted writing based on user feedback
```
