import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_KEY")

def search_google(query):
    api_key = os.getenv("SERPAPI_KEY")

    url = "https://serpapi.com/search"

    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": 5
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        #print(data)
    except Exception as e:
        return "Error fetching search results"

    # REMOVE THIS LINE (causing crash)
    # print(data)

    collected_info = ""
    # Extract relevant info from API response
    if "answer_box" in data:
        answer_box = data["answer_box"]
        if "snippet" in answer_box:
            collected_info += answer_box["snippet"] + "\n"
        if "answer" in answer_box:
            collected_info += str(answer_box["answer"]) + "\n"
    # Also include knowledge graph description if available
    if "knowledge_graph" in data:
        kg = data["knowledge_graph"]
        if "description" in kg:
            collected_info += kg["description"] + "\n"
    # Include top organic results snippets
    if "organic_results" in data:
        for result in data["organic_results"][:5]:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            collected_info += f"{title}. {snippet}\n"

    if not collected_info.strip():
        return None

    return collected_info