# LangGraph Travel Agent 🌍✈️

An intelligent travel planning agent built with LangGraph that creates personalized travel itineraries based on your preferences, hobbies, and travel details.

## Features

- **Personalized Planning**: Tailored recommendations based on your interests and hobbies
- **Comprehensive Research**: Automated destination research using web search
- **Day-by-Day Itinerary**: Detailed daily schedules with timing and activities
- **Accommodation Suggestions**: Hotel and lodging recommendations matching your preferences
- **Activity Recommendations**: Curated activities aligned with your interests
- **Complete Travel Guide**: All-in-one document with everything you need for your trip

## Architecture

The travel agent uses a LangGraph workflow with the following nodes:

1. **Validate Input** - Confirms travel details
2. **Research Destination** - Gathers information about the destination
3. **Plan Itinerary** - Creates day-by-day schedule
4. **Suggest Accommodations** - Recommends places to stay
5. **Recommend Activities** - Suggests activities based on hobbies
6. **Compile Final Plan** - Combines everything into a comprehensive guide

## Installation

1. **Clone the repository**:
```bash
cd langgraph-my-travelagent
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -e .
```

4. **Set up environment variables**:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude
- `TAVILY_API_KEY`: Your Tavily API key for web search

## Usage

Run the travel agent:

```bash
python main.py
```

You'll be prompted to enter:
- **Starting location**: Where you're traveling from
- **Destination**: Where you want to go
- **Start date**: Trip start date (YYYY-MM-DD)
- **End date**: Trip end date (YYYY-MM-DD)
- **Travel preferences**: Budget level, travel style, etc.
- **Hobbies and interests**: What you enjoy doing

The agent will then:
1. Validate your inputs
2. Research the destination
3. Create a personalized itinerary
4. Suggest accommodations
5. Recommend activities
6. Compile everything into a complete travel plan

The final plan will be displayed in the terminal and saved to a text file.

## Example

```
Starting location: San Francisco, USA
Destination: Tokyo, Japan
Trip start date: 2024-06-15
Trip end date: 2024-06-22
Travel preferences: Mid-range budget, interested in local culture
Hobbies and interests: Photography, anime, food, temples
```

The agent will create a comprehensive 7-day Tokyo itinerary with photography spots, anime locations, food recommendations, temple visits, and more!

## Project Structure

```
langgraph-my-travelagent/
├── src/
│   └── travel_agent/
│       ├── __init__.py
│       ├── state.py          # State schema definition
│       ├── tools.py          # Travel research tools
│       ├── nodes.py          # Workflow node functions
│       ├── graph.py          # LangGraph workflow
│       └── config.py         # Configuration management
├── main.py                   # CLI entry point
├── pyproject.toml           # Project dependencies
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Requirements

- Python 3.10+
- Anthropic API key (for Claude LLM)
- Tavily API key (for web search)

## API Keys

### Anthropic API Key
Sign up at [console.anthropic.com](https://console.anthropic.com/) to get your API key.

### Tavily API Key
Sign up at [tavily.com](https://tavily.com/) to get your search API key.

## Customization

You can customize the travel agent by:

1. **Adding new tools** in `src/travel_agent/tools.py`
2. **Modifying nodes** in `src/travel_agent/nodes.py`
3. **Adjusting the workflow** in `src/travel_agent/graph.py`
4. **Changing LLM settings** in `src/travel_agent/config.py`

## License

MIT License

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
