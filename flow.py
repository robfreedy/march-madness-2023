from prefect import flow, task
from prefect.blocks.system import Secret
from prefect.task_runners import ConcurrentTaskRunner
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
def calculate_score(team_stats : dict) -> float:
    points_for = team_stats['response']['points']['for']['average']['all'] 
    points_against = team_stats['response']['points']['against']['average']['all']
    win_percentage = team_stats['response']['games']['wins']['all']['percentage']
    if points_for == None or points_against == None or win_percentage == None:
        print(team_stats)
    score = (0.1 * float(points_for)) + (10 * float(win_percentage)) - (0.1 * float(points_against))
    return score

@task(log_prints=True)
def get_stats(id: int) -> dict:
    try:
        querystring = {"league":"116","season":"2022-2023", "team": id}
        url = "https://api-basketball.p.rapidapi.com/statistics"
        response = requests.request("GET", url, headers=headers, params=querystring)
        return json.loads(response.content)
    except Exception as e:
        print(f"There was an issue getting the initial statistics for team with id: {id}")
        raise e

@task(log_prints=True)
def rank_winners(teams : dict):
    return dict(sorted(teams.items(), key=lambda item: item[1]['score'], reverse=True))

@flow(log_prints=True, task_runner=ConcurrentTaskRunner())
def pick_initial_winners(team_stats: dict) -> dict:
    initial_winners = {}
    with open('teams.json') as teams_file:
        teams = json.load(teams_file)
        for team in teams.values():
            opponent_id = team["opponent"]
            id = team["id"]
            if opponent_id != None:
                score = calculate_score(team_stats[id])
                opponent_score = calculate_score(team_stats[opponent_id])
                if score >= opponent_score:
                    initial_winners[id] = {
                        'score': score, 
                        'name': team_stats[id]['response']['team']['name']}
            else:
                initial_winners[id] = {
                    'score': calculate_score(team_stats[id]), 
                    'name': team_stats[id]['response']['team']['name']}
    return initial_winners

'''
This function calls the API for
'''
@flow(log_prints=True, task_runner=ConcurrentTaskRunner())
def get_all_teams_stats() -> dict:
    all_team_stats = {}
    with open('teams.json') as teams_file:
        teams = json.load(teams_file)
        for team in teams.values():
            id = team["id"]
            all_team_stats[id]= get_stats.submit(id)
    return all_team_stats

@flow(log_prints=True)
def main():
    # Getting all of the team stats
    team_stats = get_all_teams_stats()

    # Picking the initial winners for everyone's first games
    initial_winners = pick_initial_winners(team_stats)

    # Ranking the initial winners in order to fill out the rest of the bracket
    rankings = rank_winners(initial_winners)

    # Printing out the rankings
    i = 1
    for id, value in rankings.items():
        print(f"{i}. {value['name']}")
        i += 1
    

main()