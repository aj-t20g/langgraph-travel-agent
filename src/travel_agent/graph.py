"""LangGraph workflow for the travel agent."""

from langgraph.graph import StateGraph, END

from .state import TravelAgentState
from .nodes import (
    validate_input_node,
    research_destination_node,
    plan_itinerary_node,
    suggest_accommodations_node,
    recommend_activities_node,
    compile_final_plan_node,
)


def create_travel_agent_graph():
    """Create the travel agent workflow graph.

    Returns:
        Compiled LangGraph workflow
    """
    # Initialize the graph with our state
    workflow = StateGraph(TravelAgentState)

    # Add nodes to the graph
    workflow.add_node("validate_input", validate_input_node)
    workflow.add_node("research_destination", research_destination_node)
    workflow.add_node("plan_itinerary", plan_itinerary_node)
    workflow.add_node("suggest_accommodations", suggest_accommodations_node)
    workflow.add_node("recommend_activities", recommend_activities_node)
    workflow.add_node("compile_final_plan", compile_final_plan_node)

    # Define the workflow edges (sequential flow)
    workflow.set_entry_point("validate_input")
    workflow.add_edge("validate_input", "research_destination")
    workflow.add_edge("research_destination", "plan_itinerary")
    workflow.add_edge("plan_itinerary", "suggest_accommodations")
    workflow.add_edge("suggest_accommodations", "recommend_activities")
    workflow.add_edge("recommend_activities", "compile_final_plan")
    workflow.add_edge("compile_final_plan", END)

    # Compile the graph
    return workflow.compile()


# Create a singleton instance
travel_agent_graph = create_travel_agent_graph()
