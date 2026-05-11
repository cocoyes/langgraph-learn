from llm.deepseek_client import DeepSeekClient
from nodes.prompts import PLAN_SYSTEM_PROMPT
from state import GraphState


def build_plan_node(client: DeepSeekClient):
    def plan_node(state: GraphState) -> GraphState:
        user_prompt = (
            "请围绕该需求生成 LangGraph 方案。\n"
            f"需求：{state['user_query']}\n"
            f"意图：{state['intent']}"
        )
        plan = client.invoke(system_prompt=PLAN_SYSTEM_PROMPT, user_prompt=user_prompt)
        return {"plan": plan}

    return plan_node
