import os
from dotenv import load_dotenv
import requests


load_dotenv()

us_url = "https://realty-in-us.p.rapidapi.com/agents/list"


us_headers = {
	"x-rapidapi-key": os.getenv("x_rapidapi_key"),
	"x-rapidapi-host": "realty-in-us.p.rapidapi.com"
}


def get_us_agent_details(postal_code: int) -> str:
    querystring = {"postal_code":postal_code,"offset":"0","limit":"3","sort":"recent_activity_high","types":"agent"}

    response = requests.get(us_url, headers=us_headers, params=querystring)

    results = response.json()
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
    