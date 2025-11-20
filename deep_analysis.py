"""
Deep Dive Analysis - Additional Insights
Exploring patterns in recommendations, citations, and temporal trends
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load data
print("Loading data for deep analysis...")
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

print("\n" + "=" * 80)
print("DEEP ANALYSIS - ADDITIONAL INSIGHTS")
print("=" * 80)

# ============================================================================
# 1. RECOMMENDATION PATTERN ANALYSIS
# ============================================================================
print("\n--- Recommendation Pattern Analysis ---")

# Extract common words/phrases from recommendations
all_recommendations = ' '.join(scoring_df['recommendation_text'].dropna().astype(str))
# Simple keyword extraction
keywords = ['improve', 'continue', 'strengthen', 'leverage', 'focus', 'practice', 
            'defer', 'deepen', 'ask', 'use', 'build', 'enhance']

recommendation_words = all_recommendations.lower().split()
common_words = [w for w in recommendation_words if len(w) > 4]
word_freq = Counter(common_words)

print("\nTop recommendation keywords:")
for word, count in word_freq.most_common(15):
    print(f"  {word}: {count}")

# Recommendations by skill
print("\n--- Recommendations by Skill ---")
for skill in scoring_df['skillName'].unique():
    skill_recs = scoring_df[scoring_df['skillName'] == skill]['recommendation_text'].dropna()
    if len(skill_recs) > 0:
        # Count improvement vs continuation recommendations
        improve_count = skill_recs.str.lower().str.contains('improve|strengthen|enhance|focus|practice', na=False).sum()
        continue_count = skill_recs.str.lower().str.contains('continue|leverage|maintain', na=False).sum()
        print(f"\n{skill}:")
        print(f"  Improvement needed: {improve_count} ({improve_count/len(skill_recs)*100:.1f}%)")
        print(f"  Continue doing: {continue_count} ({continue_count/len(skill_recs)*100:.1f}%)")

# ============================================================================
# 2. CITATION ANALYSIS
# ============================================================================
print("\n--- Citation Analysis ---")

# Citations by skill
citation_by_skill = scoring_df.groupby('skillName')['num_citations'].agg(['mean', 'std', 'min', 'max'])
print("\nCitations per skill:")
print(citation_by_skill.round(2))

# Citations vs Score correlation
print(f"\nCorrelation between citations and score: {scoring_df['num_citations'].corr(scoring_df['score']):.3f}")

# Citations by outcome
citation_by_outcome = merged_df.groupby('outcome')['num_citations'].agg(['mean', 'std'])
print("\nCitations by outcome:")
print(citation_by_outcome.round(2))

# ============================================================================
# 3. TEMPORAL TRENDS
# ============================================================================
print("\n--- Temporal Trend Analysis ---")

# Score trends over time
merged_df['date'] = merged_df['recordingdate'].dt.date
daily_scores = merged_df.groupby(['date', 'skillName'])['score'].mean().reset_index()

# Overall score trend
overall_trend = merged_df.groupby('date')['score'].mean()
print(f"\nOverall score trend:")
print(f"  First week average: {overall_trend.head(7).mean():.2f}")
print(f"  Last week average: {overall_trend.tail(7).mean():.2f}")
print(f"  Change: {overall_trend.tail(7).mean() - overall_trend.head(7).mean():.2f}")

# Win rate trend
recording_df['date'] = recording_df['dateCreated'].dt.date
daily_outcomes = recording_df.groupby('date')['outcome'].apply(lambda x: (x == 'won').sum() / len(x) * 100)
print(f"\nWin rate trend:")
print(f"  First week average: {daily_outcomes.head(7).mean():.2f}%")
print(f"  Last week average: {daily_outcomes.tail(7).mean():.2f}%")
print(f"  Change: {daily_outcomes.tail(7).mean() - daily_outcomes.head(7).mean():.2f}%")

# ============================================================================
# 4. SKILL INTERACTION ANALYSIS
# ============================================================================
print("\n--- Skill Interaction Analysis ---")

# Create skill score matrix per recording
skill_pivot = merged_df.pivot_table(
    index='recordingid',
    columns='skillName',
    values='score',
    aggfunc='mean'
)

# Correlation between skills
skill_corr = skill_pivot.corr()
print("\nSkill correlations (top pairs):")
# Get upper triangle
mask = np.triu(np.ones_like(skill_corr, dtype=bool), k=1)
skill_corr_masked = skill_corr.where(mask)
# Convert to list of tuples
corr_pairs = []
for i in range(len(skill_corr_masked.columns)):
    for j in range(i+1, len(skill_corr_masked.columns)):
        val = skill_corr_masked.iloc[i, j]
        if not pd.isna(val):
            corr_pairs.append((skill_corr_masked.columns[i], skill_corr_masked.columns[j], val))
corr_df = pd.DataFrame(corr_pairs, columns=['Skill1', 'Skill2', 'Correlation'])
corr_df = corr_df.sort_values('Correlation', ascending=False)
print(corr_df.head(10).to_string(index=False))

# ============================================================================
# 5. IMPACT TEXT ANALYSIS
# ============================================================================
print("\n--- Impact Text Analysis ---")

# Impact text length
merged_df['impact_length'] = merged_df['impact_text'].str.len()
impact_by_outcome = merged_df.groupby('outcome')['impact_length'].mean()
print(f"\nAverage impact text length:")
print(f"  Won: {impact_by_outcome.get('won', 0):.0f} characters")
print(f"  Lost: {impact_by_outcome.get('lost', 0):.0f} characters")

# ============================================================================
# 6. USER-SPECIFIC DEEP DIVE
# ============================================================================
print("\n--- User-Specific Deep Dive ---")

for user_id in recording_df['userId'].unique():
    user_recordings = recording_df[recording_df['userId'] == user_id]
    user_scores = merged_df[merged_df['userId_recording'] == user_id]
    
    print(f"\nUser: {user_id[:20]}...")
    print(f"  Recordings: {len(user_recordings)}")
    print(f"  Win rate: {(user_recordings['outcome'] == 'won').sum() / len(user_recordings) * 100:.1f}%")
    print(f"  Avg skill score: {user_scores['score'].mean():.2f}")
    
    # Best and worst skills
    skill_avg = user_scores.groupby('skillName')['score'].mean().sort_values(ascending=False)
    print(f"  Best skill: {skill_avg.index[0]} ({skill_avg.iloc[0]:.2f})")
    print(f"  Worst skill: {skill_avg.index[-1]} ({skill_avg.iloc[-1]:.2f})")

# ============================================================================
# 7. SCORE DISTRIBUTION ANALYSIS
# ============================================================================
print("\n--- Score Distribution Analysis ---")

# Score distribution by skill
print("\nScore distributions by skill:")
for skill in scoring_df['skillName'].unique():
    skill_scores = scoring_df[scoring_df['skillName'] == skill]['score']
    print(f"\n{skill}:")
    print(f"  Mean: {skill_scores.mean():.2f}")
    print(f"  Median: {skill_scores.median():.2f}")
    print(f"  Score 1: {(skill_scores == 1).sum()} ({(skill_scores == 1).sum()/len(skill_scores)*100:.1f}%)")
    print(f"  Score 5: {(skill_scores == 5).sum()} ({(skill_scores == 5).sum()/len(skill_scores)*100:.1f}%)")

print("\n" + "=" * 80)
print("DEEP ANALYSIS COMPLETE")
print("=" * 80)

