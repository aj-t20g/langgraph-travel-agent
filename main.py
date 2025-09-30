#!/usr/bin/env python3
"""Main entry point for the Travel Agent CLI."""

import sys
from datetime import datetime

from src.travel_agent.config import Config
from src.travel_agent.graph import travel_agent_graph
from src.travel_agent.state import TravelAgentState


def get_user_input(prompt: str, required: bool = True) -> str:
    """Get input from the user.

    Args:
        prompt: The prompt to display
        required: Whether the input is required

    Returns:
        User input string
    """
    while True:
        value = input(f"{prompt}: ").strip()
        if value or not required:
            return value
        print("This field is required. Please provide a value.")


def validate_date(date_str: str) -> bool:
    """Validate date format.

    Args:
        date_str: Date string to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_date_input(prompt: str) -> str:
    """Get a date input from the user.

    Args:
        prompt: The prompt to display

    Returns:
        Date string in YYYY-MM-DD format
    """
    while True:
        date_str = get_user_input(f"{prompt} (YYYY-MM-DD)")
        if validate_date(date_str):
            return date_str
        print("Invalid date format. Please use YYYY-MM-DD (e.g., 2024-12-25)")


def collect_travel_details() -> dict:
    """Collect travel details from the user via CLI.

    Returns:
        Dictionary with travel details
    """
    print("\n" + "=" * 60)
    print("Welcome to the AI Travel Agent!")
    print("=" * 60 + "\n")

    print("Let's plan your perfect trip! Please provide the following details:\n")

    # Collect all required information
    source = get_user_input("Starting location (city, country)")
    destination = get_user_input("Destination (city, country)")
    start_date = get_date_input("Trip start date")
    end_date = get_date_input("Trip end date")

    print("\nGreat! Now let's personalize your trip:\n")

    preferences = get_user_input(
        "Travel preferences (e.g., budget-friendly, luxury, family-friendly, solo travel)"
    )
    hobbies = get_user_input(
        "Your hobbies and interests (e.g., photography, hiking, food, history, art)"
    )

    print("\n" + "=" * 60)
    print("Perfect! I'm now creating your personalized travel plan...")
    print("This may take a few minutes as I research and plan your trip.")
    print("=" * 60 + "\n")

    return {
        "source": source,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "preferences": preferences,
        "hobbies": hobbies,
        "messages": [],
        "destination_info": "",
        "itinerary": "",
        "accommodations": "",
        "activities": "",
        "final_plan": "",
    }


def save_plan_to_file(plan: str, destination: str) -> str:
    """Save the travel plan to a file.

    Args:
        plan: The travel plan content
        destination: The destination name

    Returns:
        The filename where the plan was saved
    """
    # Create a safe filename
    safe_destination = "".join(c for c in destination if c.isalnum() or c in (" ", "-", "_")).strip()
    safe_destination = safe_destination.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"travel_plan_{safe_destination}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(plan)

    return filename


def main():
    """Main function to run the travel agent."""
    # Check configuration
    if not Config.is_valid():
        missing = Config.validate()
        print("Error: Missing required environment variables:")
        for key in missing:
            print(f"  - {key}")
        print("\nPlease create a .env file with the required API keys.")
        print("See .env.example for reference.")
        sys.exit(1)

    try:
        # Collect travel details
        travel_details = collect_travel_details()

        # Create initial state
        initial_state: TravelAgentState = travel_details

        # Run the graph
        result = travel_agent_graph.invoke(initial_state)

        # Display the final plan
        print("\n" + "=" * 60)
        print("YOUR PERSONALIZED TRAVEL PLAN")
        print("=" * 60 + "\n")
        print(result["final_plan"])
        print("\n" + "=" * 60 + "\n")

        # Save to file
        filename = save_plan_to_file(result["final_plan"], travel_details["destination"])
        print(f"Your travel plan has been saved to: {filename}")
        print("\nHave a wonderful trip! 🌍✈️")

    except KeyboardInterrupt:
        print("\n\nTravel planning cancelled. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nAn error occurred: {str(e)}")
        print("Please try again or check your configuration.")
        sys.exit(1)


if __name__ == "__main__":
    main()
