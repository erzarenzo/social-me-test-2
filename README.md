# SocialMe

SocialMe is an AI-powered content creation platform that helps users generate high-quality articles based on data sources, writing style analysis, and content strategy.

## Application Structure

The SocialMe application follows a standardized architecture:

### Core Components

- **app.py**: Main application entry point
- **app/**: Core application modules
  - **crawlers/**: Standardized web crawling implementations
  - **generators/**: Content generation modules
  - **routes/**: API and web route handlers
  - **models/**: Database models
  - **services/**: Business logic services
  - **utils/**: Helper utilities
  - **core/**: Core functionality

### Templates

- **templates/**: Web UI templates
  - **articles/**: Article-related templates
  - **auth/**: Authentication templates
  - **content/**: Content creation templates
  - **layout/**: Layout templates (base templates, etc.)
  - **components/**: Reusable UI components
  - **onboarding/**: User onboarding workflow templates

### Static Assets

- **static/**: Web assets
  - **css/**: Stylesheet files
  - **js/**: JavaScript files
  - **images/**: Image files

## Key Workflows

### Article Generation Workflow

1. **Step 1: Content Sources** - User inputs text, documents, or URLs as sources for key datapoints
2. **Step 2: Writing Style Analysis** - User provides sources for tone analysis
3. **Step 3: Content Strategy** - User defines topics, target audience, and content strategy
4. **Step 4: Article Generation** - System generates a 4000-word article using crawled content and user inputs