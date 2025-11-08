"""Response matching logic for Derek MCP

Enhanced keyword-based matching with:
- Synonym expansion
- Stemming for partial matches
- Phrase detection
- Weighted keyword scoring
- Top-N selection with recency penalty
"""

import math
import random
import re
from collections import Counter, deque
from typing import Dict, List, Optional, Tuple


# ============================================================================
# SYNONYM DICTIONARY
# ============================================================================

SYNONYMS = {
    # Cycling/Exercise
    'bike': ['bicycle', 'cycling', 'cycle', 'ride', 'cyclist'],
    'cycling': ['bike', 'bicycle', 'ride', 'cyclist'],
    'ride': ['cycling', 'bike', 'bicycle'],
    'exercise': ['workout', 'fitness', 'train', 'gym'],
    'run': ['running', 'runner', 'jog', 'marathon'],
    
    # Intelligence/Knowledge
    'smart': ['intelligent', 'clever', 'bright', 'genius', 'brilliant'],
    'stupid': ['dumb', 'idiot', 'foolish', 'ignorant'],
    'intelligent': ['smart', 'clever', 'bright'],
    'know': ['knowledge', 'understand', 'comprehend', 'aware'],
    
    # Academia
    'phd': ['doctorate', 'dissertation', 'thesis', 'doctoral'],
    'thesis': ['dissertation', 'phd', 'research'],
    'paper': ['publication', 'manuscript', 'article'],
    'research': ['study', 'investigation', 'analysis'],
    
    # Molecules/Chemistry
    'molecule': ['molecular', 'compound', 'chemical', 'structure'],
    'molecular': ['molecule', 'compound', 'chemistry'],
    'drug': ['compound', 'molecule', 'pharmaceutical'],
    'synthesis': ['synthesize', 'reaction', 'chemical'],
    
    # AI/ML
    'ai': ['artificial intelligence', 'machine learning', 'ml', 'neural network'],
    'model': ['neural network', 'algorithm', 'ml'],
    'train': ['training', 'learning', 'optimization'],
    
    # Food/Nutrition
    'food': ['eat', 'meal', 'nutrition', 'diet'],
    'lunch': ['meal', 'eat', 'dinner', 'breakfast'],
    
    # Work/Job
    'work': ['job', 'research', 'career', 'employment'],
    'job': ['work', 'position', 'employment', 'career'],
    
    # Personality
    'pedantic': ['pedantry', 'nitpick', 'correct', 'precise'],
    'correct': ['right', 'accurate', 'precise', 'fix'],
    'wrong': ['incorrect', 'mistake', 'error', 'false'],
    
    # General
    'good': ['great', 'excellent', 'nice', 'wonderful'],
    'bad': ['terrible', 'awful', 'poor', 'negative'],
    'think': ['believe', 'consider', 'opinion', 'thought'],
    'say': ['tell', 'speak', 'talk', 'mention'],
}


# ============================================================================
# TEXT PROCESSING FUNCTIONS
# ============================================================================

def simple_stem(word: str) -> str:
    """Apply simple suffix stripping for stemming.
    
    Args:
        word: Word to stem
        
    Returns:
        Stemmed word
    """
    if len(word) <= 3:
        return word
    
    suffixes = ['ings', 'ing', 'ies', 'ied', 'ed', 'es', 's', 'ly', 'er', 'est']
    
    for suffix in suffixes:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if len(stem) >= 3:  # Keep reasonable stem length
                return stem
    
    return word


def tokenize(text: str) -> set:
    """Convert text to lowercase tokens, removing punctuation.

    Args:
        text: Input text to tokenize

    Returns:
        Set of lowercase word tokens
    """
    tokens = re.findall(r'\b\w+\b', text.lower())
    return set(tokens)


def enhanced_tokenize(text: str) -> set:
    """Tokenize with stems and synonym expansion.
    
    Args:
        text: Input text
        
    Returns:
        Enhanced set of tokens including stems and synonyms
    """
    tokens = tokenize(text)
    enhanced = set(tokens)
    
    # Add stems for partial matching
    for token in tokens:
        stem = simple_stem(token)
        if stem != token:
            enhanced.add(stem)
    
    # Add synonyms for semantic matching
    for token in tokens:
        if token in SYNONYMS:
            # Add each synonym word
            for syn_phrase in SYNONYMS[token]:
                enhanced.update(tokenize(syn_phrase))
    
    return enhanced


def extract_phrases(text: str) -> set:
    """Extract multi-word phrases from text.
    
    Args:
        text: Input text
        
    Returns:
        Set of 2-3 word phrases
    """
    phrases = set()
    text_lower = text.lower()
    
    # Common 2-3 word technical phrases
    phrase_patterns = [
        r'\b(machine learning)\b',
        r'\b(artificial intelligence)\b',
        r'\b(neural network)\b',
        r'\b(active learning)\b',
        r'\b(drug discovery)\b',
        r'\b(molecular property)\b',
        r'\b(phd candidate)\b',
        r'\b(peer review)\b',
        r'\b(out of distribution)\b',
        r'\b(karman line)\b',
    ]
    
    for pattern in phrase_patterns:
        matches = re.findall(pattern, text_lower)
        phrases.update(matches)
    
    return phrases


# ============================================================================
# SCORING FUNCTIONS
# ============================================================================

def calculate_keyword_weights(responses: List[Dict]) -> Dict[str, float]:
    """Calculate IDF-style weights for keywords based on rarity.
    
    Args:
        responses: List of all response dictionaries
        
    Returns:
        Dictionary mapping keywords to weight scores
    """
    # Count keyword frequencies across all responses
    keyword_counts = Counter()
    for response in responses:
        keywords = response.get('keywords', [])
        for kw in keywords:
            keyword_counts[kw.lower()] += 1
    
    total_responses = len(responses)
    weights = {}
    
    for keyword, count in keyword_counts.items():
        # Inverse document frequency
        idf = math.log(total_responses / (1 + count))
        weights[keyword] = max(0.1, idf)  # Minimum weight of 0.1
    
    return weights


def score_response(user_tokens: set, user_phrases: set, 
                   response: Dict, keyword_weights: Dict[str, float]) -> float:
    """Score a response based on enhanced keyword matching.
    
    Args:
        user_tokens: Enhanced tokens from user input
        user_phrases: Extracted phrases from user input
        response: Response dictionary with keywords
        keyword_weights: Keyword importance weights
        
    Returns:
        Weighted match score
    """
    keywords = set(kw.lower() for kw in response.get('keywords', []))
    
    if not keywords:
        return 0.0
    
    score = 0.0
    matched_keywords = 0
    
    # Score keyword matches with weights
    for keyword in keywords:
        weight = keyword_weights.get(keyword, 0.5)
        
        # Exact match (highest score)
        if keyword in user_tokens:
            score += weight * 1.0
            matched_keywords += 1
        else:
            # Check for stem match
            keyword_stem = simple_stem(keyword)
            for token in user_tokens:
                if simple_stem(token) == keyword_stem:
                    score += weight * 0.7  # Partial match score
                    matched_keywords += 1
                    break
    
    # Bonus for phrase matches
    for phrase in user_phrases:
        phrase_tokens = tokenize(phrase)
        if phrase_tokens.issubset(keywords):
            score += 0.5  # Phrase bonus
    
    # Normalize by number of keywords (avoid bias toward responses with many keywords)
    if matched_keywords > 0:
        normalized_score = score / len(keywords)
        return normalized_score
    
    return 0.0


def apply_recency_penalty(scored_responses: List[Tuple[float, Dict]], 
                         recent_ids: deque, 
                         recency_window: int = 5) -> List[Tuple[float, Dict]]:
    """Apply penalty to recently used responses.
    
    Args:
        scored_responses: List of (score, response) tuples
        recent_ids: Deque of recently used response IDs
        recency_window: How many recent responses to penalize
        
    Returns:
        List of (adjusted_score, response) tuples
    """
    adjusted = []
    
    for score, response in scored_responses:
        response_id = response.get('id', '')
        
        # Apply penalty if response was used recently
        if response_id in recent_ids:
            # Find position in recent history (0 = most recent)
            position = list(recent_ids).index(response_id)
            # Stronger penalty for more recent responses
            penalty = 1.0 - (0.7 * (1.0 - position / recency_window))
            adjusted_score = score * penalty
        else:
            adjusted_score = score
        
        adjusted.append((adjusted_score, response))
    
    return adjusted


# ============================================================================
# TEMPLATE APPLICATION
# ============================================================================

def apply_template(response_text: str, user_input: str,
                   template_vars: Optional[Dict[str, str]] = None) -> str:
    """Apply template variables to response text.

    Supports:
    - {user_phrase}: Extracts a key phrase from user input
    - {user_input}: Full user input
    - Custom variables from template_vars dict

    Args:
        response_text: Response text with optional template variables
        user_input: Original user input
        template_vars: Optional additional template variables

    Returns:
        Response text with variables substituted
    """
    vars_dict = template_vars or {}
    vars_dict['user_input'] = user_input

    # Extract a key phrase (longest meaningful word)
    tokens = re.findall(r'\b\w{4,}\b', user_input)
    if tokens:
        vars_dict['user_phrase'] = max(tokens, key=len)
    else:
        vars_dict['user_phrase'] = user_input[:30]

    # Apply substitutions
    result = response_text
    for key, value in vars_dict.items():
        placeholder = '{' + key + '}'
        if placeholder in result:
            result = result.replace(placeholder, value)

    return result


# ============================================================================
# MAIN MATCHER CLASS
# ============================================================================

class ResponseMatcher:
    """Enhanced response matcher with top-N selection and recency penalty."""

    def __init__(self, responses_data: Dict):
        """Initialize matcher with responses data.

        Args:
            responses_data: Loaded JSON responses data
        """
        self.responses = responses_data.get('responses', [])
        self.fallback_responses = responses_data.get('fallback_responses', [])
        self.meta_responses = responses_data.get('meta_responses', {})
        
        # Calculate keyword weights once at initialization
        self.keyword_weights = calculate_keyword_weights(self.responses)
        
        # Track recently used responses
        self.recent_responses = deque(maxlen=10)  # Keep last 10 responses
        
        # Configuration
        self.threshold = 0.2  # Lower threshold for better matching
        self.top_n = 5  # Consider top 5 matches
        self.recency_window = 5  # Penalize last 5 responses

    def find_top_matches(self, user_input: str, n: int = 5) -> List[Tuple[float, Dict]]:
        """Find top N matching responses for user input.

        Args:
            user_input: User's text input
            n: Number of top matches to return

        Returns:
            List of (score, response) tuples, sorted by score descending
        """
        if not user_input.strip():
            return []
        
        # Enhanced tokenization
        user_tokens = enhanced_tokenize(user_input)
        user_phrases = extract_phrases(user_input)
        
        # Score all responses
        scored_responses = []
        for response in self.responses:
            score = score_response(user_tokens, user_phrases, response, 
                                 self.keyword_weights)
            if score >= self.threshold:
                scored_responses.append((score, response))
        
        if not scored_responses:
            return []
        
        # Sort by score
        scored_responses.sort(reverse=True, key=lambda x: x[0])
        
        # Apply recency penalty
        scored_responses = apply_recency_penalty(
            scored_responses[:n*2],  # Consider more candidates for penalty
            self.recent_responses,
            self.recency_window
        )
        
        # Re-sort after penalty and take top N
        scored_responses.sort(reverse=True, key=lambda x: x[0])
        return scored_responses[:n]

    def get_response(self, user_input: str, response_type: str = 'standard') -> Dict:
        """Get appropriate response for user input.

        Args:
            user_input: User's text input
            response_type: Type of response ('standard', 'greeting', 'goodbye', 'confusion')

        Returns:
            Response dictionary with 'response', optional 'follow_up', and 'sass_level'
        """
        # Handle meta responses
        if response_type != 'standard':
            meta_response = self.meta_responses.get(response_type, "")
            return {
                'response': meta_response,
                'sass_level': 5
            }

        # Try enhanced matching
        top_matches = self.find_top_matches(user_input, n=self.top_n)

        if top_matches:
            # Select randomly from top matches (weighted by score)
            scores = [score for score, _ in top_matches]
            responses = [resp for _, resp in top_matches]
            
            # Weighted random selection
            total_score = sum(scores)
            weights = [s / total_score for s in scores]
            
            selected_response = random.choices(responses, weights=weights, k=1)[0]
            
            # Track this response
            response_id = selected_response.get('id', '')
            if response_id:
                self.recent_responses.append(response_id)
            
            # Apply template variables
            response_dict = selected_response.copy()
            response_dict['response'] = apply_template(
                response_dict['response'],
                user_input
            )
            if 'follow_up' in response_dict:
                response_dict['follow_up'] = apply_template(
                    response_dict['follow_up'],
                    user_input
                )
            return response_dict

        # Fall back to random fallback response
        if not self.fallback_responses:
            return {
                "response": "*beep boop* Error: No fallback responses loaded. This is meta-embarrassing.",
                "sass_level": 5
            }
        
        return random.choice(self.fallback_responses)
