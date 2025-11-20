"""
Siro DS Takehome Assignment - Sales Conversation Analysis
Analyzing sales conversation metadata and LLM grader responses
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 80)
print("SIRO DS TAKEHOME ASSIGNMENT - SALES CONVERSATION ANALYSIS")
print("=" * 80)
print()

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("Loading data...")
recording_df = pd.read_csv('ds_takehome_recording.csv')
scoring_df = pd.read_csv('ds_takehome_scoring_metadata.csv')

print(f"Recording data: {len(recording_df)} records")
print(f"Scoring metadata: {len(scoring_df)} records")
print()

# ============================================================================
# 2. DATA EXPLORATION & CLEANING
# ============================================================================
print("=" * 80)
print("DATA OVERVIEW")
print("=" * 80)

# Recording data info
print("\nRecording Data Columns:")
print(recording_df.columns.tolist())
print(f"\nRecording Data Shape: {recording_df.shape}")
print(f"\nRecording Data Info:")
print(recording_df.info())
print(f"\nRecording Data Sample:")
print(recording_df.head())

# Scoring data info
print("\n\nScoring Data Columns:")
print(scoring_df.columns.tolist())
print(f"\nScoring Data Shape: {scoring_df.shape}")
print(f"\nScoring Data Info:")
print(scoring_df.info())
print(f"\nUnique Skills:")
print(scoring_df['skillName'].value_counts())
print(f"\nUnique Users:")
print(scoring_df['userId'].value_counts())

# ============================================================================
# 3. PARSE JSON SCORING METADATA
# ============================================================================
print("\n" + "=" * 80)
print("PARSING SCORING METADATA")
print("=" * 80)

def parse_scoring_metadata(row):
    """Parse the JSON scoringMetadata column"""
    try:
        metadata = json.loads(row['scoringMetadata'])
        return pd.Series({
            'raw_text': metadata.get('raw', ''),
            'score_from_metadata': metadata.get('score', ''),
            'impact': metadata.get('impact', ''),
            'recommendation': metadata.get('recommendation', ''),
            'has_citations': 'citations' in metadata.get('thinkingWithCitation', {}),
            'num_citations': len(metadata.get('thinkingWithCitation', {}).get('citations', []))
        })
    except:
        return pd.Series({
            'raw_text': '',
            'score_from_metadata': '',
            'impact': '',
            'recommendation': '',
            'has_citations': False,
            'num_citations': 0
        })

# Parse metadata
scoring_parsed = scoring_df.apply(parse_scoring_metadata, axis=1)
scoring_df = pd.concat([scoring_df, scoring_parsed], axis=1)

print(f"\nSuccessfully parsed {scoring_df['has_citations'].sum()} records with citations")
print(f"Average citations per record: {scoring_df['num_citations'].mean():.2f}")

# ============================================================================
# 4. DATA CLEANING & TRANSFORMATIONS
# ============================================================================
print("\n" + "=" * 80)
print("DATA CLEANING")
print("=" * 80)

# Convert timestamps
recording_df['dateCreated'] = pd.to_datetime(recording_df['dateCreated'])
scoring_df['recordingdate'] = pd.to_datetime(scoring_df['recordingdate'])

# Convert durations to minutes for easier interpretation
recording_df['duration_minutes'] = recording_df['durationInMilliseconds'] / 60000
recording_df['conversationTime_minutes'] = recording_df['conversationTime'] / 60000
recording_df['repSpeakingTime_minutes'] = recording_df['repSpeakingTime'] / 60000

# Calculate speaking ratio
recording_df['speaking_ratio'] = recording_df['repSpeakingTime'] / recording_df['conversationTime']
recording_df['questions_ratio'] = recording_df['repQuestionsCount'] / (recording_df['repQuestionsCount'] + recording_df['customerQuestionsCount'] + 1)

# Ensure score is numeric
scoring_df['score'] = pd.to_numeric(scoring_df['score'], errors='coerce')

print(f"\nCleaned data:")
print(f"- Recording records: {len(recording_df)}")
print(f"- Scoring records: {len(scoring_df)}")
print(f"- Missing scores: {scoring_df['score'].isna().sum()}")

# ============================================================================
# 5. MERGE DATA
# ============================================================================
print("\n" + "=" * 80)
print("MERGING DATA")
print("=" * 80)

# Merge recording and scoring data
merged_df = recording_df.merge(
    scoring_df,
    on='recordingid',
    how='inner',
    suffixes=('_recording', '_scoring')
)

print(f"Merged dataset: {len(merged_df)} records")
print(f"Unique recordings in merged: {merged_df['recordingid'].nunique()}")
print(f"Unique users: {merged_df['userId_recording'].nunique()}")

# ============================================================================
# 6. EXPLORATORY DATA ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# Basic statistics
print("\n--- Recording Statistics ---")
print(f"Total recordings: {recording_df['recordingid'].nunique()}")
print(f"Total users: {recording_df['userId'].nunique()}")
print(f"Date range: {recording_df['dateCreated'].min()} to {recording_df['dateCreated'].max()}")
print(f"\nOutcome distribution:")
print(recording_df['outcome'].value_counts())
print(f"\nOutcome percentages:")
print(recording_df['outcome'].value_counts(normalize=True) * 100)

print("\n--- Conversation Metrics ---")
print(f"Average duration: {recording_df['duration_minutes'].mean():.2f} minutes")
print(f"Average conversation time: {recording_df['conversationTime_minutes'].mean():.2f} minutes")
print(f"Average rep speaking time: {recording_df['repSpeakingTime_minutes'].mean():.2f} minutes")
print(f"Average speaking ratio: {recording_df['speaking_ratio'].mean():.2f}")
print(f"Average rep word count: {recording_df['repWordCount'].mean():.0f} words")
print(f"Average rep questions: {recording_df['repQuestionsCount'].mean():.2f}")
print(f"Average customer questions: {recording_df['customerQuestionsCount'].mean():.2f}")

print("\n--- Skill Scores ---")
skill_stats = scoring_df.groupby('skillName')['score'].agg(['mean', 'std', 'count', 'min', 'max'])
print(skill_stats.round(2))

# User-level statistics
print("\n--- User Performance ---")
user_stats = recording_df.groupby('userId').agg({
    'recordingid': 'count',
    'outcome': lambda x: (x == 'won').sum(),
    'duration_minutes': 'mean',
    'repWordCount': 'mean',
    'repQuestionsCount': 'mean',
    'customerQuestionsCount': 'mean'
}).round(2)
user_stats.columns = ['num_recordings', 'wins', 'avg_duration_min', 'avg_words', 'avg_rep_questions', 'avg_customer_questions']
user_stats['win_rate'] = (user_stats['wins'] / user_stats['num_recordings'] * 100).round(2)
print(user_stats)

# ============================================================================
# 7. KEY INSIGHTS ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("KEY INSIGHTS")
print("=" * 80)

# Insight 1: Outcome vs Speaking Ratio
print("\n--- Insight 1: Speaking Ratio vs Outcome ---")
outcome_speaking = recording_df.groupby('outcome')['speaking_ratio'].agg(['mean', 'std', 'count'])
print(outcome_speaking.round(3))

# Insight 2: Outcome vs Questions
print("\n--- Insight 2: Questions vs Outcome ---")
outcome_questions = recording_df.groupby('outcome').agg({
    'repQuestionsCount': 'mean',
    'customerQuestionsCount': 'mean'
})
print(outcome_questions.round(2))

# Insight 3: Skill Scores vs Outcome
print("\n--- Insight 3: Skill Scores by Outcome ---")
skill_outcome = merged_df.groupby(['skillName', 'outcome'])['score'].mean().unstack(fill_value=0)
print(skill_outcome.round(2))

# Insight 4: User Performance on Skills
print("\n--- Insight 4: User Performance by Skill ---")
user_skill_scores = merged_df.groupby(['userId_recording', 'skillName'])['score'].mean().unstack(fill_value=0)
print(user_skill_scores.round(2))

# Insight 5: Correlation Analysis
print("\n--- Insight 5: Correlation Matrix (Recording Metrics) ---")
corr_cols = ['duration_minutes', 'conversationTime_minutes', 'repSpeakingTime_minutes', 
             'speaking_ratio', 'repWordCount', 'repQuestionsCount', 'customerQuestionsCount', 
             'questions_ratio']
corr_matrix = recording_df[corr_cols].corr()
print(corr_matrix.round(3))

# ============================================================================
# 8. VISUALIZATIONS
# ============================================================================
print("\n" + "=" * 80)
print("GENERATING VISUALIZATIONS")
print("=" * 80)

# Create figure with subplots
fig = plt.figure(figsize=(20, 24))

# 1. Outcome Distribution
ax1 = plt.subplot(4, 3, 1)
outcome_counts = recording_df['outcome'].value_counts()
ax1.bar(outcome_counts.index, outcome_counts.values, color=['#2ecc71', '#e74c3c', '#95a5a6'])
ax1.set_title('Outcome Distribution', fontsize=14, fontweight='bold')
ax1.set_ylabel('Count')
ax1.set_xlabel('Outcome')
for i, v in enumerate(outcome_counts.values):
    ax1.text(i, v, str(v), ha='center', va='bottom')

# 2. Speaking Ratio by Outcome
ax2 = plt.subplot(4, 3, 2)
recording_df.boxplot(column='speaking_ratio', by='outcome', ax=ax2)
ax2.set_title('Speaking Ratio by Outcome', fontsize=14, fontweight='bold')
ax2.set_xlabel('Outcome')
ax2.set_ylabel('Speaking Ratio')
plt.suptitle('')  # Remove default title

# 3. Questions by Outcome
ax3 = plt.subplot(4, 3, 3)
outcome_questions_plot = recording_df.groupby('outcome')[['repQuestionsCount', 'customerQuestionsCount']].mean()
outcome_questions_plot.plot(kind='bar', ax=ax3, color=['#3498db', '#9b59b6'])
ax3.set_title('Average Questions by Outcome', fontsize=14, fontweight='bold')
ax3.set_ylabel('Average Count')
ax3.set_xlabel('Outcome')
ax3.legend(['Rep Questions', 'Customer Questions'])
ax3.tick_params(axis='x', rotation=45)

# 4. Skill Scores Distribution
ax4 = plt.subplot(4, 3, 4)
skill_scores = scoring_df.groupby('skillName')['score'].mean().sort_values(ascending=False)
ax4.barh(range(len(skill_scores)), skill_scores.values, color='#3498db')
ax4.set_yticks(range(len(skill_scores)))
ax4.set_yticklabels(skill_scores.index)
ax4.set_title('Average Skill Scores', fontsize=14, fontweight='bold')
ax4.set_xlabel('Average Score')
ax4.invert_yaxis()

# 5. Skill Scores by Outcome
ax5 = plt.subplot(4, 3, 5)
skill_outcome_plot = merged_df.groupby(['skillName', 'outcome'])['score'].mean().unstack()
skill_outcome_plot.plot(kind='barh', ax=ax5, color=['#2ecc71', '#e74c3c', '#95a5a6'])
ax5.set_title('Skill Scores by Outcome', fontsize=14, fontweight='bold')
ax5.set_xlabel('Average Score')
ax5.legend(title='Outcome')
ax5.invert_yaxis()

# 6. User Win Rates
ax6 = plt.subplot(4, 3, 6)
user_win_rates = user_stats.sort_values('win_rate', ascending=False)
ax6.barh(range(len(user_win_rates)), user_win_rates['win_rate'].values, color='#2ecc71')
ax6.set_yticks(range(len(user_win_rates)))
ax6.set_yticklabels(user_win_rates.index)
ax6.set_title('User Win Rates', fontsize=14, fontweight='bold')
ax6.set_xlabel('Win Rate (%)')
ax6.invert_yaxis()

# 7. Duration vs Outcome
ax7 = plt.subplot(4, 3, 7)
recording_df.boxplot(column='duration_minutes', by='outcome', ax=ax7)
ax7.set_title('Call Duration by Outcome', fontsize=14, fontweight='bold')
ax7.set_xlabel('Outcome')
ax7.set_ylabel('Duration (minutes)')
plt.suptitle('')

# 8. Rep Word Count by Outcome
ax8 = plt.subplot(4, 3, 8)
recording_df.boxplot(column='repWordCount', by='outcome', ax=ax8)
ax8.set_title('Rep Word Count by Outcome', fontsize=14, fontweight='bold')
ax8.set_xlabel('Outcome')
ax8.set_ylabel('Word Count')
plt.suptitle('')

# 9. Questions Ratio by Outcome
ax9 = plt.subplot(4, 3, 9)
recording_df.boxplot(column='questions_ratio', by='outcome', ax=ax9)
ax9.set_title('Questions Ratio (Rep/Customer) by Outcome', fontsize=14, fontweight='bold')
ax9.set_xlabel('Outcome')
ax9.set_ylabel('Questions Ratio')
plt.suptitle('')

# 10. Skill Score Distribution
ax10 = plt.subplot(4, 3, 10)
scoring_df['score'].hist(bins=20, ax=ax10, color='#3498db', edgecolor='black')
ax10.set_title('Distribution of All Skill Scores', fontsize=14, fontweight='bold')
ax10.set_xlabel('Score')
ax10.set_ylabel('Frequency')
ax10.axvline(scoring_df['score'].mean(), color='red', linestyle='--', label=f'Mean: {scoring_df["score"].mean():.2f}')
ax10.legend()

# 11. Citations Analysis
ax11 = plt.subplot(4, 3, 11)
citation_counts = scoring_df['num_citations'].value_counts().sort_index()
ax11.bar(citation_counts.index, citation_counts.values, color='#9b59b6')
ax11.set_title('Distribution of Citations per Record', fontsize=14, fontweight='bold')
ax11.set_xlabel('Number of Citations')
ax11.set_ylabel('Frequency')

# 12. Time Series - Recordings Over Time
ax12 = plt.subplot(4, 3, 12)
recording_df['dateCreated'].dt.date.value_counts().sort_index().plot(kind='line', ax=ax12, marker='o', color='#e67e22')
ax12.set_title('Recordings Over Time', fontsize=14, fontweight='bold')
ax12.set_xlabel('Date')
ax12.set_ylabel('Number of Recordings')
ax12.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('analysis_visualizations.png', dpi=300, bbox_inches='tight')
print("\nVisualizations saved to 'analysis_visualizations.png'")

# ============================================================================
# 9. SUMMARY STATISTICS
# ============================================================================
print("\n" + "=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)

summary_stats = {
    'Total Recordings': len(recording_df),
    'Total Users': recording_df['userId'].nunique(),
    'Total Skill Evaluations': len(scoring_df),
    'Unique Skills': scoring_df['skillName'].nunique(),
    'Overall Win Rate': f"{(recording_df['outcome'] == 'won').sum() / len(recording_df) * 100:.2f}%",
    'Average Call Duration (min)': f"{recording_df['duration_minutes'].mean():.2f}",
    'Average Skill Score': f"{scoring_df['score'].mean():.2f}",
    'Date Range': f"{recording_df['dateCreated'].min().date()} to {recording_df['dateCreated'].max().date()}"
}

for key, value in summary_stats.items():
    print(f"{key}: {value}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)

