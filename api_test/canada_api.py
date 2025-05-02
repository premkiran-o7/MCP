import os
from dotenv import load_dotenv
import requests


load_dotenv()

ca_url = "https://realty-in-ca1.p.rapidapi.com/agents/list"



ca_headers = {
	"x-rapidapi-key": os.getenv("x_rapidapi_key"),
	"x-rapidapi-host": "realty-in-ca1.p.rapidapi.com"
}

def get_canada_agent(City: str) -> dict:
    querystring = {"CurrentPage":"1","RecordsPerPage":"10","SortOrder":"A","SortBy":"11","CultureId":"1","City":City}
    response = requests.get(ca_url, headers=ca_headers, params=querystring)

    results = response.json()
    print(response.status_code)
    print(type(response.status_code))
    print(results)


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
