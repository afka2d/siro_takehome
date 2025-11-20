# Siro DS Takehome - Final Summary for PowerPoint
## 6-Slide Analysis with Supporting Data, Visualizations, and Code References

---

## SLIDE 1: Executive Summary

### Insight
**Dataset Overview:** 150 sales conversations across 5 representatives from Bob's Builders, with 993 skill evaluations across 7 core sales skills. Overall win rate: 40% (60 won, 90 lost).

**⚠️ Critical Finding:** Performance declined significantly over time - win rate dropped from 64% to 40% and skill scores declined by 15%.

### Supporting Data Points
- Total recordings: 150
- Total users: 5
- Total skill evaluations: 993
- Unique skills: 7
- Overall win rate: 40.00%
- Average call duration: 54.92 minutes
- Average skill score: 3.34/5.0
- Date range: August 6 - September 28, 2025
- First week win rate: 64.29%
- Last week win rate: 39.64%
- First week skill score: 4.10
- Last week skill score: 3.50

### Visualization
- **Chart 1:** Outcome Distribution (`chart_01_outcome_distribution.png`)
- **Chart 6:** Win Rate Over Time (`chart_06_win_rate_over_time.png`)

### Code Location
- **Data loading & summary stats:** [analysis.py#L33-L111](https://github.com/afka2d/siro_takehome/blob/main/analysis.py#L33-L111)
- **Temporal analysis:** [analysis.py#L94-L111](https://github.com/afka2d/siro_takehome/blob/main/analysis.py#L94-L111)

---

## SLIDE 2: Skill Scores Strongly Predict Outcomes

### Insight
Skill scores are consistently higher for won deals across all 7 evaluated skills. The LLM grader effectively identifies skills that correlate with successful outcomes.

### Supporting Data Points
**Skill Score Comparison (Won vs Lost):**
- **Demonstration:** Won = 4.20 vs Lost = 3.02 (+39% improvement)
- **Negotiation:** Won = 4.15 vs Lost = 2.84 (+46% improvement)
- **Discover the "Why":** Won = 3.02 vs Lost = 2.36 (+28% improvement)
- **Make a Friend:** Won = 4.24 vs Lost = 3.99 (+6% improvement)
- **Overcome Objections:** Won = 3.83 vs Lost = 3.46 (+11% improvement)
- **Secure the Sale:** Won = 3.32 vs Lost = 2.83 (+17% improvement)
- **Value Proposition:** Won = 3.20 vs Lost = 3.10 (+3% improvement)

### Visualization
- **Chart 2:** Skill Scores by Outcome (`chart_02_skill_scores_by_outcome.png`)
  - Horizontal bar chart comparing won/lost scores for each skill

### Code Location
- **Calculation:** [analysis.py#L120-L133](https://github.com/afka2d/siro_takehome/blob/main/analysis.py#L120-L133)
- **Visualization:** [analysis.py#L280-L295](https://github.com/afka2d/siro_takehome/blob/main/analysis.py#L280-L295)

---

## SLIDE 3: "Discover the Why" is the Weakest Skill

### Insight
"Discover the Why" has the lowest average score (2.63/5.0) across all reps and shows high variability. This foundational skill needs immediate attention.

### Supporting Data Points
- **Average score: 2.63/5.0** (lowest of all 7 skills)
- **Won deals:** 3.02/5.0
- **Lost deals:** 2.36/5.0
- **Standard deviation:** 1.21 (high variability)
- **Score 1 frequency:** 33 records (23.2% of evaluations)
- **Score 5 frequency:** 10 records (7.0% of evaluations)

### Visualization
- **Chart 4:** Average Skill Scores (`chart_04_average_skill_scores.png`)
  - Shows "Discover the Why" at the bottom of the skill rankings (2.63/5.0)

### Code Location
- **Skill statistics:** [analysis.py#L134-L167](https://github.com/afka2d/siro_takehome/blob/main/analysis.py#L134-L167)
- **LLM deep dive:** [llm_analysis.py#L108-L149](https://github.com/afka2d/siro_takehome/blob/main/llm_analysis.py#L108-L149)

### LLM Insights
- **Critical gaps:** Lack of direct motivation questions, absence of summaries, early incentive discussions
- **Example questions:** "Can you tell me more about what is motivating your decision to move?"
- **Source:** `llm_analysis_results.json` - "discover_why_analysis"

---

## SLIDE 4: Question Strategy Differs Between Won and Lost Deals

### Insight
In successful deals, reps ask more questions and maintain a higher rep-to-customer question ratio, suggesting better discovery and active listening.

### Supporting Data Points
**Won Deals:**
- Rep questions: 47.76 (average)
- Customer questions: 23.76 (average)
- Ratio: 2.0 rep questions per customer question

**Lost Deals:**
- Rep questions: 44.25 (average)
- Customer questions: 28.95 (average)
- Ratio: 1.5 rep questions per customer question

**Difference:**
- Rep asks 3.5 more questions in won deals
- Customer asks 5.2 fewer questions in won deals

### Visualization
- **Chart 3:** Average Questions by Outcome (`chart_03_questions_by_outcome.png`)
  - Bar chart showing rep questions vs customer questions for won/lost

### Code Location
- **Calculation:** [analysis.py#L168-L206](https://github.com/afka2d/siro_takehome/blob/main/analysis.py#L168-L206)
- **Visualization:** [analysis.py#L300-L315](https://github.com/afka2d/siro_takehome/blob/main/analysis.py#L300-L315)

---

## SLIDE 5: Significant Performance Variation Across Reps

### Insight
Win rates vary dramatically across reps (2.4x difference), suggesting significant opportunity for peer learning and knowledge transfer.

### Supporting Data Points
| User ID (abbreviated) | Recordings | Win Rate | Avg Skill Score |
|----------------------|------------|----------|-----------------|
| WQwSd6yv... | 43 | **51.2%** | 3.24 |
| heNyGaoq... | 22 | 40.9% | 3.20 |
| Rw4mGh6M... | 27 | 40.7% | 3.20 |
| FidcsnIQ... | 35 | 37.1% | 3.11 |
| Zbd0Y2ic... | 23 | **21.7%** | 3.00 |

**Key Metrics:**
- **2.4x difference** between highest (51.2%) and lowest (21.7%) win rates
- Top performer handles 29% of all recordings
- Bottom performer has similar skill scores but much lower win rate

### Visualization
- **Chart 5:** User Win Rates (`chart_05_user_win_rates.png`)
  - Horizontal bar chart showing win rates for each user (ranges from 21.7% to 51.2%)

### Code Location
- **User statistics:** [analysis.py#L207-L246](https://github.com/afka2d/siro_takehome/blob/main/analysis.py#L207-L246)
- **Visualization:** [analysis.py#L320-L335](https://github.com/afka2d/siro_takehome/blob/main/analysis.py#L320-L335)

---

## SLIDE 6: Performance Decline Over Time - Deep Dive with LLM Insights

### Insight
Both skill scores and win rates declined significantly over the analysis period. LLM analysis of recommendations and impacts reveals a shift from relationship-building to transactional approaches, explaining the decline.

### Supporting Data Points
**Temporal Decline:**
- **Skill Scores:** First week = 4.10 → Last week = 3.50 (**-15% decline**)
- **Win Rate:** First week = 64.29% → Last week = 39.64% (**-24.6 percentage points**)
- **Change:** -0.60 points in skill scores, -24.64% in win rate

**Early Period (Aug 6-15, Higher Performance):**
- Average skill score: 4.10
- Win rate: 64.29%
- Focus: Building authentic connections, systematic discovery, transparent pricing

**Late Period (Sep 15-28, Lower Performance):**
- Average skill score: 3.50
- Win rate: 39.64%
- Focus: Sustaining rapport, improving discovery, direct closing

### Visualization
- **Chart 6:** Win Rate Over Time (`chart_06_win_rate_over_time.png`)
  - Line chart showing win rate declining from 64.29% to 39.64%

### Code Location
- **Temporal analysis:** [analysis.py#L94-L111](https://github.com/afka2d/siro_takehome/blob/main/analysis.py#L94-L111)
- **LLM root cause analysis:** [llm_analysis.py#L150-L194](https://github.com/afka2d/siro_takehome/blob/main/llm_analysis.py#L150-L194)

### LLM Insights - Root Causes Identified

**1. Shift from Relationship-Building to Transactional Approach**
- Early period: Emphasized asking permission, connecting features to lifestyle needs, building rapport through personal questions
- Late period: Focused on securing permission to question, deferring incentives, deepening discovery
- **Impact:** Reduced trust and connection with customers

**2. Less Name Usage and Personalization**
- Early period: Consistent use of customer names, personalized conversations
- Late period: Reduced name usage and personalization
- **Impact:** Lower customer trust and engagement during interactions

**3. Failure to Secure Explicit Agreement**
- Early period: Confirmed resolution of objections, gained progressive agreement
- Late period: Failed to secure explicit agreement on price and timing
- **Impact:** Ambiguity and hesitations from customers, missed sales opportunities

**4. Missing Clear Closing Questions**
- Early period: Included confirming resolution of objections
- Late period: Suggested converting education into clear close but lacked follow-up confirmation
- **Impact:** Lack of commitment from customers, missed sales opportunities

### Immediate Intervention Recommendations
1. **Implement training program** emphasizing building authentic connections, understanding customer motivations, and securing explicit agreement
2. **Encourage name usage and personalization** in interactions to enhance trust and rapport
3. **Develop structured approach** to early discovery, including securing permission to question and uncovering emotional drivers before discussing incentives
4. **Provide guidance** on incorporating clear closing questions and follow-up confirmation to ensure commitment

### Source
- **LLM Analysis:** `llm_analysis_results.json` - "temporal_decline"
- **Code:** [llm_analysis.py#L150-L194](https://github.com/afka2d/siro_takehome/blob/main/llm_analysis.py#L150-L194)

---

## Quick Reference: Visualization Files

1. `chart_01_outcome_distribution.png` - Outcome Distribution
2. `chart_02_skill_scores_by_outcome.png` - Skill Scores by Outcome
3. `chart_03_questions_by_outcome.png` - Average Questions by Outcome
4. `chart_04_average_skill_scores.png` - Average Skill Scores
5. `chart_05_user_win_rates.png` - User Win Rates
6. `chart_06_win_rate_over_time.png` - Win Rate Over Time

## Quick Reference: Code Files

- **Main Analysis:** `analysis.py` - All quantitative analysis and visualizations
- **LLM Analysis:** `llm_analysis.py` - Text analysis using OpenAI API
- **Supporting:** `deep_analysis.py` - Additional analysis functions (if needed)

---

*Document prepared for PowerPoint presentation. All code, data, and visualizations available in the repository.*
