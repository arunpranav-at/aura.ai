import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from config import get_config, AppConfig

config: AppConfig = get_config()


def context_generator(query, max_results=5):
    """
    Fetches search results from Bing API and generates context by fetching page contents.

    Args:
        query (str): The search query to find context for.
        max_results (int): Number of results to fetch.

    Returns:
        str: A generated context summary from the top search results.
    """

    BING_API_KEY = config.env.bing_api_key
    BING_ENDPOINT = config.env.bing_endpoint

    if not BING_API_KEY:
        raise ValueError(
            "BING_API_KEY not found. Ensure it's set in the .env file.")

    headers = {
        "Ocp-Apim-Subscription-Key": BING_API_KEY
    }
    params = {
        "q": query,
        "count": max_results,
        "mkt": "en-US"
    }

    try:
        response = requests.get(BING_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()

        search_results = response.json()
        context = []

        for idx, result in enumerate(search_results.get("webPages", {}).get("value", [])):
            name = result.get("name", "No title")
            url = result.get("url", "")

            page_content = fetch_page_content(url)

            if page_content:
                context.append(f"{idx + 1}. {name} ({url}):\n{page_content}\n")
            else:
                context.append(
                    f"{idx + 1}. {name} ({url}):\n[Content could not be fetched.]\n")

        return "\n".join(context) if context else "No results found."

    except requests.exceptions.RequestException as e:
        return f"Error fetching context: {e}"


def fetch_page_content(url):
    """
    Fetches the content of a web page and extracts text.

    Args:
        url (str): The URL of the page to fetch.

    Returns:
        str: Extracted text content from the page.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        if response.status_code == 403:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        texts = soup.stripped_strings
        page_content = " ".join(texts)
        return page_content[:2000]

    except requests.exceptions.RequestException:
        return None
