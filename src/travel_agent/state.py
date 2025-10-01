"""State schema for the travel agent."""

from typing import Annotated, TypedDict
from langgraph.graph import add_messages


class TravelAgentState(TypedDict):
    """State for the travel agent workflow.

    Attributes:
        messages: Conversation history with the user
        user_id: Unique identifier for the user
        source: Starting location for the trip
        destination: Destination location
        start_date: Trip start date (YYYY-MM-DD format)
        end_date: Trip end date (YYYY-MM-DD format)
        preferences: User preferences (e.g., budget level, travel style)
        hobbies: User hobbies and interests
        saved_preferences: Previously saved user preferences loaded from memory
        destination_info: Research about the destination
        itinerary: Suggested daily itinerary
        accommodations: Accommodation recommendations
        activities: Activity recommendations based on hobbies
        final_plan: Complete travel plan
    """

    messages: Annotated[list, add_messages]
    user_id: str
    source: str
    destination: str
    start_date: str
    end_date: str
    preferences: str
    hobbies: str
    saved_preferences: str
    destination_info: str
    itinerary: str
    accommodations: str
    activities: str
    final_plan: str
