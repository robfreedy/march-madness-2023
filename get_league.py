from prefect import flow, task
from prefect.blocks.system import Secret
from prefect.context import get_run_context, get_settings_context
import requests
import json


secret_block = Secret.load("basketball-api-key")
api_key = secret_block.get()
base_url = "https://api-basketball.p.rapidapi.com"
headers = {
	    "X-RapidAPI-Key": api_key,
	    "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
}

@task(log_prints=True)
def get_standings() -> int:
    url = base_url + "/leagues"
    querystring = {"season":"2022-2023", "type":"league", "country" : "USA", "name" : "NCAA"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return 0

@flow(log_prints=True)
def main():
    league_id = get_standings()
