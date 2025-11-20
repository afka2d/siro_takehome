"""
Extract individual charts from the main visualization file
Useful for creating individual slides in PowerPoint
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import json
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")

# Load data
print("Loading data...")
recording_df = pd.read_csv('ds_takehome_recording.csv')
scoring_df = pd.read_csv('ds_takehome_scoring_metadata.csv')

# Parse metadata
def parse_scoring_metadata(row):
    try:
        metadata = json.loads(row['scoringMetadata'])
        return pd.Series({
            'raw_text': metadata.get('raw', ''),
            'impact': metadata.get('impact', ''),
            'recommendation': metadata.get('recommendation', ''),
        })
    except:
        return pd.Series({
            'raw_text': '',
            'impact': '',
            'recommendation': '',
        })

scoring_parsed = scoring_df.apply(parse_scoring_metadata, axis=1)
scoring_df = pd.concat([scoring_df, scoring_parsed], axis=1)

# Clean data
recording_df['dateCreated'] = pd.to_datetime(recording_df['dateCreated'])
scoring_df['recordingdate'] = pd.to_datetime(scoring_df['recordingdate'])
recording_df['duration_minutes'] = recording_df['durationInMilliseconds'] / 60000
recording_df['speaking_ratio'] = recording_df['repSpeakingTime'] / recording_df['conversationTime']
recording_df['questions_ratio'] = recording_df['repQuestionsCount'] / (recording_df['repQuestionsCount'] + recording_df['customerQuestionsCount'] + 1)
scoring_df['score'] = pd.to_numeric(scoring_df['score'], errors='coerce')

# Merge
merged_df = recording_df.merge(scoring_df, on='recordingid', how='inner', suffixes=('_recording', '_scoring'))

print("Data loaded. Creating individual charts...\n")

# ============================================================================
# CHART 1: Outcome Distribution
# ============================================================================
fig, ax = plt.subplots(figsize=(8, 6))
outcome_counts = recording_df['outcome'].value_counts()
ax.bar(outcome_counts.index, outcome_counts.values, color=['#2ecc71', '#e74c3c', '#95a5a6'])
ax.set_title('Outcome Distribution', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Count', fontsize=12)
ax.set_xlabel('Outcome', fontsize=12)
for i, v in enumerate(outcome_counts.values):
    ax.text(i, v, str(v), ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('chart_01_outcome_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Chart 1: Outcome Distribution saved")
plt.close()

# ============================================================================
# CHART 2: Skill Scores by Outcome
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 7))
skill_outcome = merged_df.groupby(['skillName', 'outcome'])['score'].mean().unstack()
skill_outcome.plot(kind='barh', ax=ax, color=['#2ecc71', '#e74c3c', '#95a5a6'])
ax.set_title('Skill Scores by Outcome', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Average Score', fontsize=12)
ax.set_ylabel('Skill Name', fontsize=12)
ax.legend(title='Outcome', fontsize=10)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('chart_02_skill_scores_by_outcome.png', dpi=300, bbox_inches='tight')
print("✓ Chart 2: Skill Scores by Outcome saved")
plt.close()

# ============================================================================
# CHART 3: Average Questions by Outcome
# ============================================================================
fig, ax = plt.subplots(figsize=(8, 6))
outcome_questions = recording_df.groupby('outcome')[['repQuestionsCount', 'customerQuestionsCount']].mean()
outcome_questions.plot(kind='bar', ax=ax, color=['#3498db', '#9b59b6'])
ax.set_title('Average Questions by Outcome', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Average Count', fontsize=12)
ax.set_xlabel('Outcome', fontsize=12)
ax.legend(['Rep Questions', 'Customer Questions'], fontsize=10)
ax.tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig('chart_03_questions_by_outcome.png', dpi=300, bbox_inches='tight')
print("✓ Chart 3: Average Questions by Outcome saved")
plt.close()

# ============================================================================
# CHART 4: Average Skill Scores
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 7))
skill_scores = scoring_df.groupby('skillName')['score'].mean().sort_values(ascending=False)
ax.barh(range(len(skill_scores)), skill_scores.values, color='#3498db')
ax.set_yticks(range(len(skill_scores)))
ax.set_yticklabels(skill_scores.index)
ax.set_title('Average Skill Scores', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Average Score', fontsize=12)
ax.invert_yaxis()
# Add value labels
for i, v in enumerate(skill_scores.values):
    ax.text(v + 0.05, i, f'{v:.2f}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('chart_04_average_skill_scores.png', dpi=300, bbox_inches='tight')
print("✓ Chart 4: Average Skill Scores saved")
plt.close()

# ============================================================================
# CHART 5: User Win Rates
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
user_stats = recording_df.groupby('userId').agg({
    'recordingid': 'count',
    'outcome': lambda x: (x == 'won').sum(),
}).round(2)
user_stats.columns = ['num_recordings', 'wins']
user_stats['win_rate'] = (user_stats['wins'] / user_stats['num_recordings'] * 100).round(2)
user_win_rates = user_stats.sort_values('win_rate', ascending=False)
ax.barh(range(len(user_win_rates)), user_win_rates['win_rate'].values, color='#2ecc71')
ax.set_yticks(range(len(user_win_rates)))
ax.set_yticklabels([uid[:15] + '...' for uid in user_win_rates.index], fontsize=9)
ax.set_title('User Win Rates', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Win Rate (%)', fontsize=12)
ax.invert_yaxis()
# Add value labels
for i, v in enumerate(user_win_rates['win_rate'].values):
    ax.text(v + 1, i, f'{v:.1f}%', va='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('chart_05_user_win_rates.png', dpi=300, bbox_inches='tight')
print("✓ Chart 5: User Win Rates saved")
plt.close()

# ============================================================================
# CHART 6: Temporal Trend - Win Rate Over Time
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 6))
recording_df['date'] = recording_df['dateCreated'].dt.date
daily_outcomes = recording_df.groupby('date')['outcome'].apply(lambda x: (x == 'won').sum() / len(x) * 100)
daily_outcomes.sort_index().plot(kind='line', ax=ax, marker='o', color='#e67e22', linewidth=2, markersize=6)
ax.set_title('Win Rate Over Time', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Win Rate (%)', fontsize=12)
ax.grid(True, alpha=0.3)
ax.axhline(y=40, color='red', linestyle='--', alpha=0.5, label='Overall Average (40%)')
ax.legend(fontsize=10)
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('chart_06_win_rate_over_time.png', dpi=300, bbox_inches='tight')
print("✓ Chart 6: Win Rate Over Time saved")
plt.close()

# ============================================================================
# CHART 7: Score Distribution
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
scoring_df['score'].hist(bins=20, ax=ax, color='#3498db', edgecolor='black', alpha=0.7)
ax.set_title('Distribution of All Skill Scores', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Score', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
mean_score = scoring_df['score'].mean()
ax.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.2f}')
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('chart_07_score_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Chart 7: Score Distribution saved")
plt.close()

print("\n" + "=" * 60)
print("All individual charts saved successfully!")
print("=" * 60)
print("\nFiles created:")
print("  - chart_01_outcome_distribution.png")
print("  - chart_02_skill_scores_by_outcome.png")
print("  - chart_03_questions_by_outcome.png")
print("  - chart_04_average_skill_scores.png")
print("  - chart_05_user_win_rates.png")
print("  - chart_06_win_rate_over_time.png")
print("  - chart_07_score_distribution.png")

