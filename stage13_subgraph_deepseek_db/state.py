from typing import TypedDict


class GraphState(TypedDict):
    user_query: str
    intent: str
    route: str
    plan: str
    research_notes: str
    draft_answer: str
    final_answer: str
    quality_score: int
    quality_decision: str
    rewrite_round: int
    max_rewrite_rounds: int
    persisted_id: int
