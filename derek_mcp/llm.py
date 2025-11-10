"""LLM integration for Derek MCP using Ollama

Provides streaming LLM responses with Derek's character profile.
Falls back gracefully if Ollama is unavailable.
"""

import json
import time
from pathlib import Path
from typing import Optional, Iterator, Dict, List, Tuple

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# Ollama configuration
OLLAMA_API_BASE = "http://localhost:11434"
MODEL_NAME = "llama3.2:3b"
GENERATION_TIMEOUT = 30  # seconds
HEALTH_CHECK_TIMEOUT = 2  # seconds


class OllamaClient:
    """Client for interacting with local Ollama API."""

    def __init__(self, model_name: str = MODEL_NAME, api_base: str = OLLAMA_API_BASE):
        """Initialize Ollama client.

        Args:
            model_name: Name of the Ollama model to use
            api_base: Base URL for Ollama API
        """
        self.model_name = model_name
        self.api_base = api_base
        self.generate_url = f"{api_base}/api/generate"
        self.tags_url = f"{api_base}/api/tags"

        # Load character profile
        self.character_profile = self._load_character_profile()

    def _load_character_profile(self) -> str:
        """Load condensed character profile from data directory.

        Returns:
            Character profile text
        """
        package_dir = Path(__file__).parent

        # Load final v3 profile (single source of truth)
        profile_path = package_dir / 'data' / 'character_profile.md'

        if profile_path.exists():
            with open(profile_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Fallback minimal profile if file not found
            print("Warning: Character profile file not found, using minimal profile.")
            return """Derek van Tilborg - PhD candidate in Molecular ML at TU/e.
Pedantic, obsessively correct, uses "ACTUALLY" frequently.
Towers over supervisor Francesca by 40cm. Tracks everything with metrics.
Cites papers (van Tilborg et al. 2022) or fake ones (I.M. Wright et al.)."""

    def check_health(self) -> Tuple[bool, Optional[str]]:
        """Check if Ollama is running and model is available.

        Returns:
            Tuple of (is_healthy, error_message)
        """
        if not REQUESTS_AVAILABLE:
            return False, "requests library not installed"

        try:
            # Check if Ollama API is responding
            response = requests.get(self.tags_url, timeout=HEALTH_CHECK_TIMEOUT)

            if response.status_code != 200:
                return False, f"Ollama API returned status {response.status_code}"

            # Check if our model is available
            data = response.json()
            models = data.get('models', [])
            model_names = [m.get('name', '') for m in models]

            if self.model_name not in model_names:
                return False, f"Model '{self.model_name}' not found. Available: {model_names}"

            return True, None

        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to Ollama (is it running?)"
        except requests.exceptions.Timeout:
            return False, "Ollama health check timed out"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def _build_prompt(self, user_input: str, matched_responses: List[Dict],
                     suggested_sass: int) -> str:
        """Build prompt for LLM with character context from profile.

        Args:
            user_input: User's message
            matched_responses: Top matched keyword responses
            suggested_sass: Suggested sass level from keyword matcher

        Returns:
            Formatted prompt string
        """
        # Extract context from matched responses (phrases, topics, keywords)
        matched_context = []
        matched_topics = set()

        for resp in matched_responses[:3]:  # Use top 3 matches
            # Get response text
            response_text = resp.get('response', '')
            if response_text:
                matched_context.append(response_text)

            # Get category/topic
            category = resp.get('category', '')
            if category:
                matched_topics.add(category)

            # Get keywords
            keywords = resp.get('keywords', [])
            if keywords:
                matched_topics.update(keywords[:3])  # Top 3 keywords

        context_text = "\n".join([f"  - {ctx[:100]}..." for ctx in matched_context]) if matched_context else "  (No specific context)"
        topics_text = ", ".join(list(matched_topics)[:5]) if matched_topics else "general"

        # Build prompt using character profile
        prompt = f"""You are Derek van Tilborg. Use the character profile you've been given.

IMPORTANT INSTRUCTIONS:
1. **Use matched response context strongly** - The responses below are highly relevant to the user's query
2. **Vary your speech patterns** - Don't always use "ACTUALLY", rotate openings and certainty markers
3. **Balance topics** - Don't default to cycling; you have many dimensions
4. **Maintain zero self-awareness** - You don't realize how pedantic you sound
5. **Quantify precisely** - Exact numbers, percentages, statistics
6. **Stay in character** - Pedantic, metric-obsessed, confidently wrong outside expertise

MATCHED RESPONSE CONTEXT (use these as strong guidance):
Topics: {topics_text}
Suggested sass level: {suggested_sass}/10 (may adjust UP if warranted)

Relevant responses from your knowledge base:
{context_text}

USER INPUT: {user_input}

RESPONSE GUIDELINES:
- 1-3 sentences maximum
- Incorporate elements from matched responses naturally
- Use Derek's characteristic speech patterns (varied, not repetitive)
- Quantify with exact measurements when relevant
- Occasionally cite papers (real: van Tilborg et al. 2022/2024, or fake: rotate through Wright, Knowitall, Obvious, Correct, Smart, Pedantic et al.)
- Maintain character consistency with profile

Generate Derek's response:"""
        return prompt

    def generate_streaming(self, user_input: str, matched_responses: List[Dict], suggested_sass: int = 5) -> Iterator[str]:
        """Generate streaming response from LLM.

        Args:
            user_input: User's message
            matched_responses: Top matched keyword responses for context
            suggested_sass: Suggested sass level from matcher (0-10)

        Yields:
            Response tokens as they're generated

        Raises:
            RuntimeError: If LLM generation fails
        """
        if not REQUESTS_AVAILABLE:
            raise RuntimeError("requests library not installed")

        # Build the prompt
        prompt = self._build_prompt(user_input, matched_responses, suggested_sass)

        # Prepare request payload with system context (character profile)
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": self.character_profile,  # Full profile as system context
            "stream": True,
            "options": {
                "temperature": 0.8,  # Creative but not too wild
                "top_p": 0.9,
                "top_k": 40,
                "num_predict": 200,  # Max tokens (1-3 sentences)
                "stop": ["\n\n", "User:", "Assistant:"],  # Stop sequences
            }
        }

        try:
            # Make streaming request
            response = requests.post(
                self.generate_url,
                json=payload,
                stream=True,
                timeout=GENERATION_TIMEOUT
            )

            if response.status_code != 200:
                raise RuntimeError(f"Ollama API error: {response.status_code}")

            # Stream the response
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        token = chunk.get('response', '')

                        if token:
                            yield token

                        # Check if generation is done
                        if chunk.get('done', False):
                            break

                    except json.JSONDecodeError:
                        continue  # Skip malformed lines

        except requests.exceptions.Timeout:
            raise RuntimeError("LLM generation timed out")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Lost connection to Ollama")
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {str(e)}")

    def generate(self, user_input: str, matched_responses: List[Dict],
                suggested_sass: int = 5) -> str:
        """Generate non-streaming response (convenience method).

        Args:
            user_input: User's message
            matched_responses: Top matched keyword responses
            suggested_sass: Suggested sass level

        Returns:
            Complete generated response

        Raises:
            RuntimeError: If generation fails
        """
        tokens = []
        for token in self.generate_streaming(user_input, matched_responses, suggested_sass):
            tokens.append(token)
        return ''.join(tokens)


def ensure_ollama() -> Tuple[bool, Optional[str], Optional[OllamaClient]]:
    """Check if Ollama is available and ready to use.

    Returns:
        Tuple of (is_available, status_message, client_or_none)
    """
    if not REQUESTS_AVAILABLE:
        return False, "requests library not installed (pip install requests)", None

    client = OllamaClient()
    is_healthy, error_msg = client.check_health()

    if is_healthy:
        return True, f"LLM ready (model: {MODEL_NAME})", client
    else:
        return False, f"Ollama not available: {error_msg}", None


def get_friendly_status_message(is_available: bool, status_msg: str) -> str:
    """Get user-friendly status message.

    Args:
        is_available: Whether Ollama is available
        status_msg: Technical status message

    Returns:
        Friendly formatted message
    """
    if is_available:
        return f"🤖 Derek is running in LLM-enhanced mode ({status_msg})"
    else:
        return f"📚 Derek is running in keyword-only mode ({status_msg})"


# Quick test function
def test_ollama():
    """Test Ollama connection and model."""
    print("Testing Ollama setup...")
    print(f"API: {OLLAMA_API_BASE}")
    print(f"Model: {MODEL_NAME}")
    print()

    is_available, msg, client = ensure_ollama()
    print(f"Status: {get_friendly_status_message(is_available, msg)}")

    if is_available and client:
        print("\nTesting generation...")
        try:
            test_input = "Tell me about height"
            matched = [{"response": "I tower over Francesca by 40 centimeters", "sass_level": 7}]

            print(f"Input: {test_input}")
            print("Response: ", end='', flush=True)

            for token in client.generate_streaming(test_input, matched, suggested_sass=7):
                print(token, end='', flush=True)
            print("\n")
            print("✓ Test successful!")

        except Exception as e:
            print(f"\n✗ Test failed: {e}")

    return is_available


if __name__ == '__main__':
    test_ollama()
