"""
Siro DS Takehome Assignment - Main Analysis Script
Supports Slides 1-5 of the presentation

This script performs quantitative analysis of sales conversation data:
- Slide 1: Executive Summary (dataset overview, temporal trends)
- Slide 2: Skill Scores Predict Outcomes
- Slide 3: "Discover the Why" is Weakest Skill
- Slide 4: Question Strategy Differences
- Slide 5: Performance Variation Across Reps
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 80)
print("SIRO DS TAKEHOME - MAIN ANALYSIS")
print("=" * 80)
print()

# ============================================================================
# SECTION 1: LOAD AND PREPARE DATA
# ============================================================================
print("Loading data...")
recording_df = pd.read_csv('ds_takehome_recording.csv')
scoring_df = pd.read_csv('ds_takehome_scoring_metadata.csv')

# Convert timestamps for temporal analysis
recording_df['dateCreated'] = pd.to_datetime(recording_df['dateCreated'])
scoring_df['recordingdate'] = pd.to_datetime(scoring_df['recordingdate'])

# Convert durations to minutes for easier interpretation
recording_df['duration_minutes'] = recording_df['durationInMilliseconds'] / 60000
recording_df['conversationTime_minutes'] = recording_df['conversationTime'] / 60000

# Calculate speaking ratio (rep speaking time / total conversation time)
recording_df['speaking_ratio'] = recording_df['repSpeakingTime'] / recording_df['conversationTime']

# Calculate questions ratio (rep questions / total questions)
recording_df['questions_ratio'] = recording_df['repQuestionsCount'] / (
    recording_df['repQuestionsCount'] + recording_df['customerQuestionsCount'] + 1
)

# Ensure score is numeric
scoring_df['score'] = pd.to_numeric(scoring_df['score'], errors='coerce')

# Merge recording and scoring data
merged_df = recording_df.merge(
    scoring_df,
    on='recordingid',
    how='inner',
    suffixes=('_recording', '_scoring')
)

print(f"Loaded {len(recording_df)} recordings and {len(scoring_df)} skill evaluations")
print(f"Merged dataset: {len(merged_df)} records")
print()

# ============================================================================
# SECTION 2: SLIDE 1 - EXECUTIVE SUMMARY
# ============================================================================
print("=" * 80)
print("SLIDE 1: EXECUTIVE SUMMARY")
print("=" * 80)

# Basic statistics
total_recordings = len(recording_df)
total_users = recording_df['userId'].nunique()
total_evaluations = len(scoring_df)
unique_skills = scoring_df['skillName'].nunique()
overall_win_rate = (recording_df['outcome'] == 'won').sum() / len(recording_df) * 100
avg_duration = recording_df['duration_minutes'].mean()
avg_skill_score = scoring_df['score'].mean()
date_range = f"{recording_df['dateCreated'].min().date()} to {recording_df['dateCreated'].max().date()}"

print(f"Total Recordings: {total_recordings}")
print(f"Total Users: {total_users}")
print(f"Total Skill Evaluations: {total_evaluations}")
print(f"Unique Skills: {unique_skills}")
print(f"Overall Win Rate: {overall_win_rate:.2f}%")
print(f"Average Call Duration: {avg_duration:.2f} minutes")
print(f"Average Skill Score: {avg_skill_score:.2f}/5.0")
print(f"Date Range: {date_range}")

# Temporal analysis - comparing first week vs last week
recording_df['date'] = recording_df['dateCreated'].dt.date
early_period = recording_df[recording_df['date'] <= pd.to_datetime('2025-08-15').date()]
late_period = recording_df[recording_df['date'] >= pd.to_datetime('2025-09-15').date()]

first_week_win_rate = (early_period['outcome'] == 'won').sum() / len(early_period) * 100
last_week_win_rate = (late_period['outcome'] == 'won').sum() / len(late_period) * 100

# Skill scores over time
early_scores = merged_df[merged_df['recordingdate'].dt.date <= pd.to_datetime('2025-08-15').date()]['score'].mean()
late_scores = merged_df[merged_df['recordingdate'].dt.date >= pd.to_datetime('2025-09-15').date()]['score'].mean()

print(f"\nFirst Week Win Rate: {first_week_win_rate:.2f}%")
print(f"Last Week Win Rate: {last_week_win_rate:.2f}%")
print(f"Win Rate Decline: {first_week_win_rate - last_week_win_rate:.2f} percentage points")
print(f"First Week Skill Score: {early_scores:.2f}")
print(f"Last Week Skill Score: {late_scores:.2f}")
print(f"Skill Score Decline: {early_scores - late_scores:.2f} points ({((early_scores - late_scores) / early_scores * 100):.1f}%)")

# ============================================================================
# SECTION 3: SLIDE 2 - SKILL SCORES PREDICT OUTCOMES
# ============================================================================
print("\n" + "=" * 80)
print("SLIDE 2: SKILL SCORES PREDICT OUTCOMES")
print("=" * 80)

# Calculate average skill scores by outcome
skill_outcome_scores = merged_df.groupby(['skillName', 'outcome'])['score'].mean().unstack(fill_value=0)
print("\nSkill Scores by Outcome:")
print(skill_outcome_scores.round(2))

# Calculate percentage improvements
for skill in skill_outcome_scores.index:
    won_score = skill_outcome_scores.loc[skill, 'won']
    lost_score = skill_outcome_scores.loc[skill, 'lost']
    if lost_score > 0:
        improvement = ((won_score - lost_score) / lost_score) * 100
        print(f"{skill}: Won={won_score:.2f}, Lost={lost_score:.2f}, Improvement={improvement:.0f}%")

# ============================================================================
# SECTION 4: SLIDE 3 - "DISCOVER THE WHY" IS WEAKEST SKILL
# ============================================================================
print("\n" + "=" * 80)
print("SLIDE 3: 'DISCOVER THE WHY' IS WEAKEST SKILL")
print("=" * 80)

# Calculate average scores by skill
skill_stats = scoring_df.groupby('skillName')['score'].agg(['mean', 'std', 'count', 'min', 'max'])
skill_stats = skill_stats.sort_values('mean', ascending=False)

print("\nAverage Skill Scores (sorted):")
print(skill_stats.round(2))

# Focus on "Discover the Why"
discover_why = scoring_df[scoring_df['skillName'] == 'Discover the "Why"']
discover_why_stats = {
    'mean': discover_why['score'].mean(),
    'std': discover_why['score'].std(),
    'won_mean': merged_df[(merged_df['skillName'] == 'Discover the "Why"') & (merged_df['outcome'] == 'won')]['score'].mean(),
    'lost_mean': merged_df[(merged_df['skillName'] == 'Discover the "Why"') & (merged_df['outcome'] == 'lost')]['score'].mean(),
    'score_1_count': (discover_why['score'] == 1).sum(),
    'score_5_count': (discover_why['score'] == 5).sum(),
    'total': len(discover_why)
}

print(f"\n'Discover the Why' Statistics:")
print(f"  Average Score: {discover_why_stats['mean']:.2f}/5.0")
print(f"  Standard Deviation: {discover_why_stats['std']:.2f}")
print(f"  Won Deals Average: {discover_why_stats['won_mean']:.2f}/5.0")
print(f"  Lost Deals Average: {discover_why_stats['lost_mean']:.2f}/5.0")
print(f"  Score 1 Frequency: {discover_why_stats['score_1_count']} ({discover_why_stats['score_1_count']/discover_why_stats['total']*100:.1f}%)")
print(f"  Score 5 Frequency: {discover_why_stats['score_5_count']} ({discover_why_stats['score_5_count']/discover_why_stats['total']*100:.1f}%)")

# ============================================================================
# SECTION 5: SLIDE 4 - QUESTION STRATEGY DIFFERENCES
# ============================================================================
print("\n" + "=" * 80)
print("SLIDE 4: QUESTION STRATEGY DIFFERENCES")
print("=" * 80)

# Calculate average questions by outcome
outcome_questions = recording_df.groupby('outcome').agg({
    'repQuestionsCount': 'mean',
    'customerQuestionsCount': 'mean'
})

print("\nAverage Questions by Outcome:")
print(outcome_questions.round(2))

# Calculate ratios
won_rep_questions = outcome_questions.loc['won', 'repQuestionsCount']
won_customer_questions = outcome_questions.loc['won', 'customerQuestionsCount']
won_ratio = won_rep_questions / won_customer_questions

lost_rep_questions = outcome_questions.loc['lost', 'repQuestionsCount']
lost_customer_questions = outcome_questions.loc['lost', 'customerQuestionsCount']
lost_ratio = lost_rep_questions / lost_customer_questions

print(f"\nWon Deals:")
print(f"  Rep Questions: {won_rep_questions:.2f}")
print(f"  Customer Questions: {won_customer_questions:.2f}")
print(f"  Ratio: {won_ratio:.2f} rep questions per customer question")

print(f"\nLost Deals:")
print(f"  Rep Questions: {lost_rep_questions:.2f}")
print(f"  Customer Questions: {lost_customer_questions:.2f}")
print(f"  Ratio: {lost_ratio:.2f} rep questions per customer question")

print(f"\nDifference:")
print(f"  Rep asks {won_rep_questions - lost_rep_questions:.2f} more questions in won deals")
print(f"  Customer asks {lost_customer_questions - won_customer_questions:.2f} more questions in lost deals")

# ============================================================================
# SECTION 6: SLIDE 5 - PERFORMANCE VARIATION ACROSS REPS
# ============================================================================
print("\n" + "=" * 80)
print("SLIDE 5: PERFORMANCE VARIATION ACROSS REPS")
print("=" * 80)

# Calculate user-level statistics
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

# Calculate average skill scores per user
user_skill_scores = merged_df.groupby('userId_recording')['score'].mean()
user_stats['avg_skill_score'] = user_skill_scores.round(2)

# Sort by win rate
user_stats = user_stats.sort_values('win_rate', ascending=False)

print("\nUser Performance Summary:")
print(user_stats[['num_recordings', 'win_rate', 'avg_skill_score']])

# Calculate range
highest_win_rate = user_stats['win_rate'].max()
lowest_win_rate = user_stats['win_rate'].min()
difference_ratio = highest_win_rate / lowest_win_rate

print(f"\nWin Rate Range:")
print(f"  Highest: {highest_win_rate:.1f}%")
print(f"  Lowest: {lowest_win_rate:.1f}%")
print(f"  Difference: {difference_ratio:.1f}x")

# ============================================================================
# SECTION 7: CREATE VISUALIZATIONS
# ============================================================================
print("\n" + "=" * 80)
print("GENERATING VISUALIZATIONS")
print("=" * 80)

# Create figure with subplots for key charts
fig = plt.figure(figsize=(20, 12))

# Chart 1: Outcome Distribution (Slide 1)
ax1 = plt.subplot(2, 3, 1)
outcome_counts = recording_df['outcome'].value_counts()
ax1.bar(outcome_counts.index, outcome_counts.values, color=['#2ecc71', '#e74c3c', '#95a5a6'])
ax1.set_title('Outcome Distribution', fontsize=14, fontweight='bold')
ax1.set_ylabel('Count')
ax1.set_xlabel('Outcome')
for i, v in enumerate(outcome_counts.values):
    ax1.text(i, v, str(v), ha='center', va='bottom')

# Chart 2: Skill Scores by Outcome (Slide 2)
ax2 = plt.subplot(2, 3, 2)
skill_outcome_plot = merged_df.groupby(['skillName', 'outcome'])['score'].mean().unstack()
skill_outcome_plot.plot(kind='barh', ax=ax2, color=['#2ecc71', '#e74c3c', '#95a5a6'])
ax2.set_title('Skill Scores by Outcome', fontsize=14, fontweight='bold')
ax2.set_xlabel('Average Score')
ax2.legend(title='Outcome')
ax2.invert_yaxis()

# Chart 3: Average Questions by Outcome (Slide 4)
ax3 = plt.subplot(2, 3, 3)
outcome_questions_plot = recording_df.groupby('outcome')[['repQuestionsCount', 'customerQuestionsCount']].mean()
outcome_questions_plot.plot(kind='bar', ax=ax3, color=['#3498db', '#9b59b6'])
ax3.set_title('Average Questions by Outcome', fontsize=14, fontweight='bold')
ax3.set_ylabel('Average Count')
ax3.set_xlabel('Outcome')
ax3.legend(['Rep Questions', 'Customer Questions'])
ax3.tick_params(axis='x', rotation=0)

# Chart 4: Average Skill Scores (Slide 3)
ax4 = plt.subplot(2, 3, 4)
skill_scores = scoring_df.groupby('skillName')['score'].mean().sort_values(ascending=False)
ax4.barh(range(len(skill_scores)), skill_scores.values, color='#3498db')
ax4.set_yticks(range(len(skill_scores)))
ax4.set_yticklabels(skill_scores.index)
ax4.set_title('Average Skill Scores', fontsize=14, fontweight='bold')
ax4.set_xlabel('Average Score')
ax4.invert_yaxis()
for i, v in enumerate(skill_scores.values):
    ax4.text(v + 0.05, i, f'{v:.2f}', va='center', fontsize=9)

# Chart 5: User Win Rates (Slide 5)
ax5 = plt.subplot(2, 3, 5)
user_win_rates = user_stats.sort_values('win_rate', ascending=False)
ax5.barh(range(len(user_win_rates)), user_win_rates['win_rate'].values, color='#2ecc71')
ax5.set_yticks(range(len(user_win_rates)))
ax5.set_yticklabels([uid[:15] + '...' for uid in user_win_rates.index], fontsize=9)
ax5.set_title('User Win Rates', fontsize=14, fontweight='bold')
ax5.set_xlabel('Win Rate (%)')
ax5.invert_yaxis()
for i, v in enumerate(user_win_rates['win_rate'].values):
    ax5.text(v + 1, i, f'{v:.1f}%', va='center', fontsize=9, fontweight='bold')

# Chart 6: Win Rate Over Time (Slide 1 & 6)
ax6 = plt.subplot(2, 3, 6)
daily_outcomes = recording_df.groupby('date')['outcome'].apply(lambda x: (x == 'won').sum() / len(x) * 100)
daily_outcomes.sort_index().plot(kind='line', ax=ax6, marker='o', color='#e67e22', linewidth=2, markersize=6)
ax6.set_title('Win Rate Over Time', fontsize=14, fontweight='bold')
ax6.set_xlabel('Date')
ax6.set_ylabel('Win Rate (%)')
ax6.grid(True, alpha=0.3)
ax6.axhline(y=overall_win_rate, color='red', linestyle='--', alpha=0.5, label=f'Overall Avg ({overall_win_rate:.0f}%)')
ax6.legend(fontsize=9)
ax6.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('analysis_visualizations.png', dpi=300, bbox_inches='tight')
print("\nVisualizations saved to 'analysis_visualizations.png'")

# Save individual charts
print("\nSaving individual charts...")

# Chart 1
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
plt.close()

# Chart 2
fig, ax = plt.subplots(figsize=(10, 7))
skill_outcome_plot = merged_df.groupby(['skillName', 'outcome'])['score'].mean().unstack()
skill_outcome_plot.plot(kind='barh', ax=ax, color=['#2ecc71', '#e74c3c', '#95a5a6'])
ax.set_title('Skill Scores by Outcome', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Average Score', fontsize=12)
ax.set_ylabel('Skill Name', fontsize=12)
ax.legend(title='Outcome', fontsize=10)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('chart_02_skill_scores_by_outcome.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 3
fig, ax = plt.subplots(figsize=(8, 6))
outcome_questions_plot = recording_df.groupby('outcome')[['repQuestionsCount', 'customerQuestionsCount']].mean()
outcome_questions_plot.plot(kind='bar', ax=ax, color=['#3498db', '#9b59b6'])
ax.set_title('Average Questions by Outcome', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Average Count', fontsize=12)
ax.set_xlabel('Outcome', fontsize=12)
ax.legend(['Rep Questions', 'Customer Questions'], fontsize=10)
ax.tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig('chart_03_questions_by_outcome.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 4
fig, ax = plt.subplots(figsize=(10, 7))
skill_scores = scoring_df.groupby('skillName')['score'].mean().sort_values(ascending=False)
ax.barh(range(len(skill_scores)), skill_scores.values, color='#3498db')
ax.set_yticks(range(len(skill_scores)))
ax.set_yticklabels(skill_scores.index)
ax.set_title('Average Skill Scores', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Average Score', fontsize=12)
ax.invert_yaxis()
for i, v in enumerate(skill_scores.values):
    ax.text(v + 0.05, i, f'{v:.2f}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('chart_04_average_skill_scores.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 5
fig, ax = plt.subplots(figsize=(10, 6))
user_win_rates = user_stats.sort_values('win_rate', ascending=False)
ax.barh(range(len(user_win_rates)), user_win_rates['win_rate'].values, color='#2ecc71')
ax.set_yticks(range(len(user_win_rates)))
ax.set_yticklabels([uid[:15] + '...' for uid in user_win_rates.index], fontsize=9)
ax.set_title('User Win Rates', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Win Rate (%)', fontsize=12)
ax.invert_yaxis()
for i, v in enumerate(user_win_rates['win_rate'].values):
    ax.text(v + 1, i, f'{v:.1f}%', va='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('chart_05_user_win_rates.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 6
fig, ax = plt.subplots(figsize=(12, 6))
daily_outcomes = recording_df.groupby('date')['outcome'].apply(lambda x: (x == 'won').sum() / len(x) * 100)
daily_outcomes.sort_index().plot(kind='line', ax=ax, marker='o', color='#e67e22', linewidth=2, markersize=6)
ax.set_title('Win Rate Over Time', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Win Rate (%)', fontsize=12)
ax.grid(True, alpha=0.3)
ax.axhline(y=overall_win_rate, color='red', linestyle='--', alpha=0.5, label=f'Overall Average ({overall_win_rate:.0f}%)')
ax.legend(fontsize=10)
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('chart_06_win_rate_over_time.png', dpi=300, bbox_inches='tight')
plt.close()

print("All individual charts saved successfully!")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
