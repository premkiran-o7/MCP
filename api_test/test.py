from us_api import get_us_agent_details
from canada_api import get_canada_agent

print("### US:")
print(get_us_agent_details('75462'))
print("-"*20)


print("### Canada:")
print(get_canada_agent("toronto"))
print("-"*20)