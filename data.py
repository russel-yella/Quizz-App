import requests

parameters={
    "amount" : 10,
    "type" : "boolean"
}

url = "https://opentdb.com/api.php"

response = requests.get(url,params=parameters)
response.raise_for_status()

data = response.json()
question_data = data["results"]