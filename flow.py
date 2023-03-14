from prefect import flow, task
from prefect.blocks.system import Secret
from prefect.context import get_run_context, get_settings_context
import requests
import json
from prefect.server.schemas.states import Completed, Failed


secret_block = Secret.load("basketball-api-key")
api_key = secret_block.get()
base_url = "https://api-basketball.p.rapidapi.com"
headers = {
	    "X-RapidAPI-Key": api_key,
	    "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
}

@task(log_prints=True)
def get_standings() -> dict:
    try:
        querystring = {"league":"116","season":"2022-2023"}
        url = "https://api-basketball.p.rapidapi.com/standings"
        response = requests.request("GET", url, headers=headers, params=querystring)
        return json.loads(response)
    except Exception as e:
        print("There was an issue getting the NCAA standings")
        raise e
    
@flow(log_prints=True)
def filter_league_standings(league_standings : dict) -> dict:
    filtered_standings = {}
    with open('teams.json') as teams_file:
        teams = json.load(teams_file)
        for team_id in teams.values():
            

@task(log_prints=True)
def pick_winner(team1: int, team2: int):
    # Important factors: 
    # Win percentage
    # Points For
    # Points Against
    print("Picking the winner based on record, quadrant, and seeding")
    print(team1)
    print(team2)

@flow(log_prints=True)
def main():
    league_standings = get_standings()
    filtered_league_standings = filter_league_standings()

main()