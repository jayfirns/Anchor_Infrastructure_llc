"""Scoring engine for the discovery questionnaire.

Takes survey answers and a scoring rubric, produces:
- recommended_tier (Anchor Seed / Anchor Node / Anchor Hybrid / Anchor Enterprise)
- dimension scores (complexity, security, availability, budget, maturity)
- reasoning text explaining the recommendation
- client_segment (Regulated Firm / Technical Founder / Privacy-Conscious Org)
"""


def score_survey(answers: dict, rubric: dict) -> dict:
    """Score survey answers against the rubric.

    Args:
        answers: Dict of question_id -> selected answer value.
        rubric: Scoring rubric loaded from data/scoring.json.

    Returns:
        Dict with recommended_tier, dimensions, total_score,
        client_segment, and reasoning.
    """
    dimensions = {}
    dimension_defs = rubric.get("dimensions", {})

    for dim_name, dim_config in dimension_defs.items():
        dim_score = 0
        for question_id, answer_scores in dim_config.get("questions", {}).items():
            answer = answers.get(question_id)
            if answer is not None and str(answer) in answer_scores:
                dim_score += answer_scores[str(answer)]
        dimensions[dim_name] = dim_score

    total = sum(dimensions.values())

    # Determine tier from thresholds
    tier_thresholds = rubric.get("tier_thresholds", {})
    recommended_tier = "Anchor Node"
    for tier_name, threshold in sorted(
        tier_thresholds.items(), key=lambda x: x[1], reverse=True
    ):
        if total >= threshold:
            recommended_tier = tier_name
            break

    # Determine client segment from highest-scoring segment dimension
    segment_map = rubric.get("segment_mapping", {})
    client_segment = _determine_segment(answers, segment_map)

    # Build reasoning
    reasoning = _build_reasoning(dimensions, recommended_tier, client_segment, rubric)

    return {
        "recommended_tier": recommended_tier,
        "dimensions": dimensions,
        "total_score": total,
        "client_segment": client_segment,
        "reasoning": reasoning,
    }


def _determine_segment(answers: dict, segment_map: dict) -> str:
    """Match answers to the best-fit client segment."""
    if not segment_map:
        return "General"

    segment_scores = {}
    for segment, indicators in segment_map.items():
        score = 0
        for question_id, matching_answers in indicators.items():
            answer = answers.get(question_id)
            if str(answer) in [str(a) for a in matching_answers]:
                score += 1
        segment_scores[segment] = score

    if not segment_scores or max(segment_scores.values()) == 0:
        return "General"

    return max(segment_scores, key=segment_scores.get)


def _build_reasoning(
    dimensions: dict, tier: str, segment: str, rubric: dict
) -> str:
    """Generate human-readable reasoning for the recommendation."""
    reasoning_templates = rubric.get("reasoning_templates", {})

    lines = [f"Based on your responses, we recommend **{tier}**."]
    lines.append("")

    # Dimension-specific reasoning
    for dim, score in dimensions.items():
        dim_config = rubric.get("dimensions", {}).get(dim, {})
        thresholds = dim_config.get("reasoning_thresholds", {})
        for level in ["high", "medium", "low"]:
            level_config = thresholds.get(level, {})
            if "min" in level_config and score >= level_config["min"]:
                lines.append(f"- **{dim.replace('_', ' ').title()}:** {level_config.get('text', '')}")
                break

    lines.append("")

    # Segment-specific note
    segment_note = reasoning_templates.get(segment, "")
    if segment_note:
        lines.append(segment_note)

    return "\n".join(lines)
