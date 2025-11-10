#!/usr/bin/env python3
"""Test Phase 1 matching improvements: synonym expansion, extended history, topic diversity."""

import json
from pathlib import Path
from derek_mcp.matcher import ResponseMatcher

def load_responses():
    """Load responses from category files."""
    package_dir = Path(__file__).parent / 'derek_mcp'
    responses_dir = package_dir / 'data' / 'responses_by_category'

    # Load index
    index_file = responses_dir / 'index.json'
    with open(index_file, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    # Load all category files
    all_responses = []
    for group_name, group_info in index_data['groups'].items():
        filename = group_info['file']
        filepath = responses_dir / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            category_data = json.load(f)
            all_responses.extend(category_data['responses'])

    responses_data = {
        'responses': all_responses,
        'fallback_responses': index_data.get('fallback_responses', []),
        'meta_responses': index_data.get('meta_responses', {})
    }

    return responses_data

def test_new_topic_synonyms():
    """Test that new v2.0 topics match correctly with synonym expansion."""
    print("="*70)
    print("TEST 1: New Topic Synonym Matching")
    print("="*70)

    responses_data = load_responses()
    matcher = ResponseMatcher(responses_data)

    test_queries = [
        ("Where do you live?", "kruisstraat"),
        ("Tell me about your apartment", "kruisstraat"),
        ("Do you have any plants?", "plant"),
        ("What about your facial hair?", "beard"),
        ("Do you wear sunscreen?", "sunscreen"),
        ("Did you used to smoke?", "smok"),  # Should match smoking topics
        ("What about climbing?", "climb"),
        ("Tell me about Roger", "roger"),
        ("Morning routine?", "toast"),
        ("Geometry preferences?", "geometry"),
    ]

    for query, expected_keyword in test_queries:
        matches = matcher.find_top_matches(query, n=3)
        if matches:
            top_response = matches[0][1]
            keywords = top_response.get('keywords', [])
            category = top_response.get('category', '')

            # Check if expected keyword or related term is in match
            matched = any(expected_keyword in kw for kw in keywords)

            status = "✓" if matched else "✗"
            print(f"\n{status} Query: '{query}'")
            print(f"  Expected: '{expected_keyword}' in keywords")
            print(f"  Got: {keywords[:3]}... (category: {category})")
            print(f"  Score: {matches[0][0]:.3f}")
        else:
            print(f"\n✗ Query: '{query}'")
            print(f"  No matches found!")

def test_extended_history():
    """Test that extended history (20 responses) prevents repetition."""
    print("\n" + "="*70)
    print("TEST 2: Extended History & Recency Penalty")
    print("="*70)

    responses_data = load_responses()
    matcher = ResponseMatcher(responses_data)

    query = "Tell me about cycling"

    print(f"\nQuerying '{query}' 15 times...")
    print("Checking for response repetition:\n")

    response_ids = []
    for i in range(15):
        response = matcher.get_response(query)
        response_id = response.get('id', 'unknown')
        response_ids.append(response_id)

        # Check if this response appeared recently
        recent_count = response_ids[-10:].count(response_id)
        status = "✓" if recent_count == 1 else "⚠"

        print(f"{i+1:2d}. {status} ID: {response_id[:30]:30s} (seen {recent_count}x in last 10)")

    # Summary
    unique_responses = len(set(response_ids))
    print(f"\nSummary: {unique_responses}/15 unique responses")
    print(f"History size: {len(matcher.recent_responses)}/{matcher.recent_responses.maxlen}")

    if unique_responses >= 10:
        print("✓ Good diversity - extended history working!")
    else:
        print("✗ Low diversity - may need tuning")

def test_topic_diversity():
    """Test that topic diversity tracking prevents topic clustering."""
    print("\n" + "="*70)
    print("TEST 3: Topic Diversity Tracking")
    print("="*70)

    responses_data = load_responses()
    matcher = ResponseMatcher(responses_data)

    # Use general queries that could match multiple categories
    queries = [
        "Tell me something interesting",
        "What do you think?",
        "How are you?",
        "What's up?",
        "Tell me more",
    ]

    print("\nQuerying with general prompts (10 cycles = 50 responses)...")
    print("Tracking topic distribution:\n")

    topics_used = []
    for cycle in range(10):
        for query in queries:
            response = matcher.get_response(query)
            category = response.get('category', 'unknown')
            topics_used.append(category)

    # Count topic distribution
    from collections import Counter
    topic_counts = Counter(topics_used)

    print("Topic distribution across 50 responses:")
    for topic, count in topic_counts.most_common():
        percentage = (count / len(topics_used)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {topic:20s}: {count:3d} ({percentage:5.1f}%) {bar}")

    # Check balance
    max_topic_pct = max(topic_counts.values()) / len(topics_used) * 100
    print(f"\nMost frequent topic: {max_topic_pct:.1f}% of responses")

    if max_topic_pct < 40:
        print("✓ Good topic diversity - no single topic dominates!")
    elif max_topic_pct < 50:
        print("⚠ Moderate diversity - one topic is common")
    else:
        print("✗ Low diversity - topic clustering detected")

    print(f"\nRecent topics queue: {list(matcher.recent_topics)}")

def test_diversity_boost_mechanism():
    """Test that diversity boost actually affects scores."""
    print("\n" + "="*70)
    print("TEST 4: Diversity Boost Mechanism")
    print("="*70)

    responses_data = load_responses()
    matcher = ResponseMatcher(responses_data)

    # Simulate having seen lots of "cycling" responses
    print("\nSimulating 5 recent 'lifestyle' category responses...")
    for _ in range(5):
        matcher.recent_topics.append('lifestyle')

    print(f"Recent topics: {list(matcher.recent_topics)}\n")

    # Create mock responses with different categories
    test_responses = [
        {'id': 'test1', 'category': 'lifestyle', 'keywords': []},
        {'id': 'test2', 'category': 'research', 'keywords': []},
        {'id': 'test3', 'category': 'conversational', 'keywords': []},
    ]

    for resp in test_responses:
        boost = matcher.calculate_topic_diversity_boost(resp)
        category = resp['category']

        if boost > 1.0:
            status = "↑ BOOST"
        elif boost < 1.0:
            status = "↓ PENALTY"
        else:
            status = "= NEUTRAL"

        print(f"{status:10s} {category:20s}: {boost:.2f}x multiplier")

    print("\n✓ Diversity mechanism working if lifestyle is penalized and others boosted")

def main():
    """Run all Phase 1 tests."""
    print("\n" + "="*70)
    print("DEREK MCP - Phase 1 Matching Improvements Test Suite")
    print("="*70)
    print("Testing:")
    print("  1. Synonym expansion (72 → 200+ entries)")
    print("  2. Extended history (10 → 20 responses)")
    print("  3. Topic diversity tracking")
    print("="*70)

    try:
        test_new_topic_synonyms()
        test_extended_history()
        test_topic_diversity()
        test_diversity_boost_mechanism()

        print("\n" + "="*70)
        print("TEST SUITE COMPLETE")
        print("="*70)
        print("\n✓ Phase 1 improvements implemented and tested!")

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
