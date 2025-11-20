# LLM-Powered Analysis Recommendations

## Overview

This document outlines the recommended LLM-powered analyses to extract deeper insights from the sales conversation data. The `llm_analysis.py` script implements these analyses using the OpenAI API.

## Why Use LLMs for This Analysis?

The dataset contains rich **unstructured text data** that traditional analysis can't fully leverage:
- **Recommendations**: 993 coaching recommendations with nuanced guidance
- **Impact descriptions**: Detailed explanations of how behaviors affected outcomes
- **Citations**: Actual quotes from sales calls (17.8 average per evaluation)
- **Raw evaluation text**: Full LLM grader reasoning

LLMs excel at:
- Pattern recognition in natural language
- Extracting themes and categories
- Identifying specific language patterns
- Generating actionable insights from text

## Recommended Analyses

### 1. **Key Themes in Recommendations** ✅
**Purpose**: Categorize and understand what coaching recommendations are most common

**What it does**:
- Compares recommendations from high-scoring (4-5) vs low-scoring (1-2) evaluations
- Identifies top 5 themes/categories
- Determines which themes correlate with success

**Value**: Helps prioritize training focus areas

**Estimated Cost**: ~$0.05-0.10

---

### 2. **Citation Pattern Analysis** ✅
**Purpose**: Analyze actual quotes from calls to identify language patterns

**What it does**:
- Compares quotes from high-scoring vs low-scoring calls
- Identifies specific phrases that work well
- Finds common mistakes or problematic language
- Extracts actionable insights for reps

**Value**: Provides concrete examples of what to say/avoid

**Estimated Cost**: ~$0.05-0.10

---

### 3. **Skill-Specific Deep Dive: "Discover the Why"** ✅
**Purpose**: Deep analysis of the weakest skill (2.63/5.0 average)

**What it does**:
- Analyzes what worked in high-scoring discovery calls
- Identifies the 3 most critical gaps
- Provides specific, actionable coaching recommendations
- Creates prioritized training plan

**Value**: Targeted improvement plan for the most critical skill gap

**Estimated Cost**: ~$0.08-0.12

---

### 4. **Temporal Decline Root Cause Analysis** ✅
**Purpose**: Understand why performance declined 24.6 percentage points over time

**What it does**:
- Compares recommendations from early (high performance) vs late (low performance) periods
- Identifies key differences in feedback
- Generates hypotheses for root causes
- Provides intervention recommendations

**Value**: Critical for addressing the performance decline

**Estimated Cost**: ~$0.08-0.12

---

### 5. **User-Specific Coaching Recommendations** ✅
**Purpose**: Compare top vs bottom performers to create targeted coaching

**What it does**:
- Analyzes differences between 51% win rate vs 22% win rate rep
- Creates specific coaching plan for bottom performer
- Identifies what to learn from top performer
- Prioritizes skill development

**Value**: Personalized coaching plans for individual reps

**Estimated Cost**: ~$0.08-0.12

---

### 6. **Impact Text Analysis** ✅
**Purpose**: Understand what behaviors actually drive wins

**What it does**:
- Compares impact descriptions from won vs lost deals
- Identifies common themes in successful calls
- Finds language patterns that predict success
- Extracts actionable insights

**Value**: Identifies the behaviors that matter most for outcomes

**Estimated Cost**: ~$0.05-0.10

---

## Additional Recommended Analyses (Not Yet Implemented)

### 7. **Recommendation Effectiveness Tracking**
**Purpose**: Track if implementing recommendations leads to score improvements

**Approach**: 
- For each rep, compare recommendations given in period 1 with scores in period 2
- Use LLM to identify which recommendations were likely implemented
- Correlate with score improvements

**Estimated Cost**: ~$0.15-0.20

---

### 8. **Citation Sentiment & Emotion Analysis**
**Purpose**: Understand emotional tone and its impact on outcomes

**Approach**:
- Analyze sentiment of quotes from high vs low scoring calls
- Identify emotional patterns (empathy, urgency, confidence, etc.)
- Correlate with outcomes

**Estimated Cost**: ~$0.10-0.15

---

### 9. **Skill Interaction Analysis**
**Purpose**: Understand how skills work together

**Approach**:
- For calls with multiple skills evaluated, analyze how recommendations interact
- Identify skill combinations that are particularly effective
- Create training programs that leverage skill synergies

**Estimated Cost**: ~$0.12-0.18

---

### 10. **Personalized Coaching Briefs**
**Purpose**: Generate individual coaching briefs for each rep

**Approach**:
- For each rep, aggregate all their recommendations and impacts
- Use LLM to create a personalized coaching brief
- Include strengths, weaknesses, and prioritized action plan

**Estimated Cost**: ~$0.20-0.30 (for all 5 reps)

---

## Cost Estimates

**Implemented Analyses (1-6)**: ~$0.40-0.65 total
- Well within the $100 budget
- Provides comprehensive insights

**Additional Analyses (7-10)**: ~$0.57-0.83 total
- Can be run if budget allows
- Provides deeper, more personalized insights

**Total Budget**: $100
**Recommended Usage**: 
- Run analyses 1-6 first (~$0.50)
- If valuable, run additional analyses 7-10 (~$0.60)
- Reserve ~$0.40 for iterations/refinements

## How to Run

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the LLM analysis**:
```bash
python llm_analysis.py
```

3. **View formatted results**:
```bash
python format_llm_results.py
```

4. **Review results**:
- Results are saved to `llm_analysis_results.json`
- Formatted output shows all insights
- Cost tracking shows budget usage

## Tips for Maximizing Value

1. **Start with implemented analyses (1-6)**: These provide the most value for cost
2. **Review results before running additional analyses**: Make sure the insights are useful
3. **Iterate on prompts**: If results aren't specific enough, refine the prompts
4. **Combine with quantitative analysis**: LLM insights complement the statistical analysis
5. **Use for presentation**: LLM insights provide concrete examples and recommendations

## Expected Outputs

Each analysis provides:
- **Structured insights**: Clear themes and patterns
- **Actionable recommendations**: Specific steps to improve
- **Examples**: Concrete quotes or behaviors
- **Prioritization**: What matters most

These can be directly incorporated into your presentation and coaching programs.

