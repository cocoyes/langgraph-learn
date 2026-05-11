import re

from enums import IntentType, QualityDecision, RouteType


QUALITY_THRESHOLD = 75
RECENT_LIMIT = 5


def normalize_intent(raw_text: str) -> str:
    lower_text = raw_text.lower()
    for item in IntentType:
        if item.value in lower_text:
            return item.value
    return IntentType.LEARNING.value


def decide_route(intent: str, user_query: str) -> str:
    long_query_min_len = 20
    if intent == IntentType.ANALYSIS.value or len(user_query.strip()) >= long_query_min_len:
        return RouteType.RESEARCH_AND_WRITE.value
    return RouteType.DIRECT_WRITE.value


def extract_quality_score(review_text: str) -> int:
    matched = re.search(r"(?<![0-9-])([0-9]{1,3})(?![0-9]|\\s*-\\s*[0-9])", review_text)
    if not matched:
        return 60
    score = int(matched.group(1))
    if score < 0:
        return 0
    if score > 100:
        return 100
    return score


def quality_to_decision(score: int, rewrite_round: int, max_rewrite_rounds: int) -> str:
    if score >= QUALITY_THRESHOLD:
        return QualityDecision.PASS.value
    if rewrite_round >= max_rewrite_rounds:
        return QualityDecision.PASS.value
    return QualityDecision.REWRITE.value
