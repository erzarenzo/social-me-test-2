"""
Workflow Data Models

This module contains data models for the SocialMe workflow.
"""

class WorkflowData:
    """
    Class to store data collected throughout the workflow steps.
    
    This class maintains the state of the workflow across different steps:
    1. Data Sources
    2. Tone Analysis
    3. Content Strategy
    4. Article Generation
    
    For V2 workflow, the order is reorganized:
    1. Content Strategy
    2. Data Sources (with topic guidance)
    3. Tone Analysis
    4. Article Generation
    """
    
    def __init__(self):
        """Initialize workflow data with empty collections"""
        self.data_sources = []
        self.tone_sources = []
        self.writing_style = {}  # Store writing style analysis data
        self.content_strategy = {}
        self.tone_analysis = {}
        self.crawled_data = {}
        self.generated_article = {}
        self.current_step = 1
        self.is_v2_workflow = False
        self.topic_relevance_data = {}  # Store topic relevance information for v2 workflow
    
    def reset(self):
        """Reset the workflow data to initial state"""
        self.__init__()
    
    def to_dict(self):
        """Convert workflow data to dictionary for serialization"""
        return {
            'data_sources': self.data_sources,
            'tone_sources': self.tone_sources,
            'writing_style': self.writing_style,
            'content_strategy': self.content_strategy,
            'tone_analysis': self.tone_analysis,
            'crawled_data': self.crawled_data,
            'generated_article': self.generated_article,
            'current_step': self.current_step,
            'is_v2_workflow': self.is_v2_workflow,
            'topic_relevance_data': self.topic_relevance_data
        }
    
    @classmethod
    def from_dict(cls, data_dict):
        """Create a WorkflowData instance from a dictionary"""
        workflow = cls()
        workflow.data_sources = data_dict.get('data_sources', [])
        workflow.tone_sources = data_dict.get('tone_sources', [])
        workflow.writing_style = data_dict.get('writing_style', {})
        workflow.content_strategy = data_dict.get('content_strategy', {})
        workflow.tone_analysis = data_dict.get('tone_analysis', {})
        workflow.crawled_data = data_dict.get('crawled_data', {})
        workflow.generated_article = data_dict.get('generated_article', {})
        workflow.current_step = data_dict.get('current_step', 1)
        workflow.is_v2_workflow = data_dict.get('is_v2_workflow', False)
        workflow.topic_relevance_data = data_dict.get('topic_relevance_data', {})
        return workflow
