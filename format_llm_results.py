"""
Format and display LLM analysis results in a readable format
"""

import json

try:
    with open('llm_analysis_results.json', 'r') as f:
        results = json.load(f)
    
    print("=" * 80)
    print("LLM ANALYSIS RESULTS - FORMATTED")
    print("=" * 80)
    
    sections = [
        ("Key Themes in Recommendations", "recommendation_themes"),
        ("Citation Pattern Analysis", "citation_patterns"),
        ("Discover the 'Why' Deep Dive", "discover_why_analysis"),
        ("Temporal Decline Analysis", "temporal_decline"),
        ("User-Specific Coaching", "user_coaching"),
        ("Impact Text Analysis", "impact_analysis")
    ]
    
    for title, key in sections:
        print(f"\n{'=' * 80}")
        print(f"{title.upper()}")
        print("=" * 80)
        print(results.get(key, "No results available"))
    
    print(f"\n{'=' * 80}")
    print("COST SUMMARY")
    print("=" * 80)
    cost_info = results.get('cost_summary', {})
    print(f"Total tokens used: {cost_info.get('total_tokens', 0):,}")
    print(f"Total cost: ${cost_info.get('total_cost', 0):.4f}")
    print(f"Remaining budget: ${cost_info.get('remaining_budget', 100):.2f}")
    
except FileNotFoundError:
    print("Error: llm_analysis_results.json not found. Please run llm_analysis.py first.")

