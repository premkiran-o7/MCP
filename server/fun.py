from typing import Any
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('Fun-Assistant')

def fetch_json(url: str) -> dict[str, Any] | None:
    """Generic helper to get JSON from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching from {url}: {e}")
        return None

@mcp.tool()
def get_chuck_norris_joke() -> str:
    """Fetches a random Chuck Norris joke."""
    url = "https://api.chucknorris.io/jokes/random"
    data = fetch_json(url)
    return data.get("value", "No joke found!") if data else "Failed to fetch Chuck Norris joke."

@mcp.tool()
def get_zen_quote() -> str:
    """Fetches a random inspirational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/quotes/"
    data = fetch_json(url)
    if data and isinstance(data, list) and len(data) > 0:
        quote = data[0]
        return f'"{quote["q"]}" — {quote["a"]}'
    return "Failed to fetch quote."

@mcp.tool()
def get_random_joke() -> str:
    """Fetches a random joke from JokeAPI."""
    url = "https://v2.jokeapi.dev/joke/Any"
    data = fetch_json(url)
    if not data:
        return "Failed to fetch joke."

    if data.get("type") == "single":
        return data["joke"]
    elif data.get("type") == "twopart":
        return f"{data['setup']} ... {data['delivery']}"
    return "No joke found."

@mcp.tool()
def search_book(query: str) -> str:
    """Searches for books by title using OpenLibrary."""
    url = f"https://openlibrary.org/search.json?q={query.replace(' ', '+')}"
    data = fetch_json(url)
    if not data or not data.get("docs"):
        return f"No books found for query: {query}"

    results = data["docs"][:3]
    output = f"Top results for '{query}':\n"
    for book in results:
        title = book.get("title", "Unknown Title")
        author = ", ".join(book.get("author_name", ["Unknown Author"]))
        year = book.get("first_publish_year", "Unknown Year")
        output += f"\n📘 {title} by {author} ({year})"
    return output
