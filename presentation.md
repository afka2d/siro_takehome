# Siro DS Takehome Assignment
## Sales Conversation Analysis - Key Findings

---

## Executive Summary

**Dataset Overview:**
- **150 sales conversations** across **5 representatives** from Bob's Builders
- **993 skill evaluations** across **7 core sales skills**
- **Time period:** August 6 - September 28, 2025
- **Overall win rate:** 40% (60 won, 90 lost)

**⚠️ Critical Finding:** Performance declined significantly over time - win rate dropped from 64% to 40% and skill scores declined by 15%. This warrants immediate investigation.

---

## Key Finding #1: Skill Scores Strongly Predict Outcomes

### The Pattern
Skill scores are **consistently higher for won deals** across all 7 evaluated skills. The gap is most pronounced in:

- **Demonstration:** Won = 4.20 vs Lost = 3.02 (+39% improvement)
- **Negotiation:** Won = 4.15 vs Lost = 2.84 (+46% improvement)
- **Discover the "Why":** Won = 3.02 vs Lost = 2.36 (+28% improvement)

### What This Means
The LLM grader is effectively identifying skills that correlate with successful outcomes. This suggests:
- **Coaching opportunity:** Focus training on skills with largest gaps (Demonstration, Negotiation)
- **Early warning system:** Low scores in these areas could flag at-risk deals
- **Validation:** The scoring system appears to measure meaningful sales behaviors

---

## Key Finding #2: "Discover the Why" is the Weakest Skill Across All Reps

### The Data
- **Average score: 2.63/5.0** (lowest of all 7 skills)
- **Won deals:** 3.02/5.0
- **Lost deals:** 2.36/5.0
- **Standard deviation:** 1.21 (high variability)

### Why This Matters
"Discover the Why" is foundational to understanding customer motivation. Low scores here suggest:
- Reps may be jumping to solutions before understanding needs
- Emotional drivers aren't being fully explored
- Opportunity to improve discovery questioning techniques

### Recommendation
Prioritize training on discovery techniques, especially:
- Asking permission to ask questions
- Probing emotional motivations
- Using "Anything else?" to capture all dissatisfiers
- Summarizing customer motivations before presenting solutions

---

## Key Finding #3: Question Strategy Differs Between Won and Lost Deals

### The Pattern
**Won deals:**
- Rep asks **47.8 questions** (avg)
- Customer asks **23.8 questions** (avg)
- **Ratio: 2.0 rep questions per customer question**

**Lost deals:**
- Rep asks **44.3 questions** (avg)
- Customer asks **29.0 questions** (avg)
- **Ratio: 1.5 rep questions per customer question**

### Interpretation
In successful deals, reps are more proactive with questions, suggesting:
- **Better discovery:** More questions = deeper understanding
- **Customer engagement:** Fewer customer questions might indicate clearer communication
- **Active listening:** Higher rep question count may reflect better follow-up on customer responses

### Actionable Insight
Encourage reps to ask **more questions** during discovery, especially follow-up questions that probe deeper into motivations and concerns.

---

## Key Finding #4: Significant Performance Variation Across Reps

### User Performance Breakdown

| User ID | Recordings | Win Rate | Avg Skill Score | Key Strength |
|---------|-----------|----------|-----------------|--------------|
| WQwSd6yvYtevHdM8h6sGlHwkV1n2 | 43 | **51.2%** | 3.24 | Highest win rate |
| heNyGaoqdcfPKrcrXefMqI77U3E3 | 22 | 40.9% | 3.20 | Strong Demonstration (4.10) |
| Rw4mGh6MEYMbLJKjdtjjnZcoLXD3 | 27 | 40.7% | 3.20 | Strong Value Prop (3.67) |
| FidcsnIQajfiMi8hZBkkJtoOOOz2 | 35 | 37.1% | 3.11 | Balanced performance |
| Zbd0Y2ic8zVKmi7gOK2p8jEiiZh2 | 23 | **21.7%** | 3.00 | Needs improvement |

### Insights
- **2.4x difference** between highest and lowest win rates
- Top performer (WQwSd6yvYtevHdM8h6sGlHwkV1n2) handles 29% of all recordings
- Bottom performer (Zbd0Y2ic8zVKmi7gOK2p8jEiiZh2) has lowest win rate but similar skill scores, suggesting:
  - Possible issue with deal qualification
  - Timing/closing skills may need work
  - Could benefit from shadowing top performer

---

## Key Finding #5: "Make a Friend" is the Strongest Skill

### The Data
- **Average score: 4.09/5.0** (highest of all skills)
- **Lowest variability:** std = 0.84 (most consistent)
- **Won deals:** 4.24/5.0
- **Lost deals:** 3.99/5.0

### What This Tells Us
Reps are consistently strong at:
- Building rapport
- Using customer names
- Expressing gratitude
- Creating warm, friendly interactions

### The Opportunity
Since relationship-building is strong, the focus should shift to:
- **Converting rapport into sales:** Leverage strong relationships to better understand needs
- **Discovery:** Use the established rapport to ask deeper questions
- **Closing:** Build on the relationship to secure commitments

---

## Key Finding #6: Performance Declined Over Time ⚠️

### The Critical Pattern
**Both skill scores and win rates declined significantly over the analysis period:**

- **Skill Scores:** First week average = 4.10 → Last week average = 3.50 (**-15% decline**)
- **Win Rate:** First week = 64.29% → Last week = 39.64% (**-24.6 percentage points**)

### What This Suggests
This temporal decline could indicate:
- **Burnout or fatigue:** Reps may be experiencing decreased engagement over time
- **Market conditions:** External factors (seasonality, competition) affecting outcomes
- **Training effectiveness:** Initial training may not be sustained
- **Data quality:** Possible changes in recording quality or evaluation criteria

### Immediate Action Required
This is a **red flag** that warrants immediate investigation:
1. **Root cause analysis:** Interview reps to understand what changed
2. **Review training:** Check if training programs were discontinued
3. **Market analysis:** Examine external factors (competition, seasonality)
4. **Intervention:** Consider refresher training or coaching support

---

## Additional Observations

### Call Duration
- **Average:** 54.9 minutes
- No significant correlation between duration and outcome
- Suggests quality of conversation matters more than length

### Speaking Ratio
- **Average:** 76% (reps speak 76% of conversation time)
- Won deals: 77.5%
- Lost deals: 75.2%
- Minimal difference suggests balance is less important than content

### Word Count
- **Average:** 4,956 words per call
- Higher word count correlates with longer calls (r=0.81)
- No direct correlation with outcome

### Skill Correlations
Strong correlations between related skills suggest skill clusters:
- **Overcome Objections ↔ Secure the Sale:** r = 0.57 (strongest)
- **Demonstration ↔ Overcome Objections:** r = 0.56
- **Demonstration ↔ Secure the Sale:** r = 0.55

This suggests that improving one skill in a cluster may have positive spillover effects on related skills.

---

## Recommendations for Sales Coaching

### Priority 1: Investigate Performance Decline ⚠️ URGENT
- **Why:** Win rate dropped 24.6 percentage points and skill scores declined 15% over time
- **How:**
  - Conduct root cause analysis with reps and management
  - Review training programs and check for discontinuation
  - Analyze market conditions and external factors
  - Implement immediate intervention (refresher training, coaching support)
  - Monitor weekly performance metrics going forward

### Priority 2: Improve "Discover the Why"
- **Why:** Lowest average score (2.63) with high impact on outcomes; 39.4% of evaluations need improvement
- **How:** 
  - Training on structured discovery frameworks
  - Practice with emotional-level questioning
  - Role-play exercises on permission-based questioning
  - Focus on deferring incentives until needs are understood

### Priority 3: Strengthen Demonstration Skills
- **Why:** Largest gap between won (4.20) and lost (3.02) deals
- **How:**
  - Focus on gaining explicit agreement at each stage
  - Room-by-room closing techniques
  - Community and homesite selection confirmation
  - Leverage skill correlation with Overcome Objections (r=0.56)

### Priority 4: Enhance Negotiation Capabilities
- **Why:** Second-largest gap (won: 4.15 vs lost: 2.84)
- **How:**
  - Negotiation frameworks and techniques
  - Objection handling practice
  - Value-based negotiation training
  - Leverage correlation with Secure the Sale (r=0.54)

### Priority 5: Peer Learning Program
- **Why:** 2.4x performance variation suggests knowledge transfer opportunity
- **How:**
  - Pair top performer (51% win rate) with bottom performer (22% win rate)
  - Shadowing and call review sessions
  - Best practice sharing sessions
  - Focus on skill clusters (e.g., Overcome Objections + Secure the Sale)

---

## Questions for Further Exploration

1. **Temporal decline root cause:** What caused the 24.6 percentage point drop in win rate? Was it:
   - Training discontinuation?
   - Market/seasonal factors?
   - Rep burnout or turnover?
   - Changes in evaluation criteria?
   - Changes in customer mix?

2. **Skill interactions:** Can we leverage skill correlations (e.g., Overcome Objections ↔ Secure the Sale, r=0.57) to create targeted training programs that improve multiple skills simultaneously?

3. **Customer segments:** Are there different skill requirements for different customer types? Do certain skills matter more for specific customer profiles?

4. **Citation analysis:** Can we extract patterns from the 17.8 average citations per evaluation to identify specific behaviors that drive high vs. low scores?

5. **Recommendation effectiveness:** What are the most common recommendations, and can we track if implementing them leads to score improvements?

6. **Score distribution insights:** Why does "Discover the Why" have 23.2% score 1s while "Make a Friend" has 34.8% score 5s? What makes one skill consistently strong and another consistently weak?

7. **User-specific patterns:** The top performer (51% win rate) has lower average skill scores (3.26) than some lower performers. What other factors (deal qualification, timing, closing ability) might explain this?

---

## Technical Notes

- **Data quality:** High - 993 evaluations with 967 containing citations
- **Coverage:** 142 of 150 recordings have skill evaluations (95% coverage)
- **Scoring consistency:** Scores range 1-5 with reasonable distribution
- **Missing data:** Minimal - only 5 recordings missing conversation metrics

---

## Conclusion

The data reveals clear patterns connecting sales skills to outcomes. The LLM grader appears to be identifying meaningful behaviors, with skill scores showing strong predictive power. The biggest opportunities lie in improving discovery techniques ("Discover the Why") and demonstration skills, while leveraging the existing strength in relationship-building ("Make a Friend").

The significant performance variation across reps suggests a peer learning program could yield substantial improvements, particularly for the bottom performer who could benefit from shadowing the top performer.

---

*Analysis completed using Python with pandas, matplotlib, and seaborn. Full code and visualizations available in `analysis.py` and `analysis_visualizations.png`.*

