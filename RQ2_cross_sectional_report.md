# RQ2 Cross-Sectional Analysis: Factors Associated with Self-Reported Impact on Desire to Pursue a Graduate Degree

## Scope and interpretation guardrails
- This is a **one-time cross-sectional survey**; results are described as factors **associated with / linked to / predictive of / correlated with** the outcome, not causal effects.
- The outcome uses respondents' wording of how the pathway **"impacted"** desire; this analysis treats that as **self-reported perceived impact**.
- Analysis sample: 141 completed, consented, non-duplicate responses with non-missing outcome.

## Outcome variable
Outcome question: *How has the availability of (or knowledge about) the alternative pathway to CPA licensure impacted your desire to pursue a graduate degree (MAcc or MBA)?*

Outcome coding (for association metrics only): significantly decreased = -2, decreased = -1, no change = 0, increased = +1, significantly increased = +2.

## Required group comparisons

### Awareness before survey (Q53)
- **No** (n=55): mean perceived-impact score = 0.382. Significantly decreased desire: 1 (1.8%); Decreased desire: 2 (3.6%); No change in desire: 28 (50.9%); Increased desire: 23 (41.8%); Significantly increased desire: 1 (1.8%).
- **Yes** (n=86): mean perceived-impact score = -0.477. Significantly decreased desire: 12 (14.0%); Decreased desire: 30 (34.9%); No change in desire: 34 (39.5%); Increased desire: 7 (8.1%); Significantly increased desire: 3 (3.5%).
- Difference in means (Aware Yes - No): **-0.859**.

### Undergraduate vs graduate status (Q27)
- **Undergraduate** (n=141): mean perceived-impact score = -0.142. Significantly decreased desire: 13 (9.2%); Decreased desire: 32 (22.7%); No change in desire: 62 (44.0%); Increased desire: 30 (21.3%); Significantly increased desire: 4 (2.8%).
- **Data limitation:** no graduate respondents had non-missing data on the main outcome (Q52), likely due survey skip logic. Direct undergrad-vs-grad comparison on the exact outcome is therefore not estimable.

## Overall ranked associations with the outcome
Metric shown = absolute association strength (|r| for ordinal/binary predictors, eta for nominal predictors). Sign indicates direction only when ordinal/binary coding is available.

| Rank | Predictor | Type | n | Strength | Direction |
|---:|---|---|---:|---:|---|
| 1 | Aware of alternative pathway before survey | ordinal/binary | 141 | 0.441 | Negative |
| 2 | School state | nominal | 141 | 0.308 | NA |
| 3 | Belief grad degree increases lifetime earnings (undergrad branch) | ordinal/binary | 140 | 0.242 | Positive |
| 4 | Belief grad degree increases lifetime earnings (combined branches) | ordinal/binary | 140 | 0.242 | Positive |
| 5 | Work at CPA firm | ordinal/binary | 141 | 0.220 | Negative |
| 6 | Likelihood of pursuing CPA | ordinal/binary | 141 | 0.195 | Negative |
| 7 | Importance: CPA exam preparation | ordinal/binary | 141 | 0.185 | Negative |
| 8 | Undergraduate major | nominal | 141 | 0.168 | NA |
| 9 | Full-time (vs part-time) student | ordinal/binary | 141 | 0.168 | Negative |
| 10 | Importance: soft-skill development | ordinal/binary | 141 | 0.167 | Positive |
| 11 | Importance: internship/recruiting opportunities | ordinal/binary | 141 | 0.153 | Positive |
| 12 | Importance: technical accounting coursework | ordinal/binary | 141 | 0.146 | Positive |
| 13 | Work >20 hours/week in accounting | ordinal/binary | 141 | 0.113 | Negative |
| 14 | Importance: networking opportunities | ordinal/binary | 141 | 0.078 | Positive |
| 15 | Importance: online/flexible learning | ordinal/binary | 141 | 0.064 | Positive |

### Key reading of strongest links
- Positive direction means higher predictor values align with reporting a higher (more increased) perceived impact on desire to pursue graduate school.
- Negative direction means higher predictor values align with reporting lower (more decreased) perceived impact.
- Direct item availability note: this dataset does not include a single explicit Likert item for "graduate school is not worth the cost/time" or a direct standalone item phrased as "alternative pathway makes graduate school less necessary"; nearest available indicators are ROI beliefs and the main outcome itself.

## Focus sections requested
### ROI belief items
- Belief grad degree increases lifetime earnings (combined branches): strength=0.242, direction=Positive, n=140.

### Graduate program quality importance items
- Importance: CPA exam preparation: strength=0.185, direction=Negative, n=141.
- Importance: soft-skill development: strength=0.167, direction=Positive, n=141.
- Importance: internship/recruiting opportunities: strength=0.153, direction=Positive, n=141.
- Importance: technical accounting coursework: strength=0.146, direction=Positive, n=141.
- Importance: networking opportunities: strength=0.078, direction=Positive, n=141.
- Importance: online/flexible learning: strength=0.064, direction=Positive, n=141.
- Importance: faculty interaction/mentorship: strength=0.042, direction=Positive, n=141.
- Importance: specialized tracks/credentials: strength=0.039, direction=Negative, n=141.

## Graduate-student-only version (recommended)
Using the exact main outcome (Q52), graduate-only sample is n=0.

| Rank | Predictor | n | Strength | Direction |
|---:|---|---:|---:|---|

### Graduate-only fallback outcome (Q35)
Because Q52 is missing for graduate respondents, this fallback uses graduate-only question Q35: *how likely they would have been to pursue a graduate degree if they had known about the alternative pathway before beginning*.
Grad fallback sample (Q35) n=37.

| Rank | Predictor | n | Strength | Direction |
|---:|---|---:|---:|---|
| 1 | 150-credit requirement influence on enrolling | 37 | 0.536 | Negative |
| 2 | Agree grad degree helps move up career ladder faster | 37 | 0.403 | Positive |
| 3 | Job offer in accounting near graduation | 37 | 0.353 | Negative |
| 4 | Employer requires/encourages graduate degree | 37 | 0.167 | Negative |
| 5 | Agree grad degree may delay advancement | 37 | 0.146 | Negative |
| 6 | Program type (MAcc/MBA/Other) | 37 | 0.004 | Positive |

### Graduate-only interpretation highlights
- Treat estimates as descriptive associations only due to cross-sectional design and small grad-only sample size.
- Program-type/modality results are exploratory because nearly all grad respondents are in MAcc and mostly/fully online formats.
