from quantum_universal_crawler import TopicRelevanceScorer

def enhance_topic_scorer():
    """
    Enhances the TopicRelevanceScorer class with improved relevance detection.
    Use this to modify the TopicRelevanceScorer inside your crawler file.
    """
    # Improved score_paragraph method
    def improved_score_paragraph(self, text):
        """Improved scoring with phrase matching and weighted keywords"""
        if not text or len(text) < 20:
            return 0.0
            
        text_lower = text.lower()
        words = set(re.findall(r'\w+', text_lower))
        
        # Direct topic phrase matching (much stronger signal)
        if self.topic in text_lower:
            base_score = 0.8  # Increased from 0.7
        else:
            # Check for partial phrase matches
            topic_parts = self.topic.split()
            if len(topic_parts) > 1:
                # For multi-word topics, check if most parts are present
                matches = sum(1 for part in topic_parts if part in text_lower)
                if matches / len(topic_parts) >= 0.7:  # 70% of topic words present
                    base_score = 0.6
                else:
                    base_score = 0.0
            else:
                base_score = 0.0
        
        # Count keyword matches with weighting for important terms
        matches = words.intersection(self.keywords)
        
        # Create importance weights for keywords
        keyword_importance = {}
        for word in self.keywords:
            # Words from the original topic get higher weight
            if word in self.topic.split():
                keyword_importance[word] = 2.0
            else:
                keyword_importance[word] = 1.0
                
        # Calculate weighted match score
        total_weight = sum(keyword_importance.get(word, 1.0) for word in self.keywords)
        if total_weight > 0:
            weighted_matches = sum(keyword_importance.get(word, 1.0) for word in matches)
            match_score = weighted_matches / total_weight
        else:
            match_score = 0.0
        
        # Calculate density (matches per word)
        word_count = len(text.split())
        density = len(matches) / (word_count or 1)
        density_score = min(1.0, density * 25)  # Increased multiplier for better sensitivity
        
        # Combined score with adjusted weights
        final_score = (base_score * 0.5) + (match_score * 0.3) + (density_score * 0.2)
        return min(1.0, final_score)  # Ensure 0.0-1.0 range
    
    return improved_score_paragraph

# Instructions for integrating this into your quantum_universal_crawler.py file
print("To improve topic relevance, update the score_paragraph method in the TopicRelevanceScorer class")
print("Find the method in your code and replace with the improved version")
