import argparse
from matplotlib import font_manager, pyplot as plt
import requests
import json
import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser()
parser.add_argument("--sport")
args = parser.parse_args()
print(args.sport)

if args.sport == "NHLhockey":
    sport = "hockey"
    league = "nhl"
    sport_color="#c5a7e7"
    home_color = "#e7b0a7"
    away_color = "#e7a7da"
if args.sport == "MLBbaseball":
    sport = "baseball"
    league = "mlb"
    sport_color = "#a7e7b1"
    home_color = "#91ffa3"
    away_color = "#63b3ed"


if args.sport == "NBAbasketball":
    sport = "basketball"
    league = "nba"
    sport_color = "#e7bba7"
    home_color = "#e7b0a7"
    away_color = "#e7a7da"

times= []
games = []


def buildGraphic(api_data):

    html_content =f'''
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');
        html{{background-color: #232931}}
        *{{font-family: "Ubuntu", sans-serif;}}
        .predictions{{
        width: 800px;
        height: 900px;

        display:flex;
        flex-direction:column;
        margin:auto;

        justify-content: space-evenly;

        
        }}
        h3{{
        text-align:center;
        }}
        .game-row{{
            align-items: center;
            justify-content: center;
            margin: 0;
            line-height: 1;
            white-space:nowrap;
            font-weight: 400;

            
            font-size: min(
                6vh,   /* height-based limit */
                3.5vw  /* width-based limit */
            );
        }}
        </style>

        <h1 style="text-align:center; font-size: 5vh; margin-top: 15px; margin-bottom: 5px; color:{sport_color}">{league.upper()} Predictions</h1>
        <h3 style="text-align:center; font-size: 3vh; color:white; margin: 5px;">{datetime.date.today().isoformat()}</h3>
        <h4 style="text-align:center; font-size: 2vh; margin: 15px; font-weight: 400; color: white;">Accuracy: {round( (int(info['predictionAccuracy']['acc'].split('-')[0]) / (int(info['predictionAccuracy']['acc'].split('-')[0]) + int(info['predictionAccuracy']['acc'].split('-')[1])))*100, 1) }%</h4>
        <div class="predictions">

        '''
        
    for game in games:
        
        first_part = game[:game.index('@')]
        second_part = game[game.index('@')+1: game.index('|')]
        third_part = game[game.index('|')+1:]
        if first_part.strip() in third_part:
            winner = first_part.strip()
            winnercolor = home_color
        else:
            winner = second_part.strip()
            winnercolor = away_color

        print(f"{first_part}@{second_part}|{third_part}---{winner}")

        html_content += f"<h3 class='game-row' style='color: white;'><span id='hometeam' style='color:{home_color}'>{first_part.strip()}</span> @ <span id='awayteam' style='color:{away_color}'>{second_part.strip()}</span> | <span style='color:{winnercolor}'>{third_part.strip()}</span></h3>\n"

    html_content += "</div>"
    html_content+=  f"<h4 style='text-align:center; width: 100%; left: 50%; transform: translateX(-50%); position:fixed; bottom:0; font-weight: 400; font-size: 3vh; color:white; margin: 5px;'>QuantusSports.pages.dev/{sport}</h4>"

    with open(f'socialposts/{args.sport}_predictions.html', 'w') as file:
        file.write(html_content)


def getUpcomingGames(teamRatings, sport):

    today = datetime.date.today().isoformat().replace('-','')
    
    print(today)

    try:
        api_request = requests.get(f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard?dates={today}")
        # api_request = requests.get(f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard?dates=20250419")

        api_request = api_request.json()

    except Exception as e:
        print("ERROR:", e)
        getUpcomingGames(teamRatings, sport)


    for i in api_request['events']:
        if i['season']['slug'] == 'regular-season':
            date_string = i['date']
            date_utc = datetime.datetime.fromisoformat(date_string.replace("Z", "+00:00"))
            date_eastern = date_utc.astimezone(ZoneInfo("America/New_York"))
            date_eastern = date_eastern.strftime("%I:%M %p")
            homeTeamShort =  i['competitions'][0]['competitors'][0]['team']['shortDisplayName']
            awayTeamShort =  i['competitions'][0]['competitors'][1]['team']['shortDisplayName']

            homeTeam =  i['competitions'][0]['competitors'][0]['team']['displayName']
            awayTeam =  i['competitions'][0]['competitors'][1]['team']['displayName']
        
            homeTeamRating = teamRatings['all'][homeTeam]['elo']
            awayTeamRating = teamRatings['all'][awayTeam]['elo']
        
            homeTeamProb = round((1 / (1+10** ((awayTeamRating-homeTeamRating)/400) ))*100, 1)
            awayTeamProb = round((1 / (1+10** ((homeTeamRating-awayTeamRating)/400) ))*100, 1)

            prob = 0
            favoured = ''
            if homeTeamProb > awayTeamProb:
                prob = homeTeamProb
                favoured = homeTeamShort
            elif homeTeamProb < awayTeamProb:
                prob = awayTeamProb
                favoured = awayTeamShort
            elif homeTeamProb == awayTeamProb:
                prob = 50
                favoured = "Tie"


            times.append(date_eastern)
            games.append(f"{homeTeamShort} @ {awayTeamShort} | {prob}% {favoured}")

    buildGraphic(api_request)

info = {}
with open(f"{args.sport}/order.json", "r") as file:
    info = json.load(file)

getUpcomingGames(info, sport)
print(games)

