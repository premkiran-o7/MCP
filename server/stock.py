from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("assistant")

objects_api = "https://api.restful-api.dev/objects"


async def fetch_objects(url: str) -> dict[str, Any] | None:
    """Make a request to get objects api with error handling"""
    headers = {"content-type": "application/json"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url = url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        

@mcp.tool(name = "get_objects", description="Get a list of objects from your stock/storage api")
async def get_objects() -> str:
    """Get a list of objects from your stock/storage api"""

    objects_data = await fetch_objects(objects_api)


    if not objects_data:
        return "Unable to fetch objects data from your local store"
    
    result_lines = []

    for obj in objects_data[:5]:  # Limit to first 5 for brevity
        name = obj.get("name", "Unnamed")
        data = obj.get("data") or {}
        
        details = "\n  ".join([f"{k}: {v}" for k, v in data.items()]) if data else "No data available"
        result_lines.append(f"📦 {name}\n  {details}")

    return "\n\n".join(result_lines)



if __name__ == "__main__":
    mcp.run(transport="stdio")
    


 