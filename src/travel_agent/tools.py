"""Tools for the travel agent to gather information."""

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool


def get_search_tool() -> TavilySearchResults:
    """Get the Tavily search tool for travel information.

    Returns:
        TavilySearchResults tool configured for travel queries
    """
    return TavilySearchResults(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
    )


@tool
def calculate_trip_duration(start_date: str, end_date: str) -> str:
    """Calculate the duration of a trip in days.

    Args:
        start_date: Trip start date in YYYY-MM-DD format
        end_date: Trip end date in YYYY-MM-DD format

    Returns:
        Number of days for the trip
    """
    from datetime import datetime

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        duration = (end - start).days + 1  # Include both start and end day
        return f"{duration} days"
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."


@tool
def get_season_info(destination: str, month: str) -> str:
    """Get general season information for a destination.

    Args:
        destination: The destination location
        month: Month name or number

    Returns:
        Basic season information
    """
    # Simple mapping - in production, this would use actual weather APIs
    northern_hemisphere_seasons = {
        "12": "Winter", "1": "Winter", "2": "Winter",
        "3": "Spring", "4": "Spring", "5": "Spring",
        "6": "Summer", "7": "Summer", "8": "Summer",
        "9": "Fall", "10": "Fall", "11": "Fall",
    }

    month_names = {
        "january": "1", "february": "2", "march": "3", "april": "4",
        "may": "5", "june": "6", "july": "7", "august": "8",
        "september": "9", "october": "10", "november": "11", "december": "12",
    }

    month_num = month_names.get(month.lower(), month)
    season = northern_hemisphere_seasons.get(month_num, "Unknown")

    return f"In {destination}, the season in month {month} is typically {season}. Consider checking current weather forecasts for accurate information."


# List of all tools available to the agent
TRAVEL_TOOLS = [
    get_search_tool(),
    calculate_trip_duration,
    get_season_info,
]
