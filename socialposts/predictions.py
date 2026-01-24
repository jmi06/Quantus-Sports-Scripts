import argparse
from dotenv import load_dotenv
from matplotlib import font_manager, pyplot as plt
import requests
import json
import datetime
from zoneinfo import ZoneInfo
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser()
parser.add_argument("--sport")
args = parser.parse_args()
print(args.sport)

if args.sport == "NHLhockey":
    sport = "hockey"
    league = "nhl"
    sport_color="#c5a7e7"
    home_color = "#a7c7e7"
    away_color = "#e7a7e5"
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
        html,body {{background-color: #232931; height: 800px; margin:0;}}
        *{{font-family: "Ubuntu", sans-serif;}}
        .predictions{{
        width: 800px;
        height: 750px;

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
    html_content+=  f"<h4 style='text-align:center; width: 100%; margin-top: 56%; left: 50%; transform: translateX(-50%); position:fixed; bottom:0; font-weight: 400; font-size: 3vh; color:white; margin: 5px;'>QuantusSports.pages.dev/{sport}</h4>"

    with open(f'socialposts/{args.sport}_predictions.html', 'w') as file:
        file.write(html_content)

    abs_path = os.path.abspath(f"socialposts/{args.sport}_predictions.html")
    file_url = f"file://{abs_path}"
    print(file_url)
    command = [
            "chromium", 
            "--headless=new",
            f"--screenshot={f'socialposts/{args.sport}_prediction.png'}",
            "--virtual-time-budget=5000",
            '--force-device-scale-factor=2',
            f'--run-all-compositor-stages-before-draw ',
            "--window-size=800,1080",
            "--hide-scrollbars",
            file_url
        ]
    subprocess.run(command, check=True)


def getUpcomingGames(teamRatings, sport):

    today = datetime.date.today().isoformat().replace('-','')
    
    print(today)

    try:
        api_request = requests.get(f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard?dates={today}")

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



def create_post(sport):
    global mlb_team_hashtags

    config = {
        "NBAbasketball" :{
            "platform": "QuantusBasketball",
            "tag": "NBA"
        },
        "NHLhockey" :{
            "platform": "QuantusHockey",
            "tag": "NHL"

        },
        "MLBbaseball" :{
            "platform": "QuantusBaseball",
            "tag": "MLB"

        }
    }

    load_dotenv(f"{sport}.env")

    BLUESKY_HANDLE = os.getenv('BLUESKY_USERNAME')
    BLUESKY_PASSWORD = os.getenv('BLUESKY_PASSWORD')

    # Using a trailing "Z" is preferred over the "+00:00" format
    now = datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

    postNow = datetime.now()

    formatted_time = postNow.strftime("%I:%M %p")

    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_PASSWORD},

    )

    session = resp.json()

    accessJwt = session["accessJwt"]

    with open(f'socialposts/{sport}_prediction.png', "rb") as f:
        img_bytes = f.read()

    if len(img_bytes) > 1000000:
        raise Exception(
            f"image file size too large. 1000000 bytes maximum, got: {len(img_bytes)}"
        )


    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.repo.uploadBlob",
        headers={
            "Content-Type": 'image/png',
            "Authorization": "Bearer " + session["accessJwt"],
        },
        data=img_bytes,
    )


    blob = resp.json()["blob"]

    postinfo = {}
    with open(f'{sport}/post.json') as postfile:
        postinfo = json.load(postfile)

    posttext = f"{config[sport]['league']} predictions for {datetime.date.today().isoformat()} \n#{config[sport]['tag']}\n QuantusSports.pages.dev"

    facets = [
        {
            "index": {
                "byteStart": posttext.find("https://QuantusSports.pages.dev/"),
                "byteEnd": posttext.find("https://QuantusSports.pages.dev/") + len("https://QuantusSports.pages.dev/")
            },
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": "https://QuantusSports.pages.dev/"}]
        },
        {
            "index": {
                "byteStart": posttext.find(config[sport]['tag']),
                "byteEnd": posttext.find(config[sport]['tag']) + len(config[sport]['tag'])
            },
            "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": config[sport]['tag'][1:]}]
        }
    ]

    post = {
        "$type": "app.bsky.feed.post",
        "text": posttext,
        "createdAt": now,
        'facets': facets
    }




    

    post["embed"] = {
        "$type": "app.bsky.embed.images",
        "images": [{
            "alt": "",
            "image": blob,
            "aspectRatio": {"width": 313, "height": 236}
        }],
    }

    attempts = 0
    try:
        resp = requests.post(
            "https://bsky.social/xrpc/com.atproto.repo.createRecord",
            headers={"Authorization": "Bearer " + session["accessJwt"]},
            json={
                "repo": session["did"],
                "collection": "app.bsky.feed.post",
                "record": post,
            },
        )
    except Exception as e:
        print('bluesky is beefing',e)
        attempts+=1
        if attempts < 3:
            create_post()
    print('posted to bluesky')

