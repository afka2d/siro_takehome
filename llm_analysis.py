"""
LLM-Powered Analysis using OpenAI API
Supports Slides 3 and 6 of the presentation

This script uses OpenAI's API to extract deeper insights from text data:
- Slide 3: Deep dive on "Discover the Why" skill (weakest skill)
- Slide 6: Root cause analysis of performance decline over time

Requires OPENAI_API_KEY environment variable to be set.
"""

import pandas as pd
import numpy as np
import json
import os
from openai import OpenAI
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
    # Pricing: gpt-3.5-turbo: $0.0005/1k input, $0.0015/1k output
    if "gpt-4" in model.lower():
        input_cost = (prompt_tokens / 1000) * 0.03
        output_cost = (completion_tokens / 1000) * 0.06
    else:
        input_cost = (prompt_tokens / 1000) * 0.0005
        output_cost = (completion_tokens / 1000) * 0.0015
    return input_cost + output_cost

def call_openai(prompt, model="gpt-3.5-turbo", max_tokens=1000, temperature=0.3):
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

# ============================================================================
# SECTION 1: LOAD AND PREPARE DATA
# ============================================================================
print("Loading data...")
recording_df = pd.read_csv('ds_takehome_recording.csv')
scoring_df = pd.read_csv('ds_takehome_scoring_metadata.csv')

# Parse JSON metadata to extract text fields
def parse_metadata(row):
    """Extract impact and recommendation text from JSON metadata"""
    try:
        metadata = json.loads(row['scoringMetadata'])
        return {
            'impact': metadata.get('impact', ''),
            'recommendation': metadata.get('recommendation', ''),
        }
    except:
        return {
            'impact': '',
            'recommendation': '',
        }

scoring_df['parsed_metadata'] = scoring_df.apply(parse_metadata, axis=1)
scoring_df['impact_text'] = scoring_df['parsed_metadata'].apply(lambda x: x['impact'])
scoring_df['recommendation_text'] = scoring_df['parsed_metadata'].apply(lambda x: x['recommendation'])

# Merge with outcomes
recording_df['dateCreated'] = pd.to_datetime(recording_df['dateCreated'])
scoring_df['recordingdate'] = pd.to_datetime(scoring_df['recordingdate'])
merged_df = recording_df.merge(scoring_df, on='recordingid', how='inner', suffixes=('_recording', '_scoring'))
merged_df['score'] = pd.to_numeric(merged_df['score'], errors='coerce')

print(f"Loaded {len(merged_df)} merged records")
print()

# ============================================================================
# SECTION 2: SLIDE 3 - "DISCOVER THE WHY" DEEP DIVE
# ============================================================================
print("=" * 80)
print("SLIDE 3: 'DISCOVER THE WHY' DEEP DIVE")
print("=" * 80)

# Focus on the weakest skill
discover_why = merged_df[merged_df['skillName'] == 'Discover the "Why"'].copy()
discover_why_high = discover_why[discover_why['score'] >= 4]
discover_why_low = discover_why[discover_why['score'] <= 2]

# Extract sample impacts and recommendations
high_impacts = discover_why_high['impact_text'].dropna().tolist()[:15]
low_impacts = discover_why_low['impact_text'].dropna().tolist()[:15]
high_recs = discover_why_high['recommendation_text'].dropna().tolist()[:15]

# Create prompt for LLM analysis
prompt1 = f"""The skill "Discover the Why" has the lowest average score (2.63/5.0) across all reps.

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
result1, tokens1, cost1 = call_openai(prompt1, model="gpt-3.5-turbo", max_tokens=1000)
print(result1)
print(f"\nTokens used: {tokens1}, Estimated cost: ${cost1:.4f}\n")

# ============================================================================
# SECTION 3: SLIDE 6 - TEMPORAL DECLINE ROOT CAUSE ANALYSIS
# ============================================================================
print("=" * 80)
print("SLIDE 6: TEMPORAL DECLINE ROOT CAUSE ANALYSIS")
print("=" * 80)

# Compare early vs late period recommendations
merged_df['date'] = merged_df['recordingdate'].dt.date
early_period = merged_df[merged_df['date'] <= pd.to_datetime('2025-08-15').date()]
late_period = merged_df[merged_df['date'] >= pd.to_datetime('2025-09-15').date()]

early_recs = early_period['recommendation_text'].dropna().tolist()[:20]
late_recs = late_period['recommendation_text'].dropna().tolist()[:20]
early_impacts = early_period['impact_text'].dropna().tolist()[:15]
late_impacts = late_period['impact_text'].dropna().tolist()[:15]

# Create prompt for LLM analysis
prompt2 = f"""Performance declined significantly: win rate dropped from 64% to 40% and skill scores declined 15% over time.

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
result2, tokens2, cost2 = call_openai(prompt2, model="gpt-3.5-turbo", max_tokens=1000)
print(result2)
print(f"\nTokens used: {tokens2}, Estimated cost: ${cost2:.4f}\n")

# ============================================================================
# SECTION 4: SAVE RESULTS
# ============================================================================
print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print(f"\nTotal tokens used: {total_tokens_used:,}")
print(f"Total estimated cost: ${total_cost:.4f}")
print(f"Remaining budget: ${100 - total_cost:.2f}")

# Save results to file
results = {
    "discover_why_analysis": result1,
    "temporal_decline": result2,
    "cost_summary": {
        "total_tokens": total_tokens_used,
        "total_cost": total_cost,
        "remaining_budget": 100 - total_cost
    }
}

with open('llm_analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to 'llm_analysis_results.json'")
