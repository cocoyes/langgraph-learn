from db.repository import LearningRunRepository
from nodes.helpers import RECENT_LIMIT
from state import GraphState


def build_persist_node(repository: LearningRunRepository):
    def persist_node(state: GraphState) -> GraphState:
        run_id = repository.save_run(
            user_query=state["user_query"],
            intent=state["intent"],
            plan=state["plan"],
            final_answer=state["final_answer"],
            quality_score=state["quality_score"],
        )
        normalized_id = run_id if run_id is not None else 0
        return {"persisted_id": normalized_id}

    return persist_node


def build_recent_runs_node(repository: LearningRunRepository):
    def recent_runs_node(_: GraphState) -> GraphState:
        recent_runs = repository.list_recent(limit=RECENT_LIMIT)
        lines = [f"最近 {len(recent_runs)} 条记录："]
        for item in recent_runs:
            lines.append(
                f"- #{item['id']} | intent={item['intent']} | score={item['quality_score']} | {item['created_at']}"
            )
        text = "\n".join(lines) if lines else "最近 0 条记录。"
        return {"research_notes": text}

    return recent_runs_node
