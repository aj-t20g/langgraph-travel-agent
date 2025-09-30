"""Node functions for the travel agent workflow."""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from .state import TravelAgentState
from .tools import TRAVEL_TOOLS


def create_llm(use_tools: bool = False):
    """Create an LLM instance.

    Args:
        use_tools: Whether to bind tools to the LLM

    Returns:
        Configured LLM instance
    """
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)
    if use_tools:
        llm = llm.bind_tools(TRAVEL_TOOLS)
    return llm


def validate_input_node(state: TravelAgentState) -> TravelAgentState:
    """Validate and confirm the travel details with the user.

    Args:
        state: Current state

    Returns:
        Updated state with validation message
    """
    validation_message = f"""
Travel Details Received:
- Source: {state.get('source', 'Not provided')}
- Destination: {state.get('destination', 'Not provided')}
- Dates: {state.get('start_date', 'Not provided')} to {state.get('end_date', 'Not provided')}
- Preferences: {state.get('preferences', 'Not provided')}
- Hobbies/Interests: {state.get('hobbies', 'Not provided')}

I'll now create a personalized travel plan for you!
"""
    return {
        **state,
        "messages": state.get("messages", []) + [HumanMessage(content=validation_message)],
    }


def research_destination_node(state: TravelAgentState) -> TravelAgentState:
    """Research the destination and gather relevant information.

    Args:
        state: Current state

    Returns:
        Updated state with destination research
    """
    llm = create_llm(use_tools=True)

    system_prompt = """You are a travel research specialist. Research the destination thoroughly and provide:
1. Overview of the destination
2. Best attractions and landmarks
3. Local culture and customs
4. Transportation options
5. Weather and best time to visit
6. Safety considerations

Use the search tool to find current and accurate information."""

    user_prompt = f"""Research {state['destination']} for a trip from {state['start_date']} to {state['end_date']}.
The traveler is coming from {state['source']}.
Their interests include: {state['hobbies']}
Their preferences: {state['preferences']}

Provide comprehensive destination information."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)

    # Handle tool calls if any
    while response.tool_calls:
        tool_messages = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Find and execute the tool
            tool = next((t for t in TRAVEL_TOOLS if t.name == tool_name), None)
            if tool:
                tool_result = tool.invoke(tool_args)
                tool_messages.append({
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": tool_call["id"],
                })

        messages.append(response)
        messages.extend(tool_messages)
        response = llm.invoke(messages)

    return {
        **state,
        "destination_info": response.content,
    }


def plan_itinerary_node(state: TravelAgentState) -> TravelAgentState:
    """Create a day-by-day itinerary.

    Args:
        state: Current state

    Returns:
        Updated state with itinerary
    """
    llm = create_llm(use_tools=False)

    system_prompt = """You are an expert travel itinerary planner. Create a detailed day-by-day itinerary that:
1. Balances activities with rest time
2. Groups nearby attractions logically
3. Considers travel time between locations
4. Matches the traveler's interests and preferences
5. Includes specific timing suggestions
6. Accounts for meal times and local dining options"""

    user_prompt = f"""Create a day-by-day itinerary for:
- Destination: {state['destination']}
- Dates: {state['start_date']} to {state['end_date']}
- Traveler interests: {state['hobbies']}
- Preferences: {state['preferences']}

Destination information:
{state['destination_info']}

Provide a detailed daily schedule."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)

    return {
        **state,
        "itinerary": response.content,
    }


def suggest_accommodations_node(state: TravelAgentState) -> TravelAgentState:
    """Suggest accommodations based on preferences.

    Args:
        state: Current state

    Returns:
        Updated state with accommodation suggestions
    """
    llm = create_llm(use_tools=True)

    system_prompt = """You are a hotel and accommodation specialist. Suggest accommodations that:
1. Match the traveler's budget and preferences
2. Are well-located for the planned itinerary
3. Have good reviews and ratings
4. Offer relevant amenities
5. Consider different accommodation types (hotels, hostels, vacation rentals, etc.)

Use the search tool to find current options and prices."""

    user_prompt = f"""Suggest accommodations in {state['destination']} for:
- Dates: {state['start_date']} to {state['end_date']}
- Preferences: {state['preferences']}
- Itinerary focus areas: See the itinerary below

Itinerary:
{state['itinerary']}

Provide 3-5 accommodation recommendations with pros and cons."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)

    # Handle tool calls if any
    while response.tool_calls:
        tool_messages = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool = next((t for t in TRAVEL_TOOLS if t.name == tool_name), None)
            if tool:
                tool_result = tool.invoke(tool_args)
                tool_messages.append({
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": tool_call["id"],
                })

        messages.append(response)
        messages.extend(tool_messages)
        response = llm.invoke(messages)

    return {
        **state,
        "accommodations": response.content,
    }


def recommend_activities_node(state: TravelAgentState) -> TravelAgentState:
    """Recommend activities based on hobbies and interests.

    Args:
        state: Current state

    Returns:
        Updated state with activity recommendations
    """
    llm = create_llm(use_tools=True)

    system_prompt = """You are an activity and experience curator. Recommend activities that:
1. Align with the traveler's hobbies and interests
2. Are unique to the destination
3. Fit within the itinerary timeframe
4. Offer a mix of popular and off-beaten-path experiences
5. Include booking information and tips

Use the search tool to find current activities, tours, and experiences."""

    user_prompt = f"""Recommend activities in {state['destination']} for someone interested in: {state['hobbies']}
- Travel dates: {state['start_date']} to {state['end_date']}
- Preferences: {state['preferences']}

Existing itinerary:
{state['itinerary']}

Suggest specific activities, tours, or experiences they shouldn't miss."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)

    # Handle tool calls if any
    while response.tool_calls:
        tool_messages = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool = next((t for t in TRAVEL_TOOLS if t.name == tool_name), None)
            if tool:
                tool_result = tool.invoke(tool_args)
                tool_messages.append({
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": tool_call["id"],
                })

        messages.append(response)
        messages.extend(tool_messages)
        response = llm.invoke(messages)

    return {
        **state,
        "activities": response.content,
    }


def compile_final_plan_node(state: TravelAgentState) -> TravelAgentState:
    """Compile all information into a comprehensive travel plan.

    Args:
        state: Current state

    Returns:
        Updated state with final compiled plan
    """
    llm = create_llm(use_tools=False)

    system_prompt = """You are a travel plan compiler. Create a comprehensive, well-organized travel plan that:
1. Combines all research, itinerary, accommodations, and activities
2. Presents information in a clear, easy-to-follow format
3. Includes practical tips and reminders
4. Adds any final recommendations
5. Formats the plan beautifully with sections and subsections"""

    user_prompt = f"""Compile a final comprehensive travel plan using all the information below:

DESTINATION RESEARCH:
{state['destination_info']}

DAILY ITINERARY:
{state['itinerary']}

ACCOMMODATIONS:
{state['accommodations']}

RECOMMENDED ACTIVITIES:
{state['activities']}

Create a polished, complete travel guide for a trip from {state['source']} to {state['destination']}
from {state['start_date']} to {state['end_date']}."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)

    return {
        **state,
        "final_plan": response.content,
        "messages": state.get("messages", []) + [HumanMessage(content=response.content)],
    }
