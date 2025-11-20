# Siro DS Takehome Assignment

## Overview

This repository contains the analysis of sales conversation data from Bob's Builders, including recording metadata and LLM grader responses for sales skills evaluation.

## Files

- **`ds_takehome_recording.csv`**: Recording metadata (150 records)
  - Contains conversation metrics, duration, questions, word counts, and outcomes
  
- **`ds_takehome_scoring_metadata.csv`**: Skill evaluation data (993 records)
  - Contains LLM grader scores for 7 sales skills with detailed metadata

- **`analysis.py`**: Main analysis script
  - Loads and cleans data
  - Performs exploratory data analysis
  - Generates visualizations
  - Identifies key insights

- **`llm_analysis.py`**: LLM-powered text analysis
  - Deep dive on "Discover the Why" skill gaps
  - Temporal decline root cause analysis
  - Uses OpenAI API for qualitative insights

- **`presentation.md`**: Key findings and insights
  - Executive summary
  - 5 major findings with actionable recommendations
  - Questions for further exploration

- **`analysis_visualizations.png`**: Comprehensive visualization dashboard
  - 12 charts covering all major aspects of the analysis

- **`requirements.txt`**: Python dependencies

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the main analysis:
```bash
python analysis.py
```

3. (Optional) Run LLM analysis (requires OpenAI API key):
```bash
export OPENAI_API_KEY="your-api-key-here"
python llm_analysis.py
```

4. Review findings in `FINAL_SUMMARY_FOR_POWERPOINT.md`

## Key Findings Summary

1. **Skill scores strongly predict outcomes** - Won deals show consistently higher scores across all skills
2. **"Discover the Why" is the weakest skill** - Average score of 2.63/5.0 across all reps
3. **Question strategy matters** - Won deals have higher rep-to-customer question ratios
4. **Significant performance variation** - Win rates range from 21.7% to 51.2% across reps
5. **"Make a Friend" is the strongest skill** - Average score of 4.09/5.0 with low variability

## Data Summary

- **150 recordings** from **5 representatives**
- **993 skill evaluations** across **7 skills**
- **40% overall win rate** (60 won, 90 lost)
- **Time period:** August 6 - September 28, 2025

## Skills Evaluated

1. Make a Friend
2. Discover the "Why"
3. Value Proposition
4. Demonstration
5. Overcome Objections
6. Negotiation
7. Secure the Sale

## LLM-Powered Analysis

For deeper insights from text data (recommendations, impacts, citations), use the LLM analysis:

**Note:** You need to set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Then run the analysis:

```bash
python llm_analysis.py
python format_llm_results.py
```

See `LLM_ANALYSIS_RECOMMENDATIONS.md` for details on available analyses and cost estimates.

## Next Steps

See `presentation.md` for detailed recommendations and questions for further exploration.

