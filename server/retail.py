from typing import Any
import os
from dotenv import load_dotenv
import requests
from mcp.server.fastmcp import FastMCP
import asyncio

ca_url = "https://realty-in-ca1.p.rapidapi.com/agents/list"



ca_headers = {
	"x-rapidapi-key": os.getenv("x_rapidapi_key"),
	"x-rapidapi-host": "realty-in-ca1.p.rapidapi.com"
}

us_url = "https://realty-in-us.p.rapidapi.com/agents/list"


us_headers = {
	"x-rapidapi-key": os.getenv("x_rapidapi_key"),
	"x-rapidapi-host": "realty-in-us.p.rapidapi.com"
}


mcp = FastMCP('Retail-Assistant')




def get_canada_agent(City: str) -> dict[str:Any]|None:
    """Make a request to get agents info from canada using api"""
    querystring = {"CurrentPage":"1","RecordsPerPage":"3","SortOrder":"A","SortBy":"11","CultureId":"1","City":City}
    response = requests.get(ca_url, headers=ca_headers, params=querystring)

    return response.json()

    

@mcp.tool()
def get_agencies_canada(City:str) -> str:
    """Get agencies details operating in a city in Canada.

    Args:
        City: A string, City name(e.g. Toronto)
    """

    results = get_canada_agent(City)
    print(f"{results['Results']}")
    if not results or 'Results' not in results:
        return "Unable to fetch results for the given city in Canada"
    
    else:
     
        op = ""
        for result in results['Results']:
            agent_info = f"""
            Agent: 
    Title: {result['Organization']['Name']}
    Phone: {result['Phones'][0]['PhoneType']} : 
    Area Code: {result['Phones'][0]['AreaCode']}, Number: {result['Phones'][0]['PhoneNumber']}
                                                        
            """

            op+=agent_info
        return op


def get_us_agents(postal_code: int) -> dict[str:Any]|None:
    """Make a request to get agents info from USA/America using api"""
    querystring = {"postal_code":postal_code,"offset":"0","limit":"3","sort":"recent_activity_high","types":"agent"}

    response = requests.get(us_url, headers=us_headers, params=querystring)

    return response.json()

    

@mcp.tool()
async def get_agencies_us(postal_code:str) -> str:
    """Get agencies details operating in America using Postal Code.

    Args:
        postal_code: A string, Postal Code in US/America
    """

    results = get_us_agents(postal_code)
    if not results or 'agents' not in results:
        return "Unable to ftech results for the given postal code in America"
    
    else:
        op = ""

        for result in results['agents']:
            agent_info = f"""
            Agent: 
    Title: {result['name']}
    Email: {result['email']}
    Phone: {result['phones'][0]['type']} : {result['phones'][0]['ext']}  {result['phones'][0]['number']}
    Rating: {result['agent_rating']} 
                                                          
            """

            op+=agent_info

        

        return op