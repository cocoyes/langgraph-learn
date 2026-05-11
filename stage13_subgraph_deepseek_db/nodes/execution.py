from llm.deepseek_client import DeepSeekClient
from nodes.prompts import RESEARCH_SYSTEM_PROMPT, WRITER_SYSTEM_PROMPT
from state import GraphState


def build_research_node(client: DeepSeekClient):
    def research_node(state: GraphState) -> GraphState:
        user_prompt = (
            "你需要为这个方案补充调研要点。\n"
            f"用户需求：{state['user_query']}\n"
            f"当前计划：{state['plan']}"
        )
        research_notes = client.invoke(system_prompt=RESEARCH_SYSTEM_PROMPT, user_prompt=user_prompt)
        return {"research_notes": research_notes}

    return research_node


def build_writer_with_research_node(client: DeepSeekClient):
    def writer_with_research_node(state: GraphState) -> GraphState:
        user_prompt = (
            "请结合计划和调研输出最终答案，要求贴近生产实践。\n"
            f"用户需求：{state['user_query']}\n"
            f"计划：{state['plan']}\n"
            f"调研：{state['research_notes']}"
        )
        draft_answer = client.invoke(system_prompt=WRITER_SYSTEM_PROMPT, user_prompt=user_prompt)
        return {"draft_answer": draft_answer}

    return writer_with_research_node


def build_writer_direct_node(client: DeepSeekClient):
    def writer_direct_node(state: GraphState) -> GraphState:
        user_prompt = (
            "请直接输出最终答案，要求可执行、可验证。\n"
            f"用户需求：{state['user_query']}\n"
            f"计划：{state['plan']}"
        )
        draft_answer = client.invoke(system_prompt=WRITER_SYSTEM_PROMPT, user_prompt=user_prompt)
        return {"draft_answer": draft_answer}

    return writer_direct_node
