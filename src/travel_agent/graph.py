"""LangGraph workflow for the travel agent."""

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.store.base import BaseStore

from .state import TravelAgentState
from .nodes import (
    load_user_preferences_node,
    save_user_preferences_node,
    validate_input_node,
    research_destination_node,
    plan_itinerary_node,
    suggest_accommodations_node,
    recommend_activities_node,
    compile_final_plan_node,
)


def create_travel_agent_graph(
    checkpointer: BaseCheckpointSaver = None,
    store: BaseStore = None,
):
    """Create the travel agent workflow graph.

    Args:
        checkpointer: Optional checkpointer for persistence
        store: Optional memory store for user preferences

    Returns:
        Compiled LangGraph workflow
    """
    # Initialize the graph with our state
    workflow = StateGraph(TravelAgentState)

    # Add nodes to the graph
    workflow.add_node("load_user_preferences", load_user_preferences_node)
    workflow.add_node("validate_input", validate_input_node)
    workflow.add_node("research_destination", research_destination_node)
    workflow.add_node("plan_itinerary", plan_itinerary_node)
    workflow.add_node("suggest_accommodations", suggest_accommodations_node)
    workflow.add_node("recommend_activities", recommend_activities_node)
    workflow.add_node("compile_final_plan", compile_final_plan_node)
    workflow.add_node("save_user_preferences", save_user_preferences_node)

    # Define the workflow edges (sequential flow)
    workflow.set_entry_point("load_user_preferences")
    workflow.add_edge("load_user_preferences", "validate_input")
    workflow.add_edge("validate_input", "research_destination")
    workflow.add_edge("research_destination", "plan_itinerary")
    workflow.add_edge("plan_itinerary", "suggest_accommodations")
    workflow.add_edge("suggest_accommodations", "recommend_activities")
    workflow.add_edge("recommend_activities", "compile_final_plan")
    workflow.add_edge("compile_final_plan", "save_user_preferences")
    workflow.add_edge("save_user_preferences", END)

    # Compile the graph with checkpointer and store
    return workflow.compile(checkpointer=checkpointer, store=store)


# Create a singleton instance for LangGraph deployment
# LangGraph Cloud/Platform automatically provides checkpointer and store
# so we compile without custom persistence - it will be injected by the platform
travel_agent_graph = create_travel_agent_graph()
