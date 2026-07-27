from google import genai
import os
from dotenv import load_dotenv
import json
from tools.currency import convert_currency
from tools.weather import get_weather
from tools.search import search_google
from tools.maps import get_distance

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def decide_tool(query):
    prompt = f"""
    You are an AI agent.

    Decide which tool(s) to use based on the user query.

    Available tools:
    1. weather → for weather information
    2. currency → for currency conversion
    3. search → for latest information/news
    4. maps → for distance between two places

    Return ONLY a JSON LIST (no explanation).

    Formats:

    Weather:
    {{ "tool": "weather", "city": "Delhi" }}

    Currency:
    {{ "tool": "currency", "amount": 100, "from": "USD", "to": "INR" }}

    Search:
    {{ "tool": "search", "query": "latest AI news" }}

    Maps:
    {{ "tool": "maps", "from": "Mumbai", "to": "Pune" }}

    IMPORTANT:
    - Always return a LIST of actions
    - Even if one tool → return list with one item
    - No text, no explanation, only JSON
    - Extract correct city names for maps queries

    Examples:

    Query: What is the weather in Delhi?
    [
    {{ "tool": "weather", "city": "Delhi" }}
    ]

    Query: Convert 100 USD to INR
    [
    {{ "tool": "currency", "amount": 100, "from": "USD", "to": "INR" }}
    ]

    Query: Distance between Mumbai and Pune
    [
    {{ "tool": "maps", "from": "Mumbai", "to": "Pune" }}
    ]

    Query: Weather in Delhi and convert 100 USD to INR
    [
    {{ "tool": "weather", "city": "Delhi" }},
    {{ "tool": "currency", "amount": 100, "from": "USD", "to": "INR" }}
    ]

    Query: Weather in Delhi and distance between Mumbai and Pune
    [
    {{ "tool": "weather", "city": "Delhi" }},
    {{ "tool": "maps", "from": "Mumbai", "to": "Pune" }}
    ]

    Query: Latest news about AI
    [
    {{ "tool": "search", "query": "latest AI news" }}
    ]

    Query: {query}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
    except:
        print("Main model busy... using backup")
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

    return response.text

def handle_query(query):
    decision = decide_tool(query)

    try:
        clean = decision.strip().replace("```json", "").replace("```", "")
        actions = json.loads(clean)   # now it's a LIST
    except:
        return f"Error understanding query: {decision}"

    results = []

    for action in actions:

        if action["tool"] == "weather":
            city = action["city"].replace("?", "").strip().title()
            results.append(get_weather(city))

        elif action["tool"] == "currency":
            results.append(
                convert_currency(
                    action["amount"],
                    action["from"],
                    action["to"]
                )
            )

        elif action["tool"] == "search":
            raw_data = search_google(action["query"])
            
            if not raw_data:
                results.append("No useful results found")
            else:
                results.append(
                    summarize_with_llm(raw_data, action["query"])
                )

        elif action["tool"] == "maps":
            results.append(
                get_distance(
                    action["from"],
                    action["to"]
                )
            )
            
        else:
            results.append("Tool not supported")

    return "\n".join(results)

def summarize_with_llm(text, query):
    prompt = f"""
    Answer the user's query using the information below.

    Query: {query}

    Information:
    {text}

    Give a complete, clear, and natural answer.
    Do not give bullet points.
    Do not give incomplete sentences.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
    except:
        print("Summarizer model busy... using backup")
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

    return response.text

if __name__ == "__main__":
    query = input("Ask something: ")
    print(handle_query(query))