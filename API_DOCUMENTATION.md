# SocialMe Content Generation Workflow API

## Overview
This API provides a comprehensive workflow for generating content with advanced AI capabilities.

## Authentication
- All endpoints require a unique `workflow_id`
- Session management handled server-side

## Endpoints

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

### 4. Add Data Sources
`POST /api/workflow/{workflow_id}/key-data-sources`
- Submit URLs for content data extraction

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
