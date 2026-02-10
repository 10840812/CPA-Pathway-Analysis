import csv
import math
from collections import Counter, defaultdict
from statistics import mean

DATA_FILE = "Alternative CPA Pathways Survey_December 31, 2025_09.45.csv"
REPORT_FILE = "RQ2_cross_sectional_report.md"

LIKERT_IMPACT = {
    "Significantly decreased desire": -2,
    "Decreased desire": -1,
    "No change in desire": 0,
    "Increased desire": 1,
    "Significantly increased desire": 2,
}

CPA_LIKELY = {
    "Very unlikely": 1,
    "Somewhat unlikely": 2,
    "Neither likely nor unlikely": 3,
    "Somewhat likely": 4,
    "Very likely": 5,
}

AGREE = {
    "Strongly disagree": 1,
    "Somewhat disagree": 2,
    "Neither agree nor disagree": 3,
    "Somewhat agree": 4,
    "Strongly agree": 5,
}

IMPORTANCE = {
    "Not at all important": 1,
    "Slightly important": 2,
    "Moderately important": 3,
    "Very important": 4,
    "Extremely important": 5,
}

YES_NO = {"No": 0, "Yes": 1}

EARNINGS = {
    "Definitely not": 1,
    "Probably not": 2,
    "Might or might not": 3,
    "Probably yes": 4,
    "Definitely yes": 5,
}

INFLUENCE_150 = {
    "It had no influence on my decision to pursue a graduate program.": 1,
    "It was a minor factor in my decision to pursue a graduate program.": 2,
    "It was a significant factor among others in my decision to pursue a graduate program.": 3,
    "It was the primary factor in my decision to pursue a graduate program.": 4,
    "It was the only reason I chose to pursue a graduate program.": 5,
}

SATISFACTION = {
    "Extremely dissatisfied": 1,
    "Somewhat dissatisfied": 2,
    "Neither satisfied nor dissatisfied": 3,
    "Somewhat satisfied": 4,
    "Extremely satisfied": 5,
}

LIKELY_GRAD_IF_KNEW = {
    "Extremely unlikely": 1,
    "Somewhat unlikely": 2,
    "Neither likely nor unlikely": 3,
    "Somewhat likely": 4,
    "Extremely likely": 5,
}

PROGRAM_MODALITY = {
    "Fully or mostly in person": 0,
    "Fully or mostly online": 1,
}

PROGRAM_TYPE = {
    "MAcc": 1,
    "MBA": 2,
    "Other": 3,
}

WORKING_STATUS = {
    "Part-time": 0,
    "Full-time": 1,
}

MAJOR = {
    "Accounting": 1,
    "Other Business / Non-accounting": 2,
    "Other Non-business": 3,
}

STATE = {
    "Utah": 0,
    "Texas": 1,
}


def is_valid_response(row):
    rid = row.get("ResponseId", "")
    if not rid.startswith("R_"):
        return False
    if row.get("Finished") != "True":
        return False
    if row.get("Q61") != "Yes":
        return False
    # Remove duplicate responses the survey itself flags.
    if row.get("Q28") == "Yes":
        return False
    if row.get("Q52", "") not in LIKERT_IMPACT:
        return False
    return True


def pearsonr(x, y):
    n = len(x)
    if n < 3:
        return None
    mx = mean(x)
    my = mean(y)
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return None
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / math.sqrt(sxx * syy)


def corr_ratio(categories, values):
    # eta (correlation ratio) for nominal categorical -> numeric outcome
    if len(values) < 3:
        return None
    overall = mean(values)
    groups = defaultdict(list)
    for c, v in zip(categories, values):
        groups[c].append(v)
    if len(groups) < 2:
        return None
    ss_between = sum(len(g) * (mean(g) - overall) ** 2 for g in groups.values())
    ss_total = sum((v - overall) ** 2 for v in values)
    if ss_total == 0:
        return None
    return math.sqrt(ss_between / ss_total)


def summarize_group(rows, group_col):
    out = {}
    for g in sorted(set(r[group_col] for r in rows if r.get(group_col))):
        sub = [r for r in rows if r.get(group_col) == g]
        y = [LIKERT_IMPACT[r["Q52"]] for r in sub]
        dist = Counter(r["Q52"] for r in sub)
        out[g] = {
            "n": len(sub),
            "mean": mean(y),
            "dist": dist,
        }
    return out


def encode(rows, col, mapping):
    x, y = [], []
    for r in rows:
        v = r.get(col, "")
        if v in mapping:
            x.append(mapping[v])
            y.append(LIKERT_IMPACT[r["Q52"]])
    return x, y


def assoc_ordinal(rows, col, mapping, label):
    x, y = encode(rows, col, mapping)
    r = pearsonr(x, y)
    return {
        "predictor": label,
        "type": "ordinal/binary",
        "n": len(x),
        "metric": abs(r) if r is not None else None,
        "signed": r,
    }


def assoc_nominal(rows, col, label):
    cats, vals = [], []
    for r in rows:
        v = r.get(col, "")
        if v:
            cats.append(v)
            vals.append(LIKERT_IMPACT[r["Q52"]])
    e = corr_ratio(cats, vals)
    return {
        "predictor": label,
        "type": "nominal",
        "n": len(cats),
        "metric": e,
        "signed": None,
    }


def fmt(x, digits=3):
    if x is None:
        return "NA"
    return f"{x:.{digits}f}"


with open(DATA_FILE, newline="", encoding="utf-8-sig") as fh:
    rows = list(csv.DictReader(fh))

analysis_rows = [r for r in rows if is_valid_response(r)]

# Main subgroup comparisons
aware_stats = summarize_group(analysis_rows, "Q53")
student_stats = summarize_group(analysis_rows, "Q27")

associations = []

# A) awareness/exposure
associations.append(assoc_ordinal(analysis_rows, "Q53", YES_NO, "Aware of alternative pathway before survey"))
associations.append(assoc_ordinal(analysis_rows, "Q31", YES_NO, "(Grad-only item) aware before beginning graduate program"))

# B) CPA direction
associations.append(assoc_ordinal(analysis_rows, "Q29", CPA_LIKELY, "Likelihood of pursuing CPA"))
associations.append(assoc_ordinal(analysis_rows, "Q51", LIKERT_IMPACT, "Perceived impact on desire to pursue CPA"))

# C) ROI beliefs
associations.append(assoc_ordinal(analysis_rows, "Q33", AGREE, "Agree grad degree helps move up career ladder faster"))
associations.append(assoc_ordinal(analysis_rows, "Q34", AGREE, "Agree grad degree may delay advancement"))
associations.append(assoc_ordinal(analysis_rows, "Q55", EARNINGS, "Belief grad degree increases lifetime earnings (undergrad branch)"))
associations.append(assoc_ordinal(analysis_rows, "Q44", EARNINGS, "Belief grad degree increases lifetime earnings (grad branch)"))

# D) Importance ratings
importance_labels = {
    "Q39_1": "Importance: CPA exam preparation",
    "Q39_2": "Importance: networking opportunities",
    "Q39_3": "Importance: faculty interaction/mentorship",
    "Q39_4": "Importance: technical accounting coursework",
    "Q39_5": "Importance: soft-skill development",
    "Q39_6": "Importance: internship/recruiting opportunities",
    "Q39_7": "Importance: online/flexible learning",
    "Q39_8": "Importance: specialized tracks/credentials",
}
for col, label in importance_labels.items():
    associations.append(assoc_ordinal(analysis_rows, col, IMPORTANCE, label))

# E) Work/employer context
associations.append(assoc_ordinal(analysis_rows, "Q46", YES_NO, "Work >20 hours/week in accounting"))
associations.append(assoc_ordinal(analysis_rows, "Q47", YES_NO, "Work at CPA firm"))
associations.append(assoc_ordinal(analysis_rows, "Q49", YES_NO, "Employer requires/encourages graduate degree"))
associations.append(assoc_ordinal(analysis_rows, "Q48", YES_NO, "Job offer in accounting near graduation"))

# F) Background controls
associations.append(assoc_ordinal(analysis_rows, "Q65", {str(i): i for i in range(15, 90)}, "Age"))
associations.append(assoc_nominal(analysis_rows, "Q17", "Undergraduate major"))
associations.append(assoc_nominal(analysis_rows, "Q60", "School state"))
associations.append(assoc_ordinal(analysis_rows, "Q16", WORKING_STATUS, "Full-time (vs part-time) student"))
associations.append(assoc_nominal(analysis_rows, "Q27", "Undergraduate vs graduate student status"))

# combined earnings variable for cleaner ranking
x, y = [], []
for r in analysis_rows:
    if r.get("Q55") in EARNINGS:
        x.append(EARNINGS[r["Q55"]])
        y.append(LIKERT_IMPACT[r["Q52"]])
    elif r.get("Q44") in EARNINGS:
        x.append(EARNINGS[r["Q44"]])
        y.append(LIKERT_IMPACT[r["Q52"]])
associations.append({
    "predictor": "Belief grad degree increases lifetime earnings (combined branches)",
    "type": "ordinal/binary",
    "n": len(x),
    "metric": abs(pearsonr(x, y)) if pearsonr(x, y) is not None else None,
    "signed": pearsonr(x, y),
})

ranked = [a for a in associations if a["metric"] is not None and a["n"] >= 20]
ranked.sort(key=lambda d: d["metric"], reverse=True)

# Grad-only version
grad_rows = [r for r in analysis_rows if r.get("Q27") == "Graduate"]
grad_associations = []
grad_associations.append(assoc_ordinal(grad_rows, "Q31", YES_NO, "Aware before beginning graduate program"))
grad_associations.append(assoc_ordinal(grad_rows, "Q30", INFLUENCE_150, "150-credit requirement influence on enrolling"))
grad_associations.append(assoc_ordinal(grad_rows, "Q37", SATISFACTION, "Satisfaction with pursuing graduate degree"))
grad_associations.append(assoc_ordinal(grad_rows, "Q57", PROGRAM_MODALITY, "Program modality (online vs in person)"))
grad_associations.append(assoc_ordinal(grad_rows, "Q58", PROGRAM_TYPE, "Program type (MAcc/MBA/Other)"))
grad_associations.append(assoc_ordinal(grad_rows, "Q49", YES_NO, "Employer requires/encourages graduate degree"))
grad_associations.append(assoc_ordinal(grad_rows, "Q48", YES_NO, "Job offer in accounting near graduation"))
grad_associations.append(assoc_ordinal(grad_rows, "Q51", LIKERT_IMPACT, "Perceived impact on desire to pursue CPA"))
grad_associations.append(assoc_ordinal(grad_rows, "Q33", AGREE, "Agree grad degree helps move up career ladder faster"))
grad_associations.append(assoc_ordinal(grad_rows, "Q34", AGREE, "Agree grad degree may delay advancement"))
grad_ranked = [a for a in grad_associations if a["metric"] is not None and a["n"] >= 8]
grad_ranked.sort(key=lambda d: d["metric"], reverse=True)

# Alternate grad-only analysis using grad-specific outcome Q35
all_valid_rows = [
    r for r in rows
    if r.get("ResponseId", "").startswith("R_")
    and r.get("Finished") == "True"
    and r.get("Q61") == "Yes"
    and r.get("Q28") != "Yes"
]
grad_q35_rows = [r for r in all_valid_rows if r.get("Q27") == "Graduate" and r.get("Q35") in LIKELY_GRAD_IF_KNEW]


def assoc_ordinal_custom_outcome(rows, outcome_col, outcome_map, predictor_col, predictor_map, label):
    x, y = [], []
    for r in rows:
        if r.get(outcome_col) in outcome_map and r.get(predictor_col) in predictor_map:
            y.append(outcome_map[r[outcome_col]])
            x.append(predictor_map[r[predictor_col]])
    r = pearsonr(x, y)
    return {
        "predictor": label,
        "n": len(x),
        "metric": abs(r) if r is not None else None,
        "signed": r,
    }


grad_q35_associations = [
    assoc_ordinal_custom_outcome(grad_q35_rows, "Q35", LIKELY_GRAD_IF_KNEW, "Q31", YES_NO, "Aware before beginning graduate program"),
    assoc_ordinal_custom_outcome(grad_q35_rows, "Q35", LIKELY_GRAD_IF_KNEW, "Q30", INFLUENCE_150, "150-credit requirement influence on enrolling"),
    assoc_ordinal_custom_outcome(grad_q35_rows, "Q35", LIKELY_GRAD_IF_KNEW, "Q37", SATISFACTION, "Satisfaction with pursuing graduate degree"),
    assoc_ordinal_custom_outcome(grad_q35_rows, "Q35", LIKELY_GRAD_IF_KNEW, "Q57", PROGRAM_MODALITY, "Program modality (online vs in person)"),
    assoc_ordinal_custom_outcome(grad_q35_rows, "Q35", LIKELY_GRAD_IF_KNEW, "Q58", PROGRAM_TYPE, "Program type (MAcc/MBA/Other)"),
    assoc_ordinal_custom_outcome(grad_q35_rows, "Q35", LIKELY_GRAD_IF_KNEW, "Q49", YES_NO, "Employer requires/encourages graduate degree"),
    assoc_ordinal_custom_outcome(grad_q35_rows, "Q35", LIKELY_GRAD_IF_KNEW, "Q48", YES_NO, "Job offer in accounting near graduation"),
    assoc_ordinal_custom_outcome(grad_q35_rows, "Q35", LIKELY_GRAD_IF_KNEW, "Q33", AGREE, "Agree grad degree helps move up career ladder faster"),
    assoc_ordinal_custom_outcome(grad_q35_rows, "Q35", LIKELY_GRAD_IF_KNEW, "Q34", AGREE, "Agree grad degree may delay advancement"),
]
grad_q35_ranked = [a for a in grad_q35_associations if a["metric"] is not None and a["n"] >= 8]
grad_q35_ranked.sort(key=lambda d: d["metric"], reverse=True)


def distribution_text(counter):
    order = [
        "Significantly decreased desire",
        "Decreased desire",
        "No change in desire",
        "Increased desire",
        "Significantly increased desire",
    ]
    total = sum(counter.values())
    parts = []
    for k in order:
        if counter.get(k, 0):
            parts.append(f"{k}: {counter[k]} ({counter[k]/total:.1%})")
    return "; ".join(parts)

with open(REPORT_FILE, "w", encoding="utf-8") as out:
    out.write("# RQ2 Cross-Sectional Analysis: Factors Associated with Self-Reported Impact on Desire to Pursue a Graduate Degree\n\n")
    out.write("## Scope and interpretation guardrails\n")
    out.write("- This is a **one-time cross-sectional survey**; results are described as factors **associated with / linked to / predictive of / correlated with** the outcome, not causal effects.\n")
    out.write("- The outcome uses respondents' wording of how the pathway **\"impacted\"** desire; this analysis treats that as **self-reported perceived impact**.\n")
    out.write(f"- Analysis sample: {len(analysis_rows)} completed, consented, non-duplicate responses with non-missing outcome.\n\n")

    out.write("## Outcome variable\n")
    out.write("Outcome question: *How has the availability of (or knowledge about) the alternative pathway to CPA licensure impacted your desire to pursue a graduate degree (MAcc or MBA)?*\n\n")
    out.write("Outcome coding (for association metrics only): significantly decreased = -2, decreased = -1, no change = 0, increased = +1, significantly increased = +2.\n\n")

    out.write("## Required group comparisons\n\n")
    out.write("### Awareness before survey (Q53)\n")
    for grp, stats in aware_stats.items():
        out.write(f"- **{grp}** (n={stats['n']}): mean perceived-impact score = {stats['mean']:.3f}. {distribution_text(stats['dist'])}.\n")
    if "Yes" in aware_stats and "No" in aware_stats:
        diff = aware_stats["Yes"]["mean"] - aware_stats["No"]["mean"]
        out.write(f"- Difference in means (Aware Yes - No): **{diff:.3f}**.\n")
    out.write("\n")

    out.write("### Undergraduate vs graduate status (Q27)\n")
    for grp, stats in student_stats.items():
        out.write(f"- **{grp}** (n={stats['n']}): mean perceived-impact score = {stats['mean']:.3f}. {distribution_text(stats['dist'])}.\n")
    if "Graduate" not in student_stats:
        out.write("- **Data limitation:** no graduate respondents had non-missing data on the main outcome (Q52), likely due survey skip logic. Direct undergrad-vs-grad comparison on the exact outcome is therefore not estimable.\n")
    out.write("\n")

    out.write("## Overall ranked associations with the outcome\n")
    out.write("Metric shown = absolute association strength (|r| for ordinal/binary predictors, eta for nominal predictors). Sign indicates direction only when ordinal/binary coding is available.\n\n")
    out.write("| Rank | Predictor | Type | n | Strength | Direction |\n")
    out.write("|---:|---|---|---:|---:|---|\n")
    for i, row in enumerate(ranked[:15], start=1):
        direction = "NA"
        if row["signed"] is not None:
            direction = "Positive" if row["signed"] > 0 else "Negative"
        out.write(f"| {i} | {row['predictor']} | {row['type']} | {row['n']} | {fmt(row['metric'])} | {direction} |\n")

    out.write("\n")
    out.write("### Key reading of strongest links\n")
    out.write("- Positive direction means higher predictor values align with reporting a higher (more increased) perceived impact on desire to pursue graduate school.\n")
    out.write("- Negative direction means higher predictor values align with reporting lower (more decreased) perceived impact.\n")
    out.write("- Direct item availability note: this dataset does not include a single explicit Likert item for \"graduate school is not worth the cost/time\" or a direct standalone item phrased as \"alternative pathway makes graduate school less necessary\"; nearest available indicators are ROI beliefs and the main outcome itself.\n\n")

    out.write("## Focus sections requested\n")

    out.write("### ROI belief items\n")
    for label in [
        "Belief grad degree increases lifetime earnings (combined branches)",
        "Agree grad degree helps move up career ladder faster",
        "Agree grad degree may delay advancement",
    ]:
        row = next((a for a in associations if a["predictor"] == label), None)
        if row and row["metric"] is not None:
            out.write(f"- {label}: strength={fmt(row['metric'])}, direction={'Positive' if (row['signed'] or 0)>0 else 'Negative'}, n={row['n']}.\n")
    out.write("\n")

    out.write("### Graduate program quality importance items\n")
    imp_rows = [a for a in associations if a["predictor"].startswith("Importance:") and a["metric"] is not None]
    imp_rows.sort(key=lambda d: d["metric"], reverse=True)
    for r in imp_rows:
        out.write(f"- {r['predictor']}: strength={fmt(r['metric'])}, direction={'Positive' if (r['signed'] or 0)>0 else 'Negative'}, n={r['n']}.\n")
    out.write("\n")

    out.write("## Graduate-student-only version (recommended)\n")
    out.write(f"Using the exact main outcome (Q52), graduate-only sample is n={len(grad_rows)}.\n\n")
    out.write("| Rank | Predictor | n | Strength | Direction |\n")
    out.write("|---:|---|---:|---:|---|\n")
    for i, row in enumerate(grad_ranked, start=1):
        out.write(f"| {i} | {row['predictor']} | {row['n']} | {fmt(row['metric'])} | {'Positive' if (row['signed'] or 0)>0 else 'Negative'} |\n")

    out.write("\n")
    out.write("### Graduate-only fallback outcome (Q35)\n")
    out.write("Because Q52 is missing for graduate respondents, this fallback uses graduate-only question Q35: *how likely they would have been to pursue a graduate degree if they had known about the alternative pathway before beginning*.\n")
    out.write(f"Grad fallback sample (Q35) n={len(grad_q35_rows)}.\n\n")
    out.write("| Rank | Predictor | n | Strength | Direction |\n")
    out.write("|---:|---|---:|---:|---|\n")
    for i, row in enumerate(grad_q35_ranked, start=1):
        out.write(f"| {i} | {row['predictor']} | {row['n']} | {fmt(row['metric'])} | {'Positive' if (row['signed'] or 0)>0 else 'Negative'} |\n")

    out.write("\n")
    out.write("### Graduate-only interpretation highlights\n")
    out.write("- Treat estimates as descriptive associations only due to cross-sectional design and small grad-only sample size.\n")
    out.write("- Program-type/modality results are exploratory because nearly all grad respondents are in MAcc and mostly/fully online formats.\n")

print(f"Wrote {REPORT_FILE} with {len(analysis_rows)} analysis rows.")
