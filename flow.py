from prefect import flow, task
from prefect.blocks.system import Secret
import requests

secret_block = Secret.load("basketball-api-key")
api_key = secret_block.get()
base_url = "https://api-basketball.p.rapidapi.com"
headers = {
	    "X-RapidAPI-Key": api_key,
	    "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
}

@task()
def get_league() -> int:
    url = base_url + "/leagues"
    querystring = {"season":"2022-2023", "type":"league", "country" : "USA", "name" : "NCAA"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    querystring = {"league":"116","season":"2022-2023"}
    url = "https://api-basketball.p.rapidapi.com/standings"
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return 0

@flow()
def main():
    league_id = get_league()

main()