#!/usr/bin/env python3
"""Generate statistics about keywords in responses.json."""

import json
from collections import defaultdict
from pathlib import Path


def generate_keyword_stats():
    """Analyze and display keyword statistics from responses.json."""
    
    responses_file = Path("derek_mcp/data/responses.json")
    
    if not responses_file.exists():
        print(f"❌ Error: {responses_file} not found")
        return
    
    with open(responses_file, 'r') as f:
        data = json.load(f)
    
    # Count keywords by category
    category_stats = defaultdict(list)
    
    for r in data['responses']:
        category = r.get('category', 'unknown')
        keyword_count = len(r.get('keywords', []))
        category_stats[category].append(keyword_count)
    
    # Display category-wise statistics
    print('=' * 85)
    print('KEYWORD STATISTICS BY CATEGORY')
    print('=' * 85)
    print(f'{"Category":<25} | {"Avg":>5} | {"Min":>3} | {"Max":>3} | {"Responses":>9}')
    print('-' * 85)
    
    for category in sorted(category_stats.keys()):
        counts = category_stats[category]
        avg = sum(counts) / len(counts)
        print(f'{category:<25} | {avg:5.1f} | {min(counts):3} | {max(counts):3} | {len(counts):9}')
    
    # Overall stats
    all_counts = [len(r.get('keywords', [])) for r in data['responses']]
    total_responses = len(all_counts)
    avg_keywords = sum(all_counts) / total_responses if total_responses > 0 else 0
    
    print('=' * 85)
    print(f'OVERALL: {total_responses} responses | Average: {avg_keywords:.1f} keywords per response')
    print('=' * 85)
    
    # Additional insights
    print(f'\nKeyword Distribution:')
    print(f'  • Minimum: {min(all_counts)} keywords')
    print(f'  • Maximum: {max(all_counts)} keywords')
    print(f'  • Median: {sorted(all_counts)[len(all_counts)//2]} keywords')
    
    # Count responses by keyword range
    ranges = {
        '1-5': sum(1 for c in all_counts if 1 <= c <= 5),
        '6-10': sum(1 for c in all_counts if 6 <= c <= 10),
        '11-15': sum(1 for c in all_counts if 11 <= c <= 15),
        '16-20': sum(1 for c in all_counts if 16 <= c <= 20),
        '21+': sum(1 for c in all_counts if c >= 21),
    }
    
    print(f'\nKeyword Range Distribution:')
    for range_name, count in ranges.items():
        percentage = (count / total_responses * 100) if total_responses > 0 else 0
        bar = '█' * int(percentage / 2)
        print(f'  • {range_name:6} keywords: {count:3} responses ({percentage:5.1f}%) {bar}')
    
    # Find responses with fewest/most keywords
    print(f'\nResponses with Fewest Keywords:')
    sorted_responses = sorted(data['responses'], key=lambda r: len(r.get('keywords', [])))
    for r in sorted_responses[:3]:
        kw_count = len(r.get('keywords', []))
        print(f'  • {r["id"]:<20} ({r["category"]:<20}) - {kw_count} keywords')
    
    print(f'\nResponses with Most Keywords:')
    for r in sorted_responses[-3:]:
        kw_count = len(r.get('keywords', []))
        print(f'  • {r["id"]:<20} ({r["category"]:<20}) - {kw_count} keywords')
    
    # Meta stats
    print(f'\nDatabase Stats:')
    print(f'  • Standard responses: {len(data["responses"])}')
    print(f'  • Fallback responses: {len(data.get("fallback_responses", []))}')
    print(f'  • Meta responses: {len(data.get("meta_responses", {}))}')
    print(f'  • Total categories: {len(category_stats)}')
    
    return {
        'total_responses': total_responses,
        'avg_keywords': avg_keywords,
        'category_stats': dict(category_stats),
    }


if __name__ == '__main__':
    generate_keyword_stats()
