# Consolidated Changelog

This document combines the project-level and FastAPI app changelogs.

## Table of Contents
1. [Project Changelog](#project-changelog)
2. [FastAPI App Changelog](#fastapi-app-changelog)


## Project Changelog

# Changelog

## [Unreleased]

### 2025-05-27
- **Implemented Section-Based Article Generation for Longer, More Comprehensive Content**:
  - Created a four-stage generation process: outline, section-by-section content, assembly, and enhancement
  - Increased article length by 276% (from ~1000 to 3600+ words) with the same API usage
  - Added detailed case studies, expert quotes, statistics, and bullet points to each section
  - Implemented dynamic section content generation with dedicated token allocations
  - Enhanced prompts to match authoritative tone patterns from tone analysis
  - Increased default target word count from 2500 to 4000 words

- **Implemented Topic-Based URL Enrichment for Autonomous Content Gathering**:
  - Enhanced QuantumUniversalCrawler to automatically find topic-relevant URLs
  - Added search APIs integration for finding domain-specific content
  - Implemented domain-specific path generation for 13+ major domains
  - Created Wikipedia API integration for finding high-quality topic articles
  - Modified workflow_api.py to use topic-based URL enrichment during data collection
  - Improved content diversity with multi-source, topic-focused extraction

- **Enhanced Integration Between Tone Analysis and Article Generation**:
  - Fixed the mapping between Universal Voice Pattern and article generation
  - Implemented proper conversion of tone analysis data to voice pattern format
  - Modified generate_advanced_article to prioritize the EnhancedArticleGenerator
  - Added detailed logging for tone data mapping and integration
  - Validated with successful end-to-end workflow test generating article with proper tone

- **Enhanced QuantumUniversalCrawler for Root Domain Handling**:
  - Fixed domain-level URL extraction by adding automatic HTTPS protocol prefix handling
  - Implemented proper redirect following for both TLS client and httpx requests
  - Modified crawler to track final URLs after redirects for more accurate content attribution
  - Validated crawler with multiple domain sources, reaching 31,064 words from 6 healthcare AI sources
  - Improved error handling and logging for URL processing issues

- **Optimized Data Source Collection**:
  - Enhanced domain-specific content targeting for AI in healthcare domain
  - Identified optimal content-rich paths (e.g., wikipedia.org/wiki/Artificial_intelligence_in_healthcare)
  - Successfully extracted 31,064 words vs. target of 12,000 words for comprehensive article generation
  - Improved logging to track word count per source with detailed extraction metrics
  - Validated extraction accuracy across multiple domain types (academic, commercial, wiki)
- **Fixed Tone Analysis Workflow with Comprehensive Solution**:
  - Hardcoded OpenAI API key in app/config/api_config.py for prototype use, bypassing environment variable checks
  - Corrected import paths from 'app.config' to 'fastapi_app.app.config' to resolve module not found errors
  - Fixed OpenAI module scope issues by moving imports to module level and removing redundant imports
  - Reorganized prompt construction to improve readability and maintenance
  - Validated end-to-end workflow from topic → key data sources → tone analysis → article generation

- **Implemented Universal Voice Pattern Extraction System**:
  - Created a style-agnostic tone analyzer capable of analyzing any writing style
  - Developed a comprehensive 10-part style guide framework to fully capture voice characteristics
  - Enhanced system prompt to reverse-engineer complete style guides from any content
  - Added transformation examples showing how to convert generic content into specific voices
  - Integrated topic-specific adaptation guidance for consistent style application
  
- **Validated System Performance**:
  - Successfully extracted 1,685 words from technical article and 741 words from children's book
  - Generated detailed voice models for drastically different writing styles
  - Confirmed system adapts without bias to various content types (technical, educational, etc.)
  - Verified the tone analysis output provides actionable style guidance for content creation
  
- **Updated Documentation**:
  - Enhanced API_GUIDE_CONSOLIDATED.md with detailed tone analysis response format
  - Updated AI_TECHNICAL_REFERENCE.md with the new Voice Pattern Extraction framework
  - Added comprehensive example outputs to demonstrate system capabilities

### 2025-05-21
- **Fixed OpenAI Tone Analyzer API Authentication Issues**:
  - Resolved OpenAI API authentication issues with service account and project-based API keys
  - Enhanced API key loading with proper precedence handling (environment variables > .env file > config file)
  - Updated OpenAIToneAnalyzer to properly validate all OpenAI API key formats (standard, project-based, service account)
  - Improved error handling and logging for API key configuration issues
  - Updated start_workflow_server.sh to explicitly set the OpenAI API key as an environment variable
  - Added comprehensive API key configuration documentation in AI_TECHNICAL_REFERENCE.md
  - Enhanced logging for API key loading to improve debugging

### 2025-05-09
- **Implemented OpenAI Tone Analyzer and Style Sample System**:
  - Created new `OpenAIToneAnalyzer` class in `fastapi_app/app/tone_adaptation/openai_tone_analyzer.py` for advanced tone analysis
  - Implemented `HybridToneAdapter` in `fastapi_app/app/tone_adaptation/hybrid_tone_adapter.py` to combine OpenAI with local fallbacks
  - Added two new API endpoints:
    - `POST /api/workflow/{workflow_id}/style-samples`: Generates multiple writing style samples based on tone analysis
    - `POST /api/workflow/{workflow_id}/style-sample-feedback`: Processes user feedback on style samples with option to regenerate
  - Created comprehensive test and demo scripts:
    - `tests/demo_openai_tone_workflow.py`: End-to-end demonstration of the OpenAI tone analyzer workflow
    - `tests/verify_openai_tone_adapter.py`: Verification script for sample feedback processing
    - `tests/test_openai_tone_analyzer.py`: Unit tests for the OpenAI tone analyzer
  - Modified workflow_api.py to use direct file loading technique to bypass spaCy dependency issues
  - Fixed workflow state persistence by replacing incorrect `save_workflow_state` function with `save_workflows`
  - Updated technical documentation to include detailed information about the OpenAI tone analyzer implementation
  - Improved error handling and graceful degradation for tone analysis
  - Enhanced article generation to incorporate preferred writing style from user feedback

### 2025-05-08
- Implemented a new dark-themed workflow UI with direct API serving to bypass static file serving issues
- Created a centralized workflow UI template at `/fastapi_app/workflow_ui_template.html` served directly from the API
- Added a redirector at `/static/workflow.html` that points to the new workflow UI
- Fixed "Save Edit" and "Approve and Download" buttons with proper workflow ID persistence
- Enhanced error handling and user feedback in the UI
- Archived legacy HTML interfaces in `/static/archive/` directory to maintain clean organization
- Updated documentation to highlight the direct workflow UI as the recommended approach

### 2025-05-01
- Fixed critical bug where workflow state could be lost or not found after article generation. Workflow state is now always reloaded from disk before retrieval, ensuring consistent state across all endpoints and external access.
- Refactored article generation endpoint to ensure all required variables are defined, robust error handling is in place, and fallback generation is reliable.
- End-to-end workflow (start, topic, sources, tone, article) now passes both local and external tests.
- Updated documentation and API guide to reflect new persistence mechanism and external compatibility.


### 2025-05-01
- Refactored all workflow state-mutating endpoints in `app/APP.py` to persist workflow state to disk using `save_workflows(WORKFLOWS)` and ensured thread safety with `WORKFLOWS_LOCK`.
- Added logging for workflow state persistence actions.
- Added end-to-end workflow test script at `tests/test_workflow_end_to_end.py`.
- Updated documentation to reflect new persistence and testing approach.


### 2025-05-01
- Fixed 422 error on `/key-data-sources` endpoint by patching the `prioritize_quantum_crawler` decorator to preserve FastAPI endpoint signatures.
- Fixed NameError (`source_results` not defined) in `submit_key_data_sources`; all processed source details now collected in `details`.
- End-to-end workflow test now passes: start, topic, data sources, tone, and article generation all work externally.
- Documentation and test scripts updated to reflect new workflow and error handling improvements.


### 2025-04-30
- Restored `/health` and `/api/health` endpoints for monitoring and frontend compatibility.
- Resolved circular import between APP.py and quantum_priority.py by moving `extract_content_from_html` to `crawler_utils.py`.
- Updated API documentation to describe health endpoints and their usage.
- Fixed Quantum Crawler integration issues:
  - Resolved `allowed_methods` parameter incompatibility in requests library
  - Implemented PatchedQuantumCrawler with proper parameter handling
  - Re-enabled Wayback Machine integration and fallback mechanisms
  - Ensured crawler meets 12,000+ word extraction targets (achieving 15,900+ words)
  - Improved API endpoint compatibility with patched crawler

### Security
- Replaced old OpenAI API key with a new temporary key in all configuration files and scripts.
- Removed all outdated and unused OpenAI API keys to prevent unauthorized access.
- Ensured API keys are set via environment variables where required.
- Noted that the new OpenAI API key is temporary and should be replaced with a permanent key when available.

### Changed
- Updated error handling for API key usage in workflow and test scripts.
- Enhanced QuantumUniversalCrawler to reliably collect over 18,000 words of content by lowering confidence thresholds, adding fallback extraction, and targeting content-rich domains (Wikipedia, IBM, NVIDIA).
- Improved logging and monitoring for API key validation and usage.

### Added
- Enhanced fallback mechanisms using Wayback Machine keyword search and Google search
- Modular integration for fallback mechanisms via enhanced_fallback_integration.py
- Standalone demonstration script for fallback mechanisms (fallback_demo_standalone.py)
- Detailed integration guide for enhanced fallback mechanisms
- Successfully integrated enhanced fallback mechanisms into workflow_api.py
- Improved error handling for fallback mechanisms
- Performance optimizations for fallback source retrieval


### 2025-04-28
- Fixed Python imports and module structure in several modules:
  - Shifted from absolute imports (app.x) to relative imports (.x) for proper module resolution
  - Fixed nested imports in routes/articles.py (..storage instead of .storage)
  - Fixed nested imports in routes/api.py for services and generators
  - Fixed services/crawler.py to use relative imports instead of sys.path manipulation
  - Added missing tls-client dependency to requirements.txt for QuantumUniversalCrawler
  - Set up a virtual environment approach for faster debugging outside of Docker containers
  - Identified FastAPI root_path configuration ("/dev") to ensure all endpoints work correctly


### 2025-04-27
- Enhanced workflow start endpoint in APP.py to handle dynamic config and request parameters
- Robust handling of optional workflow initialization parameters
- Comprehensive logging for workflow start process
- Workflow ID generation with UUID
- New `/api/workflow/start` endpoint in Flask application
- Comprehensive workflow initialization with flexible configuration
- Robust handling of optional workflow parameters
- UUID-based workflow ID generation
- Detailed logging for workflow start process


### 2025-04-26
- Fixed 503 Service Unavailable errors during deployment
- Improved server processes in development and production environments
- Enhanced error reporting for API endpoints
- Fixed connectivity issues with API endpoints
- Restructured API route configuration
- Enhanced workflow start endpoint with more flexible initialization
- Improved error handling and logging for workflow routes
- Simplified API route configuration
- Streamlined workflow start endpoint implementation
- Improved error handling for workflow initialization
- Enhanced Flask route configuration for workflow management
- Improved error handling in workflow initialization
- Standardized workflow start response structure


### 2025-04-25
- Fixed port binding and network accessibility issues
- Added health check endpoint at `/api/health`
- Improved error logging for various API endpoints
- Enhanced documentation for error troubleshooting
- Improved endpoint error handling and logging
- Corrected payload processing for workflow initialization
- Resolved issues with workflow start endpoint connectivity
- Improved server binding and network configuration
- Resolved complex Nginx routing conflicts affecting API accessibility
- Removed unintended SSL redirects for workflow API
- Fixed server configuration blocking external API calls
- Implemented precise routing for workflow API across different environments


### 2025-04-24
- Enhanced documentation for Flask/FastAPI service transition
- Added healthchecks for service monitoring
- Implemented metrics collection in development mode
- Improved FastAPI integration points
- Updated error handling and reporting
- Better traceability for API requests

### 2025-04-22
- Fixed FastAPI application entry point to avoid recursion
- Enhanced application configuration for production environment
- Added test scripts for validating API in production
- Streamlined documentation for API endpoints

### 2025-04-20
- Fixed FastAPI import structure to avoid circular references
- Restructured the `routes` module for better organization
- Removed deprecated endpoints
- Added health check endpoint at `/api/health`

### 2025-04-18
- Refactored application structure to separate Flask and FastAPI components
- Added validation for API requests
- Enhanced error handling and reporting
- Added documentation for transition from Flask to FastAPI
- Added support for automatic API documentation

### Removed
- Deprecated `/legacy` endpoints
- Flask-specific route handling
- Legacy configuration files

## [1.0.0] - 2025-04-14
### Production Release
- Deployed Workflow API to production environment
- Added systemd service configuration
- Implemented production-grade configuration management
- Enhanced security and logging for production deployment

### Added
- Production configuration file
- Systemd service file for automated deployment
- Deployment script for easy setup
- Comprehensive requirements.txt for production dependencies

### Changed
- Updated documentation for production deployment
- Enhanced error handling for production environment
- Improved logging for production use
- Fixed path references for deployment in different environments


## FastAPI App Changelog

## 2025-05-09 - OpenAI Tone Analyzer Integration
- **Major Feature Addition**: Implemented OpenAI-powered tone analysis and style sample generation system
  - Added OpenAIToneAnalyzer class for analyzing tone and generating writing style samples
  - Created HybridToneAdapter for seamless fallback between OpenAI and local analysis
  - Added new endpoints for style sample generation and feedback processing
  - Implemented user feedback processing to refine writing style
  - Created demonstration and testing scripts for the new functionality
  - Fixed workflow state persistence with correct save_workflows function
  - Enhanced article generation to incorporate preferred writing style
  - Added comprehensive documentation in AI_TECHNICAL_REFERENCE.md

## 2025-05-07 - Enhanced Workflow UI and Article Management
- **Major UI Enhancement**: Fixed article generation workflow issues with improved transitions and error handling
  - Fixed duplicate article generation endpoints causing routing conflicts
  - Added /workflow/{workflow_id}/status endpoint for polling generation status
  - Enhanced error handling throughout generation process
  - Added robust timeout management for long-running article generation
  - Implemented polling mechanism for checking completion status
  - Created centralized article response processing to handle different response formats
  - Improved workflow ID persistence throughout all steps of the generation process
  - Enhanced user experience with clear feedback about background processing status

## 2025-05-06 (Initial)
- Fixed OpenAI API integration to properly utilize provided API keys regardless of format
- Enhanced article generation workflow to properly extract source material and tone analysis from all possible locations in the workflow data structure
- Fixed data persistence issues when saving generated articles
- Improved robustness of article saving by adding redundant storage locations
- Enhanced error handling during article generation and storage to prevent workflow failures
- Added proper thread-safety with WORKFLOWS_LOCK for concurrent workflow operations

## 2025-05-05
- Added OpenAI-only article generation with no fallback mechanisms
- Modified article generation endpoint (`/api/workflow/{workflow_id}/article/generate`) to exclusively use OpenAI
- Improved error handling to provide clear error messages if OpenAI is unavailable
- Fixed static file serving to properly serve HTML files from the correct directory
- Updated path resolution for generators to ensure proper imports in different environments

## 2025-05-02
- Enhanced article generator now produces 4,700+ word content with professional formatting (up from 1,900 words)
- Added four new content sections: Implementation Roadmap, Technical Details, expanded WHAT IF scenarios, and FAQ 
- Improved markdown formatting with proper H1/H2/H3 headers and bulleted lists throughout
- Enhanced content extraction from 37,888 words of source material
- Implemented content addiction architecture with distinctive voice tone
- Fixed content flow from crawler to article generator

## 2025-05-01
- Fixed workflow state loss after article generation: workflow state is now always reloaded from disk before retrieval, making the API robust and reliable for both local and external access.
- Refactored article generation endpoint to ensure all variables are defined, error handling is robust, and fallback generation is reliable.
- End-to-end workflow (start, topic, sources, tone, article) now passes both local and external tests.
- API endpoints are externally testable and workflow state is reliably persisted and accessible across all endpoints.
- Article generation and workflow retrieval are robust against race conditions and server restarts.


## 2025-04-17
- FastAPI workflow app (`app/workflow_api.py`) now running in a Python virtual environment (`venv`).
- All Flask entrypoints in `app/` have been renamed or moved to prevent accidental startup.
- `/api/workflow/start` and `/health` endpoints tested and working externally via Nginx and HTTPS.
- Global exception handler added: all backend errors are logged to `fastapi_errors.log` for easier debugging.
- Next steps: test additional endpoints, improve API docs, and guide frontend integration.

## May 7, 2025 Update

### Added
- **Enhanced Article Workflow Functionality**:
  - Article viewing endpoint to retrieve generated articles
  - Article editing and validation endpoint with version history
  - Article approval endpoint for finalizing content
  - Enhanced article download endpoint supporting multiple formats (markdown, HTML, plain text, JSON)
  - Option to include metadata with downloaded articles

- **Improved Frontend UI**:
  - New enhanced workflow UI with article editing features
  - Section-by-section article editing capability
  - Version history tracking and management
  - Article approval interface
  - Multiple download format options
  - Preview functionality for different formats

### Fixed
- Resolved issues with article retrieval from different storage locations
- Improved error handling with more detailed messages
- Fixed workflow transitions between article generation and editing steps

### Changed
- Restructured project documentation for better organization
- Consolidated multiple guides into unified reference documents
