# Deploying to LangGraph Cloud

This guide walks you through deploying your travel agent to LangGraph Cloud.

## Prerequisites

1. **LangGraph Cloud Account**: Sign up at [langchain-ai.github.io/langgraph/cloud/](https://langchain-ai.github.io/langgraph/cloud/)
2. **LangGraph CLI**: Install the CLI tool
   ```bash
   pip install langgraph-cli
   ```

## Project Structure for Deployment

The project is already configured for LangGraph Cloud with:

- `langgraph.json` - Configuration file specifying the graph location
- `requirements.txt` - Python dependencies
- `src/travel_agent/graph.py` - Exports `travel_agent_graph`

## Step 1: Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit - Travel Agent"
```

## Step 2: Set Up Environment Variables

Your API keys need to be configured in LangGraph Cloud:

- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `TAVILY_API_KEY` - Your Tavily search API key

## Step 3: Test Locally

Before deploying, test the graph locally:

```bash
# Start local LangGraph server
langgraph dev

# This will start a local server at http://localhost:8123
```

You can then test the API using curl or the LangGraph Studio UI.

## Step 4: Deploy to LangGraph Cloud

```bash
# Login to LangGraph Cloud
langgraph login

# Deploy your graph
langgraph deploy

# Follow the prompts to:
# 1. Select or create a deployment
# 2. Configure environment variables
# 3. Confirm deployment
```

## Step 5: Configure Environment Variables

After deployment, set your environment variables:

```bash
langgraph env set ANTHROPIC_API_KEY="your-key-here"
langgraph env set TAVILY_API_KEY="your-key-here"
```

## Using the Deployed API

Once deployed, you'll get an API endpoint. Here's how to use it:

### Python Client

```python
from langgraph_sdk import get_client

# Connect to your deployment
client = get_client(url="your-deployment-url")

# Create a thread
thread = await client.threads.create()

# Run the travel agent
input_data = {
    "messages": [],
    "source": "San Francisco, USA",
    "destination": "Tokyo, Japan",
    "start_date": "2024-06-15",
    "end_date": "2024-06-22",
    "preferences": "Mid-range budget, local culture",
    "hobbies": "Photography, food, temples",
    "destination_info": "",
    "itinerary": "",
    "accommodations": "",
    "activities": "",
    "final_plan": ""
}

run = await client.runs.create(
    thread_id=thread["thread_id"],
    assistant_id="travel_agent",
    input=input_data
)

# Wait for completion and get result
result = await client.runs.join(
    thread_id=thread["thread_id"],
    run_id=run["run_id"]
)

print(result["final_plan"])
```

### HTTP API

```bash
# Create a thread
curl -X POST "your-deployment-url/threads" \
  -H "x-api-key: your-api-key"

# Run the agent
curl -X POST "your-deployment-url/threads/{thread_id}/runs" \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "travel_agent",
    "input": {
      "messages": [],
      "source": "San Francisco, USA",
      "destination": "Tokyo, Japan",
      "start_date": "2024-06-15",
      "end_date": "2024-06-22",
      "preferences": "Mid-range budget",
      "hobbies": "Photography, food",
      "destination_info": "",
      "itinerary": "",
      "accommodations": "",
      "activities": "",
      "final_plan": ""
    }
  }'

# Get the result
curl "your-deployment-url/threads/{thread_id}/runs/{run_id}" \
  -H "x-api-key: your-api-key"
```

## Monitoring and Logs

View logs and monitor your deployment:

```bash
# View logs
langgraph logs

# Check deployment status
langgraph status
```

## Updating Your Deployment

After making changes:

```bash
git add .
git commit -m "Update travel agent"
langgraph deploy
```

## Local Development with LangGraph Studio

LangGraph Studio provides a visual interface for testing:

```bash
# Install LangGraph Studio (macOS)
brew install --cask langgraph-studio

# Open your project
langgraph studio
```

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**
   - Ensure `ANTHROPIC_API_KEY` and `TAVILY_API_KEY` are set in the cloud environment

2. **Import Errors**
   - Verify all dependencies are in `requirements.txt`
   - Check that the graph path in `langgraph.json` is correct

3. **Graph Not Found**
   - Ensure `travel_agent_graph` is properly exported in `graph.py`
   - Check the path in `langgraph.json` matches your file structure

### Debug Locally

```bash
# Run with verbose logging
langgraph dev --verbose

# Test specific nodes
langgraph test
```

## Cost Considerations

- Each run will use Claude API calls (Anthropic)
- Web searches will use Tavily API calls
- Monitor your usage in the respective dashboards

## Security Best Practices

1. Never commit API keys to git
2. Use environment variables for all secrets
3. Rotate API keys regularly
4. Monitor API usage for anomalies

## Resources

- [LangGraph Cloud Documentation](https://langchain-ai.github.io/langgraph/cloud/)
- [LangGraph SDK](https://github.com/langchain-ai/langgraph-sdk)
- [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio)
