# LangGraph Travel Agent 🌍✈️

An intelligent travel planning agent built with LangGraph that creates personalized travel itineraries based on your preferences, hobbies, and travel details.

## Features

- **Multi-User Support**: Each user identified by user_id with persistent preferences
- **Memory Across Sessions**: Automatically saves and loads user preferences
- **Personalized Planning**: Tailored recommendations based on your interests and hobbies
- **Comprehensive Research**: Automated destination research using web search
- **Day-by-Day Itinerary**: Detailed daily schedules with timing and activities
- **Accommodation Suggestions**: Hotel and lodging recommendations matching your preferences
- **Activity Recommendations**: Curated activities aligned with your interests
- **Complete Travel Guide**: All-in-one document with everything you need for your trip

## Architecture

The travel agent uses a LangGraph workflow with the following nodes:

1. **Load User Preferences** - Retrieves saved preferences for returning users
2. **Validate Input** - Confirms travel details
3. **Research Destination** - Gathers information about the destination
4. **Plan Itinerary** - Creates day-by-day schedule
5. **Suggest Accommodations** - Recommends places to stay
6. **Recommend Activities** - Suggests activities based on hobbies
7. **Compile Final Plan** - Combines everything into a comprehensive guide
8. **Save User Preferences** - Stores preferences for future trips

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

### Local Testing

Test the graph locally with LangGraph dev server:

```bash
langgraph dev
```

This starts a local server at http://127.0.0.1:2024 with LangGraph Studio UI.

### Deploy to LangGraph Cloud

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions:

```bash
langgraph login
langgraph deploy
```

### API Usage

The agent accepts the following inputs:
- **user_id**: Unique identifier (email/username) for saving preferences
- **source**: Starting location
- **destination**: Where you want to go
- **start_date**: Trip start date (YYYY-MM-DD)
- **end_date**: Trip end date (YYYY-MM-DD)
- **preferences**: Budget level, travel style, etc.
- **hobbies**: What you enjoy doing

The agent returns:
- **final_plan**: Complete travel guide (3000-5000 words) ← **Use this!**
- **saved_preferences**: Previous preferences for returning users
- Plus: destination_info, itinerary, accommodations, activities

See [API_RESPONSE_GUIDE.md](API_RESPONSE_GUIDE.md) for detailed response documentation.

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
langgraph-t20g-travelagent/
├── src/
│   └── travel_agent/
│       ├── __init__.py
│       ├── state.py          # State schema (includes user_id)
│       ├── tools.py          # Travel research tools (Tavily)
│       ├── nodes.py          # Memory-enabled workflow nodes
│       ├── graph.py          # LangGraph workflow (exports travel_agent_graph)
│       └── config.py         # Configuration management
├── langgraph.json           # LangGraph Cloud configuration
├── pyproject.toml           # Project dependencies
├── .env                     # Environment variables (gitignored)
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── DEPLOYMENT.md           # Deployment guide
└── API_RESPONSE_GUIDE.md   # API response documentation
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
