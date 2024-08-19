import requests

# Use the raw URL to get the raw content
gist_response = requests.get("https://gist.githubusercontent.com/FrankAffatigato/492c49343f06906f5f5ada0a9a401804/raw")

# Assuming the gist content is in JSON format
data = gist_response.json()['full_name']

print(data)