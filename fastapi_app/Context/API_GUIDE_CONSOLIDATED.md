# API Documentation and Configuration Guide

This consolidated document combines the API documentation, API guide, and API key configuration.

## Table of Contents
1. [API Overview](#api-overview)
2. [API Key Configuration](#api-key-configuration)
3. [Endpoints Reference](#endpoints-reference)
4. [Integration Guides](#integration-guides)


## API Overview

# SocialMe Workflow API Guide

## Workflow UI Access (UPDATED)

### Direct API Workflow UI (Recommended)

The recommended way to access the SocialMe workflow interface is through the direct API endpoint:

- **UI URL:** `http://localhost:8001/workflow-ui`
- **Access Method:** Direct access via browser
- **Description:** This endpoint serves the complete workflow UI directly from the API, bypassing static file serving issues

### Alternative Access Methods

- **Redirect HTML:** `http://localhost:8001/static/workflow.html` (redirects to the direct workflow UI)
- **Legacy HTML Files:** All previous workflow HTML interfaces have been archived in `/static/archive/`

## Overview

The SocialMe Workflow API provides endpoints for initiating and managing content generation workflows.

## Base URL
```
https://38.242.151.92/api
```

## Authentication
*Currently, no authentication is required. Authentication will be implemented in future versions.*

## Endpoints

### 1. Health Check
- **Endpoint:** `GET /health`
- **Description:** Checks the status of the API and its components
- **Response:**
  ```json
  {
    "status": "healthy",
    "components": {
      "api": "operational",
      "database": "not checked"
    }
  }
  ```

### 2. Workflow Initiation
- **Endpoint:** `POST /api/workflow/start`
- **Description:** Start a new content generation workflow
- **Request Body:**
  ```json
  {
    "project_type": "string",
    "project_details": {
      // Optional detailed configuration
    },
    "user_id": "string (optional)"
  }
  ```
- **Response:**
  ```json
  {
    "status": "workflow initiated",
    "workflow_id": "unique_workflow_identifier",
    "project": "project_type",
    "details": {}
  }
  ```

## Request Examples

### Using Axios (JavaScript/TypeScript)
```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

async function startWorkflow() {
  try {
    const response = await apiClient.post('/workflow/start', {
      project_type: 'blog_post',
      project_details: {
        topic: 'AI in Software Development',
        length: 'long-form'
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error('Workflow start failed', error);
  }
}
```

### Using Fetch (JavaScript)
```javascript
async function startWorkflow() {
  try {
    const response = await fetch('/api/workflow/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        project_type: 'social_media_post',
        project_details: {
          platform: 'twitter',
          tone: 'professional'
        }
      })
    });
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Workflow start failed', error);
  }
}
```

## Error Handling
- Errors will return appropriate HTTP status codes
- Error responses include:
  - `status_code`: HTTP status code
  - `detail`: Error description
  - `request`: Details about the failed request

## CORS Configuration
- All origins are currently allowed
- Supports all HTTP methods
- Allows all headers

## Versioning
- Current API Version: 1.0.0
- Accessible via `/docs` for Swagger UI
- OpenAPI schema at `/openapi.json`

## Upcoming Features
- User authentication
- Workflow status tracking
- More granular project type support

## Troubleshooting
- Ensure network connectivity
- Check CORS settings in your frontend
- Verify API endpoint URL
- Use browser developer tools to inspect network requests

## Contact
For support or feature requests, please contact the SocialMe development team.

## API Key Configuration

# API Key Configuration Guide

This document outlines how to configure API keys for the article generation system.

## Overview of the Configuration System

Our API key management system uses a hierarchical approach with multiple fallback mechanisms to ensure API keys are always available to the backend:

1. **Environment variables** (highest priority)
2. **Configuration file** (second priority)
3. **Hardcoded defaults** (lowest priority, empty by default)

## Setting Up the API Keys

### Method 1: Environment Variables (Recommended for Production)

Set the following environment variables on your server:

```bash
export OPENAI_API_KEY=your-openai-key-here
export ANTHROPIC_API_KEY=your-anthropic-key-here
```

For persistent configuration, add these to your server's environment configuration or service definition.

### Method 2: Configuration File

You can store API keys in a JSON configuration file at `/config/api_keys.json`:

```json
{
    "OPENAI_API_KEY": "your-openai-key-here",
    "ANTHROPIC_API_KEY": "your-anthropic-key-here"
}
```

**Important security note:** Restrict access to this file using appropriate permissions:

```bash
chmod 600 /path/to/config/api_keys.json
```

### Method 3: Automated Setup

Use the provided setup script to configure your API keys:

```bash
# Set environment variables first
export OPENAI_API_KEY=your-openai-key-here
export ANTHROPIC_API_KEY=your-anthropic-key-here

# Then run the setup script
./setup_api_keys.sh
```

This will create/update the configuration file with the current environment variables.

## Troubleshooting

If you're experiencing issues with API key access:

1. **Check environment variables** are correctly set:
   ```bash
   echo $OPENAI_API_KEY
   echo $ANTHROPIC_API_KEY
   ```

2. **Verify configuration file** exists and has correct permissions:
   ```bash
   ls -la /path/to/config/api_keys.json
   ```

3. **Check application logs** for API key-related errors:
   ```bash
   grep -i "api key" /path/to/logs/fastapi_errors.log
   ```

4. **Test key validity** using a simple script:
   ```bash
   python3 -c "from fastapi_app.app.config.api_config import get_openai_api_key; print(f'OpenAI API key found: {get_openai_api_key() is not None}')"
   ```

## Deployment Considerations

When deploying to production:

1. **Never commit API keys** to version control
2. **Use environment variables** in orchestration systems like Docker, Kubernetes, etc.
3. **Implement key rotation** policies for enhanced security
4. **Monitor API key usage** to detect unauthorized access

## Fixing 500 Error on API Documentation

If you're seeing a 500 error when accessing `/docs` on your API:

1. Ensure all required environment variables are set
2. Check that the API key configuration is valid
3. Verify the service has proper permissions to read the configuration file
4. Check logs for specific error messages
5. Restart the service after configuring API keys

## Endpoints Reference

# SocialMe Content Generation Workflow API

## Overview
This API provides a comprehensive workflow for generating content with advanced AI capabilities, featuring enhanced fallback mechanisms for retrieving content when direct URL crawling doesn't yield sufficient results.

## Authentication
- All endpoints require a unique `workflow_id`
- Session management handled server-side

## Endpoints

### Health Check Endpoints

#### `GET /health`
- Returns the health status of the API server.
- Useful for monitoring and frontend compatibility.

#### Example Response
```json
{
  "status": "ok",
  "version": "2.0.0",
  "timestamp": "2025-04-30T15:48:52.579182"
}
```

#### `GET /api/health`
- Compatibility endpoint for health checks with `/api` prefix.
- Returns the same response as `/health`.

---

## Frontend Integration & API Guide

### User Workflow (Frontend)
1. User inputs their topic and avatar
2. User provides URLs or documents as sources for key information
3. User provides documents or links for tone sources
4. User can edit or approve the result of the tone analysis
5. Article is processed and generated

### API Endpoint Sequence
1. `/api/workflow/start`
    - Initialize a new workflow session
    - Generate a unique workflow ID
    - Set initial workflow state
    - Return session details and initial configuration options
2. `/api/workflow/{workflow_id}/topic`
    - Submit primary and optional secondary topics
    - Validate and store topic information
    - Return topic confirmation and next workflow step
3. `/api/workflow/{workflow_id}/avatar`
    - Upload or select user avatar
    - Store avatar metadata and link to session
    - Return avatar confirmation
4. `/api/workflow/{workflow_id}/key-data-sources`
    - Add sources: URLs, document uploads, or direct text
    - Categorize sources and perform extraction/validation
    - Return source processing status
5. `/api/workflow/{workflow_id}/tone-analysis`
    - Add tone sources: URLs, documents, or text
    - Categorize tone sources and perform extraction/validation
    - Return tone analysis and allow editing/approval
6. `/api/workflow/{workflow_id}/generate-article`
    - Trigger article generation based on collected data and tone
    - Return generated article draft with metadata
7. `/api/workflow/{workflow_id}/validate-article`
    - Allow user to review, edit, and validate article
    - Track version history and provide final approval

### Recommendations for Frontend
- Store `workflow_id` in client-side session
- Implement sequential API calls following the workflow steps
- Handle potential errors and edge cases gracefully

---

### Technical Overview
- **Modular API-driven design**
- Granular, stepwise workflow
- Flexible input sources (URL, docs, text)
- Advanced NLP and neural tone mapping
- Modular crawler architecture for data and tone

### Key Technologies
- FastAPI, Python 3.9+
- SpaCy, scikit-learn, custom NLP modules

### Prototype Capabilities
- Adaptive content generation
- Multi-source data integration
- Sophisticated style analysis
- Personalized content creation

### Limitations & Future Enhancements
- Prototype stage, limited error handling
- Scalability to be determined
- Potential for ML model training, advanced tone transfer, and more personalization

---

### API Contract Review

#### 1. `/api/workflow/start`
**Request:** `POST /api/workflow/start`
```json
{}
```
**Response:**
```json
{
  "workflow_id": "unique_uuid_string",
  "initial_config": {
    "workflow_version": "2.0",
    "supported_features": [
      "topic_input", "avatar_upload", "data_sources", "tone_sources", "article_generation"
    ]
  }
}
```
**Strengths:** Unique workflow ID, clear config. **Improvements:** Add timestamp, optional config.

#### 2. `/api/workflow/{workflow_id}/topic`
**Request:** `POST /api/workflow/{workflow_id}/topic`
```json
{
  "primary_topic": "string",
  "secondary_topics": ["optional", "topics"]
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Topic submitted successfully"
}
```
**Strengths:** Supports primary/secondary topics. **Improvements:** Add validation, return details.

#### 3. `/api/workflow/{workflow_id}/avatar`
**Request:** `POST /api/workflow/{workflow_id}/avatar`
```json
{
  "avatar_url": "optional_url_string",
  "avatar_file": "optional_base64_encoded_file"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Avatar uploaded successfully"
}
```
**Strengths:** URL/file upload. **Improvements:** Add validation, metadata.

#### 4. `/api/workflow/{workflow_id}/key-data-sources` (Enhanced May 2025)
**Request:** `POST /api/workflow/{workflow_id}/key-data-sources`
```json
{
  "urls": ["wikimedia.org", "wired.com", "medium.com", "ibm.com"],
  "documents": ["optional docs"],
  "text_input": "optional text"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Successfully processed 6 sources",
  "sources_processed": 6,
  "total_word_count": 31064,
  "extraction_method": "enhanced",
  "source_details": [
    {
      "url": "wikipedia.org/wiki/Artificial_intelligence_in_healthcare",
      "title": "Artificial intelligence in healthcare - Wikipedia",
      "word_count": 12467,
      "confidence": 0.95,
      "extraction_method": "article_tags"
    },
    {
      "url": "ncbi.nlm.nih.gov/pmc/articles/PMC8285156",
      "title": "Artificial intelligence in healthcare: transforming the practice ...",
      "word_count": 9522,
      "confidence": 0.91,
      "extraction_method": "main_content"
    }
  ]
}
```
**Strengths:** 
- Domain-level URL support with automatic HTTPS protocol prefixing
- Robust redirect handling for maximum content extraction
- Optimized targeting of content-rich paths
- Detailed extraction metrics with word counts and confidence scores
- Multiple extraction methods with fallbacks (article_tags, main_content, etc.)
- Successfully extracting 31,000+ words from just 6 sources

**Technical Implementation:**
- Enhanced QuantumUniversalCrawler with protocol detection and auto-prefixing
- Redirect following via allow_redirects parameter for both TLS client and httpx
- Updated URL tracking to maintain source attribution after redirects
- Improved logging for better debugging and monitoring
- Support for academic, commercial, and wiki content sources

#### 5. `/api/workflow/{workflow_id}/tone-analysis` (Enhanced May 2025)
**Request:** `POST /api/workflow/{workflow_id}/tone-analysis`

*Three input methods are supported:*

1. **Direct Text Input:**
```json
{
  "source_type": "text",
  "sample_text": "This is a sample of the writing style for tone analysis..."
}
```

2. **URL Analysis:**
```json
{
  "source_type": "url",
  "url": "https://example.com/article-with-desired-tone"
}
```

3. **Document Upload:**
```json
{
  "source_type": "document",
  "document_content": "base64_encoded_document_content"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Tone analysis completed successfully from combined sources",
  "tone_analysis": {
    "PART 1: Structural Fingerprint Analysis": {
      "Document Structure": "Analysis of overall document organization and layout",
      "Sentence Architecture": "Patterns in sentence length, complexity, and variation",
      "Visual Formatting Patterns": "Use of formatting elements like bullets, headings, etc."
    },
    "PART 2: Linguistic Pattern Analysis": {
      "Vocabulary & Word Choice": "Terminology patterns and lexical preferences",
      "Pronoun Usage": "Patterns in first/second/third person usage",
      "Tense & Perspective": "Dominant tense and narrative perspective",
      "Punctuation Fingerprint": "Characteristic punctuation patterns"
    },
    "PART 3: Rhetorical Strategy Mapping": {
      "Opening Techniques": "How content typically begins",
      "Persuasive Framework": "Approach to persuasion and argument structure",
      "Authority Establishment": "Methods used to establish credibility",
      "Transition Techniques": "How ideas are connected and flow managed",
      "Conclusion Patterns": "Characteristic closing approaches"
    },
    "PART 4: Content Strategy Analysis": {
      "Topic Approach": "How subjects are introduced and framed",
      "Example Usage": "Patterns in illustration and example deployment",
      "Data Presentation": "How facts and figures are incorporated",
      "Framework Creation": "Methods of organizing concepts",
      "Contrarian Elements": "Use of opposing viewpoints and challenges"
    },
    "PART 5: Emotional Texture Mapping": {
      "Tone Spectrum": "Range from formal to casual, positive to critical",
      "Humor Profile": "Use and type of humor if present",
      "Reader Relationship": "How the content engages and relates to audience",
      "Distinctive Emotional Markers": "Unique emotional characteristics"
    },
    "PART 6: Synthesis & Voice Model Creation": {
      "Voice Foundation": "Core voice characteristics and identity",
      "Style Elements Catalog": "Distinct stylistic patterns and techniques",
      "Language Pattern Guide": "Vocabulary preferences and linguistic signatures",
      "Content Framework": "Organizational preferences and structural tendencies",
      "Transformation Examples": "Examples showing voice application"
    }
  },
  "source_summary": {
    "sources": ["URL: https://example.com/article-with-desired-tone"],
    "total_words": 1685
  }
}
```

**Implementation Notes:**
- The enhanced tone analysis system now integrates with QuantumUniversalCrawler for improved content extraction
- Successfully tested with extraction of 1,685 words from source material
- Analysis uses the comprehensive 'Client Voice Analysis System' framework with six major analysis categories
- Multiple sources can be combined into a single coherent analysis
- The system has been validated end-to-end with the complete workflow sequence

#### 6. `/api/workflow/{workflow_id}/style-samples` (NEW - May 2025)
**Request:** `POST /api/workflow/{workflow_id}/style-samples`

Generates multiple writing style samples based on analysis of provided text. Used to verify the detected writing style matches the user's preferences.

```json
{
  "sample_text": "This is a sample of my writing style that will be analyzed...",
  "num_samples": 3,
  "target_length": 250
}
```

**Response:**
```json
{
  "status": "success",
  "style_analysis": {
    "key_characteristics": ["formal", "analytical", "technical", "academic", "structured"],
    "distinctive_patterns": ["complex sentences", "third-person perspective", "passive voice"]
  },
  "samples": [
    {
      "id": 1,
      "sample_text": "The implementation of advanced algorithms in modern software development demonstrates...",
      "topic": "Technology Integration"
    },
    {
      "id": 2,
      "sample_text": "Research indicates that environmental sustainability initiatives have gained momentum...",
      "topic": "Environmental Policy"
    },
    {
      "id": 3,
      "sample_text": "Financial market analysis suggests that diversification strategies continue to...",
      "topic": "Economic Trends"
    }
  ]
}
```

#### 7. `/api/workflow/{workflow_id}/style-sample-feedback` (NEW - May 2025)
**Request:** `POST /api/workflow/{workflow_id}/style-sample-feedback`

Provides feedback on generated style samples. Can optionally request new samples based on feedback.

```json
{
  "sample_id": 2,
  "rating": "upvote",
  "comments": "This style matches my writing very well",
  "regenerate": false
}
```

Or for regeneration:

```json
{
  "sample_id": 3,
  "rating": "downvote",
  "comments": "Too informal, not my style",
  "regenerate": true,
  "num_samples": 3
}
```

**Response with regenerate=false:**
```json
{
  "status": "success",
  "message": "Feedback recorded successfully"
}
```

**Response with regenerate=true:**
```json
{
  "status": "success",
  "style_analysis": {
    "adjusted_characteristics": ["more formal", "structured", "evidence-based"],
    "avoided_patterns": ["casual tone", "first-person perspective"]
  },
  "samples": [
    {
      "id": 4,
      "sample_text": "The analysis of economic indicators reveals significant trends...",
      "topic": "Economic Analysis"
    },
    // Additional samples...
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Tone analysis completed successfully from URL: https://example.com/article",
  "tone_analysis": {
    "neural_tone_analysis": {
      "formality": "formal",
      "complexity": "high",
      "primary_sentence_type": "declarative"
    },
    "detail_metrics": {
      "avg_word_length": 5.32,
      "avg_sentence_length": 18.7,
      "formal_word_count": 42,
      "informal_word_count": 12,
      "question_count": 3,
      "exclamation_count": 1
    },
    "extended_attributes": {
      "readability": "medium",
      "persuasiveness": "high",
      "engagement": "medium"
    },
    "style_fingerprints": {
      "basic": [
        "Example sentence that represents the tone",
        "Another characteristic phrase from the content"
      ],
      "advanced": [
        "Primary domain: academic",
        "Dominant thought pattern: analytical",
        "Dominant reasoning style: deductive"
      ]
    }
  }
}
```

**✅ Strengths:**
* Multiple input methods (text, URL, document)
* Comprehensive tone profile with neural analysis
* Detailed metrics on writing style characteristics
* Style fingerprinting with key phrase extraction
* Advanced domain and thought pattern detection

**🔄 Implementation Notes:**
* URL analysis uses QuantumToneCrawler with advanced anti-bot measures
* Document upload supports txt, md, doc, docx, and pdf formats
* Multiple sources can be combined in the workflow UI
**Strengths:** Comprehensive analysis. **Improvements:** Add consistency metrics, adaptation suggestions.

#### 6. `/api/workflow/{workflow_id}/generate-article`
**Request:** `POST /api/workflow/{workflow_id}/generate-article`
```json
{}
```
**Response:**
```json
{
  "status": "success",
  "article": {
    "text": "Generated content",
    "title": "Generated title",
    "metadata": {
      "word_count": 750,
      "reading_time": "4 min",
      "tone_profile": "professional"
    }
  }
}
```
**Response:**
```json
{
  "status": "success",
  "article": {
    "title": "Comprehensive Guide to Quantum Computing",
    "content": "Full article content in Markdown format with proper section structure",
    "word_count": 3600,
    "metadata": {
      "generation_time": 165,
      "sources_used": 7,
      "provider": "enhanced_openai",
      "sectioned_generation": true,
      "enhancement_applied": true,
      "sections_generated": 8
    }
  }
}
```
**Strengths:** 
- Advanced section-based generation producing 3,600+ word articles (276% longer than previous system)
- Structured content with proper hierarchical organization
- Rich content elements including case studies, expert quotes, statistics, and bullet points
- Enhanced content following the specified tone pattern from tone analysis
- Dynamic token allocation across multiple sections for detailed content
- Comprehensive article structure with proper introduction, body sections, and conclusion

#### 7. `/api/workflow/{workflow_id}/validate-article`
**Request:** `POST /api/workflow/{workflow_id}/validate-article`
```json
{
  "edits": {
    "tone": "More academic",
    "sections": {}
  }
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Article validated",
  "article": {},
  "versions": [
    {
      "timestamp": "ISO_TIMESTAMP",
      "version_data": {}
    }
  ]
}
```
**Strengths:** Editing, versioning. **Improvements:** Add collaborative/diff support.

---

The API incorporates sophisticated fallback retrieval when primary sources are insufficient:

- **Multi-layered fallback strategy**: Automatically tries multiple methods to find relevant content
- **Wayback Machine integration**: Retrieves historical versions of relevant pages
- **Google search integration**: Identifies additional content sources related to the topic
- **Performance optimization**: Parallel processing, caching, and sophisticated retry logic
- **Circuit breaker patterns**: Prevents overwhelming external APIs during outages
- **Production-grade logging**: Comprehensive tracking of all fallback operations

### 1. Start Workflow
`POST /api/workflow/start`
- Initializes a new workflow session
- Returns:
  - `workflow_id`: Unique identifier for the session
  - `initial_config`: Workflow configuration details

#### Example Request
```json
{}
```

#### Example Response
```json
{
  "workflow_id": "uuid-v4-string",
  "initial_config": {
    "workflow_version": "2.0",
    "supported_features": [
      "topic_input",
      "avatar_upload", 
      "data_sources", 
      "tone_sources", 
      "article_generation"
    ]
  }
}
```

### 2. Submit Topic
`POST /api/workflow/{workflow_id}/topic`
- Submit primary and secondary topics for content generation

#### Example Request
```json
{
  "primary_topic": "AI in Healthcare",
  "secondary_topics": ["Machine Learning", "Medical Diagnostics"]
}
```

### 3. Upload Avatar
`POST /api/workflow/{workflow_id}/avatar`
- Upload or select user avatar

#### Example Request
```json
{
  "avatar_url": "https://example.com/avatar.jpg"
}
```

### 4. Add Data Sources (Enhanced May 2025)
`POST /api/workflow/{workflow_id}/key-data-sources`
- Submit URLs for content data extraction
- **NEW:** Now supports domain-level URLs (e.g., ibm.com) with automatic protocol handling
- **NEW:** Implements robust redirect following to maximize content extraction
- **NEW:** Optimized for content-rich paths to reach 30,000+ word extraction

#### Example Request
```json
{
  "urls": [
    "https://www.nature.com/articles/example",
    "https://www.scientificamerican.com/article/ai-healthcare"
  ]
}
```

### 5. Tone Analysis
`POST /api/workflow/{workflow_id}/tone-analysis`
- Submit sources for tone and style analysis

#### Example Request
```json
{
  "urls": [
    "https://www.wired.com/story/ai-medical-breakthroughs",
    "https://www.scientificamerican.com/article/ai-in-medicine"
  ]
}
```

### 6. Generate Article
`POST /api/workflow/{workflow_id}/generate-article`
- Trigger article generation based on previous inputs

#### Example Response
```json
{
  "status": "success",
  "article": {
    "text": "Generated article content...",
    "word_count": 500
  }
}
```

### 7. Validate Article
`POST /api/workflow/{workflow_id}/validate-article`
- Review and validate generated article

#### Example Request
```json
{
  "edits": {
    "tone": "More academic",
    "length": "Reduce by 20%"
  }
}
```

## Error Handling
- 400: Bad Request
- 404: Not Found
- 500: Server Error

## Recommended Frontend Workflow
1. Call `/start` to get `workflow_id`
2. Sequentially call other endpoints
3. Handle each response for user feedback
4. Use `workflow_id` for all subsequent requests

## Article Workflow Enhancements (May 2025 Update)

### Workflow UI Improvements (May 8, 2025)

A new dark-themed workflow interface has been implemented with direct API serving to avoid static file serving issues:

```
GET /workflow-ui
```

This endpoint directly serves the SocialMe workflow UI from the FastAPI application. It provides a streamlined interface with:

- Numbered step navigation (Topic → Sources → Style → Generate → View)
- Dark theme for improved readability
- Persistent workflow ID storage across steps
- Enhanced error handling with status messages
- Improved "Save Edit" and "Approve & Download" functionality

**Access Methods:**
- Direct access (recommended): `http://localhost:8001/workflow-ui`
- Redirector: `http://localhost:8001/static/workflow.html`

### Article Endpoints

The following endpoints have been added to enhance the article workflow functionality:

### Article Viewing Endpoint

```
GET /api/workflow/{workflow_id}/article
```

Retrieves the generated article for a specific workflow.

**Parameters:**
- `workflow_id` (path parameter): The ID of the workflow

**Responses:**
- `200 OK`: Returns the article content and metadata
- `404 Not Found`: Article not found for the given workflow ID

**Example Response:**
```json
{
  "content": "# Article Title\n\nArticle content goes here...",
  "title": "Article Title",
  "word_count": 4703,
  "status": "generated"
}
```

### Article Editing Endpoint

```
POST /api/workflow/{workflow_id}/article/edit
```

Allows editing the generated article and saves the edited version.

**Parameters:**
- `workflow_id` (path parameter): The ID of the workflow

**Request Body:**
```json
{
  "content": "Updated article content",
  "title": "Updated Title",
  "version_name": "Draft 2",
  "comments": "Fixed grammar issues and improved conclusion"
}
```

**Responses:**
- `200 OK`: Article successfully edited and version saved
- `404 Not Found`: Article not found for the given workflow ID

**Example Response:**
```json
{
  "status": "success",
  "message": "Article updated successfully",
  "version": {
    "version_name": "Draft 2", 
    "timestamp": "2025-05-07T08:30:00",
    "word_count": 4750
  }
}
```

### Article Approval Endpoint

```
POST /api/workflow/{workflow_id}/article/approve
```

Approves the article for publication.

**Parameters:**
- `workflow_id` (path parameter): The ID of the workflow

**Request Body:**
```json
{
  "approved": true,
  "publish": true
}
```

**Responses:**
- `200 OK`: Approval status updated successfully
- `404 Not Found`: Article not found for the given workflow ID

**Example Response:**
```json
{
  "status": "success",
  "message": "Article approved and published",
  "approval_status": {
    "approved": true,
    "published": true,
    "timestamp": "2025-05-07T09:00:00"
  }
}
```

### Enhanced Article Download Endpoint

```
GET /api/workflow/{workflow_id}/article/download
```

Downloads the article in the requested format.

**Parameters:**
- `workflow_id` (path parameter): The ID of the workflow
- `format` (query parameter): The desired format (markdown, html, text, json)
- `include_metadata` (query parameter): Whether to include metadata (true/false)

**Responses:**
- `200 OK`: Returns the article in the requested format
- `404 Not Found`: Article not found for the given workflow ID
- `400 Bad Request`: Invalid format requested

The response will vary based on the requested format:
- Markdown: Returns the article as markdown text
- HTML: Returns the article as HTML
- Text: Returns the article as plain text
- JSON: Returns the article with metadata as JSON

These new endpoints enable a complete end-to-end workflow for article generation, editing, approval, and multi-format downloading.
# OpenAI Tone Analyzer Integration

## Overview

The OpenAI Tone Analyzer is a new integration that provides advanced writing style analysis and sample generation capabilities to the SocialMe workflow. This system uses the OpenAI API to analyze writing styles, generate multiple style samples, and process user feedback to refine the writing style used in article generation.

## Key Components

### 1. OpenAIToneAnalyzer

Located at `/fastapi_app/app/tone_adaptation/openai_tone_analyzer.py`, this class provides:

- Writing style analysis using OpenAI's GPT-4 model
- Generation of multiple writing style samples
- Processing of user feedback to refine writing style
- Integration with the article generation workflow

### 2. HybridToneAdapter

Located at `/fastapi_app/app/tone_adaptation/hybrid_tone_adapter.py`, this adapter:

- Combines OpenAI tone analysis with local fallback options
- Provides a unified interface regardless of analyzer used
- Handles graceful degradation when API is unavailable

## New API Endpoints

### Style Samples Generation

```
POST /api/workflow/{workflow_id}/style-samples
```

Generates multiple writing style samples based on the provided text.

**Request Body:**
```json
{
  "sample_text": "Text sample for style analysis...",
  "num_samples": 3,
  "target_length": 250
}
```

**Parameters:**
- `sample_text` (required): Text sample to analyze for style characteristics
- `num_samples` (optional): Number of samples to generate (default: 3, range: 1-5)
- `target_length` (optional): Target length of each sample in words (default: 250, range: 50-500)

**Response:**
```json
{
  "status": "success",
  "style_analysis": {
    "key_characteristics": [
      "Formal tone with technical accuracy",
      "Complex sentence structures",
      "Domain-specific vocabulary",
      "Analytical reasoning",
      "Evidence-based claims"
    ],
    "distinctive_patterns": [
      "Frequent use of terms like 'paradigm shift' and 'efficacy'",
      "Structured argumentation with logical flow",
      "References to specific fields or domains"
    ]
  },
  "samples": [
    {
      "id": 1,
      "sample_text": "The emergence of artificial intelligence in modern business processes signifies a profound transformation in operational dynamics...",
      "topic": "Artificial Intelligence in Business Operations"
    },
    {
      "id": 2,
      "sample_text": "The widespread adoption of renewable energy sources in global power generation marks a pivotal evolution in energy strategies...",
      "topic": "Renewable Energy in Power Generation"
    },
    {
      "id": 3,
      "sample_text": "Recent advancements in quantum computing algorithms demonstrate significant progress toward solving previously intractable problems...",
      "topic": "Quantum Computing Applications"
    }
  ],
  "original_text": "The integration of quantum computing into practical applications represents a significant paradigm shift in computational methodologies..."
}
```

### Style Sample Feedback

```
POST /api/workflow/{workflow_id}/style-sample-feedback
```

Process user feedback on generated style samples and optionally regenerate new samples.

**Request Body:**
```json
{
  "sample_id": 2,
  "rating": "upvote",
  "comments": "This style matches what I'm looking for",
  "regenerate": false
}
```

**Parameters:**
- `sample_id` (required): ID of the sample being rated
- `rating` (required): Rating type - "upvote", "downvote", or "neutral"
- `comments` (optional): User comments about the rating
- `regenerate` (optional): Whether to generate new samples based on feedback (default: false)
- `num_samples` (optional): Number of new samples to generate if regenerate is true (default: 3)

**Response (without regeneration):**
```json
{
  "status": "success",
  "message": "Feedback recorded successfully"
}
```

**Response (with regeneration):**
```json
{
  "status": "success",
  "message": "Generated new samples based on your feedback",
  "samples": [
    {
      "id": 4,
      "sample_text": "The analysis of economic indicators reveals significant trends...",
      "topic": "Economic Analysis"
    },
    {
      "id": 5,
      "sample_text": "Contemporary research in neuroplasticity demonstrates remarkable capabilities...",
      "topic": "Neuroscience Research"
    },
    {
      "id": 6,
      "sample_text": "The examination of global climate data illustrates concerning patterns...",
      "topic": "Climate Science"
    }
  ]
}
```

## Integration with Article Generation

The selected writing style (based on user feedback) is incorporated into the article generation process, affecting:

1. Tone and formality level
2. Sentence structure complexity
3. Vocabulary choices
4. Overall writing style characteristics

This integration creates a more personalized content generation experience, allowing users to influence the writing style of their generated articles.

## Technical Implementation Notes

1. **Direct File Loading:** The OpenAIToneAnalyzer is loaded using direct file imports to bypass potential spaCy dependency issues:
   ```python
   import importlib.util
   spec = importlib.util.spec_from_file_location("openai_tone_analyzer", analyzer_path)
   openai_tone_analyzer = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(openai_tone_analyzer)
   ```

2. **Workflow State Management:** Style samples and feedback are stored in the workflow state under:
   ```
   WORKFLOWS[workflow_id]["style_samples"] = result
   ```

3. **OpenAI API Configuration:** The system uses the OpenAI API key stored in:
   ```
   /root/socialme/social-me-test-2/config/api_keys.json
   ```

## Example Usage with cURL

```bash
# Generate style samples
curl -X POST "http://localhost:8001/api/workflow/example-workflow-id/style-samples" \
  -H "Content-Type: application/json" \
  -d '{
    "sample_text": "The integration of quantum computing into practical applications represents a significant paradigm shift in computational methodologies. Contemporary research indicates that quantum systems exhibit considerable potential in addressing complex optimization problems that remain intractable for classical computing architectures.",
    "num_samples": 2
  }'

# Submit feedback on a sample
curl -X POST "http://localhost:8001/api/workflow/example-workflow-id/style-sample-feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "sample_id": 1,
    "rating": "upvote"
  }'
```

## Common Error Resolution

1. **Server Errors (500):** If you encounter 500 Internal Server Error when accessing the style samples endpoint, check:
   - OpenAI API key validity
   - Direct file loading implementation
   - Workflow state persistence (use save_workflows function)

2. **Import Errors:** If the OpenAI tone analyzer can't be loaded:
   - Verify the file path in the direct import implementation
   - Check for modified imports in the tone_adaptation modules
   - Make sure the OpenAI Python package is installed

3. **No Style Samples Generated:** If no samples are returned:
   - Check if the sample text provided is long enough
   - Verify OpenAI API connectivity
   - Look for parsing errors in the OpenAI response

## Combining with Section-Based Article Generation

The OpenAI tone analyzer works in conjunction with the enhanced section-based article generator to produce comprehensive, well-structured content with professional formatting. The system employs a sophisticated four-stage generation process:

1. **Outline Generation**: Creates a detailed outline with main sections and subsections based on the topic
2. **Section-by-Section Content**: Generates content for each section independently with dedicated token allocations
3. **Article Assembly**: Combines all sections into a cohesive draft with proper structure
4. **Content Enhancement**: Adds case studies, expert quotes, statistics, and bullet points based on tone requirements

### Key Technical Advantages

- **Dynamic Token Allocation**: Each section receives an independent token allocation (up to 4,000 tokens per section)
- **Context-Aware Generation**: Different prompts for introduction, body, and conclusion sections
- **Enhanced Content Elements**: Automatically adds case studies, expert quotes, statistics, and bullet points
- **Tone Consistency**: Maintains the analyzed tone throughout the entire article
- **Increased Output Length**: Produces articles averaging 3,600+ words (276% longer than previous system)

The selected writing style from tone analysis influences:

1. Overall voice and tone characteristics
2. Vocabulary choices and power words
3. Sentence and paragraph structure patterns
4. Content organization and section frameworks
5. Types of examples and case studies included
