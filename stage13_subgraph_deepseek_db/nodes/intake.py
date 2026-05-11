from llm.deepseek_client import DeepSeekClient
from nodes.helpers import decide_route, normalize_intent
from nodes.prompts import INTENT_SYSTEM_PROMPT
from state import GraphState


def build_intake_node(client: DeepSeekClient):
    def intake_node(state: GraphState) -> GraphState:
        user_query = state["user_query"].strip()
        intent_raw = client.invoke(
            system_prompt=INTENT_SYSTEM_PROMPT,
            user_prompt="用户问题：" + user_query,
        )
        intent = normalize_intent(intent_raw)
        route = decide_route(intent=intent, user_query=user_query)
        return {"intent": intent, "route": route}

    return intake_node
