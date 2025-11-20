"""
LLM-Powered Analysis using OpenAI API
Extracting deeper insights from text data (recommendations, impacts, citations)
"""

import pandas as pd
import numpy as np
import json
import os
from openai import OpenAI
from collections import Counter, defaultdict
import time
import warnings
warnings.filterwarnings('ignore')

# Initialize OpenAI client
# API key should be set as environment variable: OPENAI_API_KEY
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it before running this script.")
client = OpenAI(api_key=api_key)

# Cost tracking
total_tokens_used = 0
total_cost = 0

def estimate_cost(prompt_tokens, completion_tokens, model="gpt-3.5-turbo"):
    """Estimate cost based on token usage"""
    # Pricing as of 2024 (approximate)
    # gpt-3.5-turbo: $0.0005/1k input, $0.0015/1k output
    # gpt-4: $0.03/1k input, $0.06/1k output
    if "gpt-4" in model.lower():
        input_cost = (prompt_tokens / 1000) * 0.03
        output_cost = (completion_tokens / 1000) * 0.06
    else:
        input_cost = (prompt_tokens / 1000) * 0.0005
        output_cost = (completion_tokens / 1000) * 0.0015
    return input_cost + output_cost

def call_openai(prompt, model="gpt-3.5-turbo", max_tokens=500, temperature=0.3):
    """Call OpenAI API with error handling and cost tracking"""
    global total_tokens_used, total_cost
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        
        total_tokens_used += total_tokens
        cost = estimate_cost(prompt_tokens, completion_tokens, model)
        total_cost += cost
        
        return response.choices[0].message.content.strip(), total_tokens, cost
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return None, 0, 0

print("=" * 80)
print("LLM-POWERED ANALYSIS")
print("=" * 80)
print()

# Load and prepare data
print("Loading data...")
recording_df = pd.read_csv('ds_takehome_recording.csv')
scoring_df = pd.read_csv('ds_takehome_scoring_metadata.csv')

# Parse JSON metadata
def parse_metadata(row):
    try:
        metadata = json.loads(row['scoringMetadata'])
        return {
            'impact': metadata.get('impact', ''),
            'recommendation': metadata.get('recommendation', ''),
            'raw': metadata.get('raw', ''),
            'citations': metadata.get('thinkingWithCitation', {}).get('citations', [])
        }
    except:
        return {
            'impact': '',
            'recommendation': '',
            'raw': '',
            'citations': []
        }

scoring_df['parsed_metadata'] = scoring_df.apply(parse_metadata, axis=1)
scoring_df['impact_text'] = scoring_df['parsed_metadata'].apply(lambda x: x['impact'])
scoring_df['recommendation_text'] = scoring_df['parsed_metadata'].apply(lambda x: x['recommendation'])
scoring_df['num_citations'] = scoring_df['parsed_metadata'].apply(lambda x: len(x['citations']))

# Merge with outcomes
recording_df['dateCreated'] = pd.to_datetime(recording_df['dateCreated'])
scoring_df['recordingdate'] = pd.to_datetime(scoring_df['recordingdate'])
merged_df = recording_df.merge(scoring_df, on='recordingid', how='inner', suffixes=('_recording', '_scoring'))
merged_df['score'] = pd.to_numeric(merged_df['score'], errors='coerce')

print(f"Loaded {len(merged_df)} merged records")
print()

# ============================================================================
# ANALYSIS 1: Extract Key Themes from Recommendations
# ============================================================================
print("=" * 80)
print("ANALYSIS 1: Key Themes in Recommendations")
print("=" * 80)

# Sample recommendations for high vs low scores
high_score_recs = merged_df[merged_df['score'] >= 4]['recommendation_text'].dropna().tolist()[:50]
low_score_recs = merged_df[merged_df['score'] <= 2]['recommendation_text'].dropna().tolist()[:50]

prompt1 = f"""Analyze these sales coaching recommendations and identify the top 5 themes/categories.

HIGH SCORE RECOMMENDATIONS (score 4-5):
{chr(10).join([f"- {rec[:200]}" for rec in high_score_recs[:20]])}

LOW SCORE RECOMMENDATIONS (score 1-2):
{chr(10).join([f"- {rec[:200]}" for rec in low_score_recs[:20]])}

For each theme, provide:
1. Theme name
2. Brief description
3. Whether it's more common in high or low scores
4. Key action items

Format as a structured list."""

print("Analyzing recommendation themes...")
result1, tokens1, cost1 = call_openai(prompt1, model="gpt-3.5-turbo", max_tokens=800)
print(result1)
print(f"\nTokens used: {tokens1}, Estimated cost: ${cost1:.4f}\n")

# ============================================================================
# ANALYSIS 2: Citation Pattern Analysis
# ============================================================================
print("=" * 80)
print("ANALYSIS 2: Citation Pattern Analysis")
print("=" * 80)

# Extract citations from high and low scoring evaluations
high_score_citations = []
low_score_citations = []

for idx, row in merged_df.iterrows():
    citations = row['parsed_metadata']['citations']
    if citations:
        quotes = [c.get('quote', '') for c in citations if c.get('quote')]
        if row['score'] >= 4 and len(high_score_citations) < 30:
            high_score_citations.extend(quotes[:3])  # Sample 3 per record
        elif row['score'] <= 2 and len(low_score_citations) < 30:
            low_score_citations.extend(quotes[:3])

prompt2 = f"""Analyze these actual quotes from sales calls and identify patterns.

QUOTES FROM HIGH-SCORING CALLS (score 4-5):
{chr(10).join([f"- {quote[:150]}" for quote in high_score_citations[:20]])}

QUOTES FROM LOW-SCORING CALLS (score 1-2):
{chr(10).join([f"- {quote[:150]}" for quote in low_score_citations[:20]])}

Identify:
1. Language patterns that distinguish high vs low scores
2. Specific phrases or approaches that work well
3. Common mistakes or problematic language
4. Actionable insights for sales reps

Provide specific examples."""

print("Analyzing citation patterns...")
result2, tokens2, cost2 = call_openai(prompt2, model="gpt-3.5-turbo", max_tokens=800)
print(result2)
print(f"\nTokens used: {tokens2}, Estimated cost: ${cost2:.4f}\n")

# ============================================================================
# ANALYSIS 3: Skill-Specific Deep Dive
# ============================================================================
print("=" * 80)
print("ANALYSIS 3: Skill-Specific Deep Dive - 'Discover the Why'")
print("=" * 80)

# Focus on the weakest skill
discover_why = merged_df[merged_df['skillName'] == 'Discover the "Why"'].copy()
discover_why_high = discover_why[discover_why['score'] >= 4]
discover_why_low = discover_why[discover_why['score'] <= 2]

high_impacts = discover_why_high['impact_text'].dropna().tolist()[:15]
low_impacts = discover_why_low['impact_text'].dropna().tolist()[:15]
high_recs = discover_why_high['recommendation_text'].dropna().tolist()[:15]

prompt3 = f"""The skill "Discover the Why" has the lowest average score (2.63/5.0) across all reps.

HIGH SCORE IMPACTS (what worked):
{chr(10).join([f"- {impact}" for impact in high_impacts[:10]])}

LOW SCORE IMPACTS (what didn't work):
{chr(10).join([f"- {impact}" for impact in low_impacts[:10]])}

RECOMMENDATIONS FOR IMPROVEMENT:
{chr(10).join([f"- {rec}" for rec in high_recs[:10]])}

Based on this analysis, provide:
1. The 3 most critical gaps preventing reps from excelling at discovery
2. Specific, actionable coaching recommendations
3. Example questions or phrases that would improve scores
4. A prioritized action plan for training

Be specific and practical."""

print("Analyzing 'Discover the Why' skill...")
result3, tokens3, cost3 = call_openai(prompt3, model="gpt-3.5-turbo", max_tokens=1000)
print(result3)
print(f"\nTokens used: {tokens3}, Estimated cost: ${cost3:.4f}\n")

# ============================================================================
# ANALYSIS 4: Temporal Decline Analysis
# ============================================================================
print("=" * 80)
print("ANALYSIS 4: Temporal Decline Root Cause Analysis")
print("=" * 80)

# Compare early vs late period recommendations
merged_df['date'] = merged_df['recordingdate'].dt.date
early_period = merged_df[merged_df['date'] <= pd.to_datetime('2025-08-15').date()]
late_period = merged_df[merged_df['date'] >= pd.to_datetime('2025-09-15').date()]

early_recs = early_period['recommendation_text'].dropna().tolist()[:20]
late_recs = late_period['recommendation_text'].dropna().tolist()[:20]
early_impacts = early_period['impact_text'].dropna().tolist()[:15]
late_impacts = late_period['impact_text'].dropna().tolist()[:15]

prompt4 = f"""Performance declined significantly: win rate dropped from 64% to 40% and skill scores declined 15% over time.

EARLY PERIOD RECOMMENDATIONS (Aug 6-15, higher performance):
{chr(10).join([f"- {rec[:180]}" for rec in early_recs[:15]])}

LATE PERIOD RECOMMENDATIONS (Sep 15-28, lower performance):
{chr(10).join([f"- {rec[:180]}" for rec in late_recs[:15]])}

EARLY PERIOD IMPACTS:
{chr(10).join([f"- {impact[:150]}" for impact in early_impacts[:10]])}

LATE PERIOD IMPACTS:
{chr(10).join([f"- {impact[:150]}" for impact in late_impacts[:10]])}

Analyze what changed and provide:
1. Key differences in recommendations between periods
2. Potential root causes for the decline
3. Specific hypotheses to investigate
4. Immediate intervention recommendations

Focus on actionable insights."""

print("Analyzing temporal decline...")
result4, tokens4, cost4 = call_openai(prompt4, model="gpt-3.5-turbo", max_tokens=1000)
print(result4)
print(f"\nTokens used: {tokens4}, Estimated cost: ${cost4:.4f}\n")

# ============================================================================
# ANALYSIS 5: User-Specific Coaching Recommendations
# ============================================================================
print("=" * 80)
print("ANALYSIS 5: User-Specific Coaching Recommendations")
print("=" * 80)

# Analyze top and bottom performers
top_user = 'WQwSd6yvYtevHdM8h6sGlHwkV1n2'  # 51% win rate
bottom_user = 'Zbd0Y2ic8zVKmi7gOK2p8jEiiZh2'  # 22% win rate

top_user_data = merged_df[merged_df['userId_recording'] == top_user]
bottom_user_data = merged_df[merged_df['userId_recording'] == bottom_user]

top_recs = top_user_data['recommendation_text'].dropna().tolist()[:20]
bottom_recs = bottom_user_data['recommendation_text'].dropna().tolist()[:20]

# Get skill scores
top_skills = top_user_data.groupby('skillName')['score'].mean().to_dict()
bottom_skills = bottom_user_data.groupby('skillName')['score'].mean().to_dict()

prompt5 = f"""Compare two sales reps with very different performance:

TOP PERFORMER (51% win rate):
Skill Scores: {top_skills}
Sample Recommendations: {chr(10).join([f"- {rec[:150]}" for rec in top_recs[:10]])}

BOTTOM PERFORMER (22% win rate):
Skill Scores: {bottom_skills}
Sample Recommendations: {chr(10).join([f"- {rec[:150]}" for rec in bottom_recs[:10]])}

Provide:
1. Key differences in their approaches (based on recommendations)
2. Specific coaching plan for the bottom performer
3. What the bottom performer should learn from the top performer
4. Prioritized skill development plan

Be specific and actionable."""

print("Analyzing user-specific coaching needs...")
result5, tokens5, cost5 = call_openai(prompt5, model="gpt-3.5-turbo", max_tokens=1000)
print(result5)
print(f"\nTokens used: {tokens5}, Estimated cost: ${cost5:.4f}\n")

# ============================================================================
# ANALYSIS 6: Impact Text Sentiment & Themes
# ============================================================================
print("=" * 80)
print("ANALYSIS 6: Impact Text Analysis")
print("=" * 80)

# Compare impacts for won vs lost deals
won_impacts = merged_df[merged_df['outcome'] == 'won']['impact_text'].dropna().tolist()[:30]
lost_impacts = merged_df[merged_df['outcome'] == 'lost']['impact_text'].dropna().tolist()[:30]

prompt6 = f"""Analyze the "impact" descriptions from sales call evaluations.

IMPACTS FROM WON DEALS:
{chr(10).join([f"- {impact}" for impact in won_impacts[:20]])}

IMPACTS FROM LOST DEALS:
{chr(10).join([f"- {impact}" for impact in lost_impacts[:20]])}

Identify:
1. Common themes in won deal impacts vs lost deal impacts
2. Language patterns that predict success
3. Key behaviors that differentiate won from lost deals
4. Actionable insights for improving outcomes

Focus on what actually drives wins."""

print("Analyzing impact text patterns...")
result6, tokens6, cost6 = call_openai(prompt6, model="gpt-3.5-turbo", max_tokens=800)
print(result6)
print(f"\nTokens used: {tokens6}, Estimated cost: ${cost6:.4f}\n")

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print(f"\nTotal tokens used: {total_tokens_used:,}")
print(f"Total estimated cost: ${total_cost:.4f}")
print(f"Remaining budget: ${100 - total_cost:.2f}")

# Save results to file
results = {
    "recommendation_themes": result1,
    "citation_patterns": result2,
    "discover_why_analysis": result3,
    "temporal_decline": result4,
    "user_coaching": result5,
    "impact_analysis": result6,
    "cost_summary": {
        "total_tokens": total_tokens_used,
        "total_cost": total_cost,
        "remaining_budget": 100 - total_cost
    }
}

with open('llm_analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to 'llm_analysis_results.json'")
print("\nTo view formatted results, run: python format_llm_results.py")

