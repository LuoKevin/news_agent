from typing import TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.workflow.nodes.handlers import HandlerResult, handle_general_query, handle_news_request, handle_unknown
from src.workflow.nodes.intent import Intent, IntentResult, classify_intent


class GraphState(TypedDict, total=False):
    message: str
    intent: IntentResult
    response: HandlerResult


def _classify_node(state: GraphState) -> GraphState:
    return {"intent": classify_intent(state["message"])}


def _route(state: GraphState) -> str:
    intent = state["intent"].intent
    if intent == Intent.NEWS_REQUEST:
        return "news"
    if intent == Intent.GENERAL_QUERY:
        return "general"
    return "unknown"


def build_graph() -> CompiledStateGraph:
    g = StateGraph(GraphState)
    g.add_node("classify", _classify_node)
    g.add_node("news", lambda state: {"response": handle_news_request(state["intent"])})
    g.add_node("general", lambda state: {"response": handle_general_query(state["intent"])})
    g.add_node("unknown", lambda state: {"response": handle_unknown(state["intent"])})

    g.set_entry_point("classify")
    g.add_conditional_edges("classify", _route, {"news": "news", "general": "general", "unknown": "unknown"})
    for node in ["news", "general", "unknown"]:
        g.add_edge(node, END)

    return g.compile()


def run_graph(graph: CompiledStateGraph, message: str) -> HandlerResult:
    state = {"message": message}
    final = graph.invoke(state)
    return final["response"]
