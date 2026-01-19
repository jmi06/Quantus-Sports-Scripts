import requests
import json
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--sport")
args = parser.parse_args()


config = {
    "MLBbaseball":{
        "start": "2026-03-25",
        "games": 162,
        "sport": "baseball",
        "league": "mlb"

    },
    "NBAbasketball":{
        "start": "2025-10-21",
        "games": 82,
        "league": "nba",
        "sport":"basketball"
    },
    "NHLhockey":{
        "start": "2025-10-07",
        "games": 82,
        "league": "nhl",
        "sport": "hockey"
    }

}


with open(f'{args.sport}/games.json') as file:
    games = json.load(file)

with open(f'{args.sport}/teams.json') as file:
    teams = json.load(file)



from datetime import date, timedelta

startstr = config[args.sport]['start'].split('-')
start_date = date(int(startstr[0]), int(startstr[1]), int(startstr[2]))
end_date = date.today()

delta = timedelta(days=1)
current_date = start_date
dates = []
while current_date <= end_date:
    dates.append(current_date.strftime('%Y%m%d'))
    current_date += delta




#https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=20250318
def fetch_games(date):

    api_url = f'https://site.api.espn.com/apis/site/v2/sports/{config[args.sport]['sport']}/{config[args.sport]['league']}/scoreboard?dates={date}'


    api_request = requests.get(api_url)
    api_request = api_request.json()
    print('called api')

    game_list = api_request['events']

    keepGoing = False
    for i in game_list:
        if i['status']['type']['name'] != 'STATUS_FINAL':
            keepGoing = True





    for game in game_list:
        # game_identifier = f"{game['id']} {game['date']} {game['competitions'][0]['attendance']} {game['competitions'][0]['competitors'][0]['records'][0]['summary']}"
        game_identifier = game['uid']

        teams[game['competitions'][0]['competitors'][0]['team']['displayName']]['record'] = game['competitions'][0]['competitors'][0]['records'][0]['summary']
        teams[game['competitions'][0]['competitors'][1]['team']['displayName']]['record'] = game['competitions'][0]['competitors'][1]['records'][0]['summary']
            

        if game['season']['slug'] == 'regular-season' and game_identifier not in games and game['status']['type']['name'] == 'STATUS_FINAL':
            
            games[game_identifier] = {'socialpost': True, 'points_diff': abs(   float(game['competitions'][0]['competitors'][0]['score']) - float(game['competitions'][0]['competitors'][1]['score'])   ), 'date': game['date'].split("T")[0] } 

            games[game_identifier]['team_1'] = {'team_name': game['competitions'][0]['competitors'][0]['team']['displayName'],
                                           'winner': game['competitions'][0]['competitors'][0]['winner'],
                                           'score': game['competitions'][0]['competitors'][0]['score'],
                                           'logo': game['competitions'][0]['competitors'][0]['team']['logo'],
                                           

                                           'record': game['competitions'][0]['competitors'][0]['records'][0]['summary']}
            games[game_identifier]['team_2'] = {'team_name': game['competitions'][0]['competitors'][1]['team']['displayName'],
                                           'winner': game['competitions'][0]['competitors'][1]['winner'],
                                           'score': game['competitions'][0]['competitors'][1]['score'],
                                           'logo': game['competitions'][0]['competitors'][1]['team']['logo'],


                                           

                                           'record': game['competitions'][0]['competitors'][1]['records'][0]['summary']}



    with open(f'{args.sport}/games.json', 'w') as file:
        json.dump(games, file)



for i in dates:
    print(i)
    fetch_games(i)
    time.sleep(1)



