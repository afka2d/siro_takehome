"""
Deep Analysis - Supporting Functions
Helper functions for additional analysis if needed

This file contains utility functions that may be referenced but are not
essential for the 6-slide presentation. Kept for completeness.
"""

import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

def parse_scoring_metadata(df):
    """
    Parse JSON scoringMetadata column to extract structured data
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with 'scoringMetadata' column containing JSON strings
    
    Returns:
    --------
    pandas.DataFrame
        Original DataFrame with additional parsed columns
    """
    def parse_row(row):
        try:
            metadata = json.loads(row['scoringMetadata'])
            return {
                'impact': metadata.get('impact', ''),
                'recommendation': metadata.get('recommendation', ''),
                'citations': metadata.get('thinkingWithCitation', {}).get('citations', [])
            }
        except:
            return {
                'impact': '',
                'recommendation': '',
                'citations': []
            }
    
    parsed = df.apply(parse_row, axis=1)
    df['parsed_metadata'] = parsed
    df['impact_text'] = df['parsed_metadata'].apply(lambda x: x['impact'])
    df['recommendation_text'] = df['parsed_metadata'].apply(lambda x: x['recommendation'])
    df['num_citations'] = df['parsed_metadata'].apply(lambda x: len(x['citations']))
    
    return df

def calculate_skill_correlations(merged_df):
    """
    Calculate correlation matrix between different skills
    
    Parameters:
    -----------
    merged_df : pandas.DataFrame
        Merged dataframe with recording and scoring data
    
    Returns:
    --------
    pandas.DataFrame
        Correlation matrix between skills
    """
    # Create pivot table: one row per recording, one column per skill
    skill_pivot = merged_df.pivot_table(
        index='recordingid',
        columns='skillName',
        values='score',
        aggfunc='mean'
    )
    
    # Calculate correlation
    skill_corr = skill_pivot.corr()
    
    return skill_corr

def analyze_recommendation_patterns(scoring_df):
    """
    Analyze patterns in coaching recommendations
    
    Parameters:
    -----------
    scoring_df : pandas.DataFrame
        DataFrame with recommendation_text column
    
    Returns:
    --------
    dict
        Dictionary with recommendation statistics
    """
    all_recs = scoring_df['recommendation_text'].dropna().tolist()
    
    # Count improvement vs continuation keywords
    improve_keywords = ['improve', 'strengthen', 'enhance', 'focus', 'practice', 'defer', 'deepen']
    continue_keywords = ['continue', 'leverage', 'maintain', 'keep']
    
    improve_count = sum(1 for rec in all_recs if any(kw in rec.lower() for kw in improve_keywords))
    continue_count = sum(1 for rec in all_recs if any(kw in rec.lower() for kw in continue_keywords))
    
    return {
        'total_recommendations': len(all_recs),
        'improvement_needed': improve_count,
        'continue_doing': continue_count
    }

# Example usage (commented out - uncomment if needed)
if __name__ == "__main__":
    print("This file contains helper functions for deep analysis.")
    print("Import functions as needed, or use main analysis.py for primary analysis.")
