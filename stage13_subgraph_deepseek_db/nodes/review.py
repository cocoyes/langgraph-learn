from llm.deepseek_client import DeepSeekClient
from nodes.helpers import extract_quality_score, quality_to_decision
from nodes.prompts import REVIEW_SYSTEM_PROMPT
from state import GraphState


def build_review_node(client: DeepSeekClient):
    def review_node(state: GraphState) -> GraphState:
        review_text = client.invoke(
            system_prompt=REVIEW_SYSTEM_PROMPT,
            user_prompt="请评审以下草稿：\n" + state["draft_answer"],
        )
        quality_score = extract_quality_score(review_text=review_text)
        decision = quality_to_decision(
            score=quality_score,
            rewrite_round=state["rewrite_round"],
            max_rewrite_rounds=state["max_rewrite_rounds"],
        )
        return {"quality_score": quality_score, "quality_decision": decision}

    return review_node


def rewrite_round_node(state: GraphState) -> GraphState:
    return {"rewrite_round": state["rewrite_round"] + 1}


def finalize_node(state: GraphState) -> GraphState:
    return {"final_answer": state["draft_answer"]}
