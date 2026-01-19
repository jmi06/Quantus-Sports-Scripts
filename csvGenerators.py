import json
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import argparse


config = {
    "MLBbaseball":{
        "start": "2026-03-25",
        "games": 162

    },
    "NBAbasketball":{
        "start": "2025-10-21",
        "games": 82
    },
    "NHLhockey":{
        "start": "2025-10-07",
        "games": 82
    }

}

parser = argparse.ArgumentParser()
parser.add_argument("--sport")
args = parser.parse_args()


START_DATE = config[args.sport]['start']
END_DATE = datetime.now().strftime("%Y-%m-%d")
GAMES_NUM = config[args.sport]['games']
team_names = set()



with open(f'{args.sport}/games.json', 'r') as file:
    games = json.load(file)
    
for game in games.values():
    if 'team_1' in game:
        team_names.add(game['team_1']['team_name'])
    if 'team_2' in game:
        team_names.add(game['team_2']['team_name'])

sorted_teams = sorted(list(team_names))



def byGame():

    game_len = {team: 0 for team in sorted_teams}

    df = pd.DataFrame(index=sorted_teams, columns=range(1,GAMES_NUM+1))


    for game in games.values():
        t1_name = game['team_1']['team_name']
        t1_elo = game['team_1']['elo_after']
        
        if t1_name in game_len:
            game_len[t1_name] += 1
            col_idx = game_len[t1_name]
            
            if col_idx <= GAMES_NUM: 
                df.at[t1_name, col_idx] = t1_elo

        t2_name = game['team_2']['team_name']
        t2_elo = game['team_2']['elo_after']

        if t2_name in game_len:
            game_len[t2_name] += 1
            col_idx = game_len[t2_name]

            if col_idx <= 82:
                df.at[t2_name, col_idx] = t2_elo                


        df.to_csv('eloGame.csv')


    with open(f'{args.sport}/order.json', 'r') as file:
        orderFile = json.load(file)


    orderFile['byGame'] = df.to_string()

    with open(f'{args.sport}/order.json', 'w') as file:
        json.dump(orderFile, file)




    return


def byDate():


    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    formatted_dates = date_range.strftime("%Y-%m-%d")
    df = pd.DataFrame(index=sorted_teams, columns=date_range)

    teamsGames = {}

    for game in games.values():
        date = game['date']
        if date in df.columns:

            t1_name = game['team_1']['team_name']
            t1_elo = game['team_1']['elo_after']
            df.at[t1_name, date] = t1_elo

            t2_name = game['team_2']['team_name']
            t2_elo = game['team_2']['elo_after']
            df.at[t2_name, date] = t2_elo

            df = df.ffill(axis=1)

        df.to_csv(f'{args.sport}/eloDate.csv')


    with open(f'{args.sport}/order.json', 'r') as file:
        orderFile = json.load(file)


    orderFile['byDate'] = df.to_string()

    with open(f'{args.sport}/order.json', 'w') as file:
        json.dump(orderFile, file)




    return

byDate()
byGame()



with open(f'{args.sport}/order.json','r') as file:
    orderedFile = file

#ADD TEAMS TO THE ELO DB
load_dotenv(f'{args.sport}.env')


GAMES_API_TOKEN = os.getenv('GAMES_API_TOKEN')

GAMES_ACCOUNT_ID = os.getenv('GAMES_ACCOUNT_ID')
GAMES_NAMESPACE_ID = os.getenv('GAMES_NAMESPACE_ID')




BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{GAMES_ACCOUNT_ID}/storage/kv/namespaces/{GAMES_NAMESPACE_ID}/values/byGame"

HEADERS = {
    "Authorization": f"Bearer {GAMES_API_TOKEN}",
    "Content-Type": "application/json"
}

try:
    response = requests.get(BASE_URL, headers=HEADERS)
    response = requests.put(
        BASE_URL,
        headers=HEADERS,
        data=json.dumps(orderedFile)
    )
    print('Games Added')
except:
    print('error')