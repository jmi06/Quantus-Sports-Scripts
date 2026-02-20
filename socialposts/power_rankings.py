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

current_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_dir)




team_colours = {
  "nba": {
    "Atlanta Hawks": { "colour": "#fcbbb6" },
    "Boston Celtics": { "colour": "#b6fcc3" },
    "Brooklyn Nets": { "colour": "#b6d8fc" },
    "Charlotte Hornets": { "colour": "#c8b6fc" },
    "Chicago Bulls": { "colour": "#fcb6f1" },
    "Cleveland Cavaliers": { "colour": "#fcbbb6" },
    "Dallas Mavericks": { "colour": "#b6ddfc" },
    "Denver Nuggets": { "colour": "#f5f5ab" },
    "Detroit Pistons": { "colour": "#b6d8fc" },
    "Golden State Warriors": { "colour": "#f5f5ab" },
    "Houston Rockets": { "colour": "#fcb6f1" },
    "Indiana Pacers": { "colour": "#f5f5ab" },
    "LA Clippers": { "colour": "#b6ddfc" },
    "Los Angeles Lakers": { "colour": "#c8b6fc" },
    "Memphis Grizzlies": { "colour": "#b6d8fc" },
    "Miami Heat": { "colour": "#fcb6f1" },
    "Milwaukee Bucks": { "colour": "#b6fcc3" },
    "Minnesota Timberwolves": { "colour": "#b6ddfc" },
    "New Orleans Pelicans": { "colour": "#b6fcc3" },
    "New York Knicks": { "colour": "#fcbbb6" },
    "Oklahoma City Thunder": { "colour": "#b6d8fc" },
    "Orlando Magic": { "colour": "#b6d8fc" },
    "Philadelphia 76ers": { "colour": "#fcb6f1" },
    "Phoenix Suns": { "colour": "#fcbbb6" },
    "Portland Trail Blazers": { "colour": "#fcb6f1" },
    "Sacramento Kings": { "colour": "#c8b6fc" },
    "San Antonio Spurs": { "colour": "#b6fcc3" },
    "Toronto Raptors": { "colour": "#c8b6fc" },
    "Utah Jazz": { "colour": "#c8b6fc" },
    "Washington Wizards": { "colour": "#b6ddfc" }
  },

  "mlb": {
    "Arizona Diamondbacks": { "colour": "#fcbbb6" },
    "Atlanta Braves": { "colour": "#b6d8fc" },
    "Baltimore Orioles": { "colour": "#f5f5ab" },
    "Boston Red Sox": { "colour": "#fcb6f1" },
    "Chicago Cubs": { "colour": "#b6d8fc" },
    "Chicago White Sox": { "colour": "#b6fcc3" },
    "Cincinnati Reds": { "colour": "#fcb6f1" },
    "Cleveland Guardians": { "colour": "#fcbbb6" },
    "Colorado Rockies": { "colour": "#c8b6fc" },
    "Detroit Tigers": { "colour": "#b6d8fc" },
    "Houston Astros": { "colour": "#f5f5ab" },
    "Kansas City Royals": { "colour": "#b6d8fc" },
    "Los Angeles Angels": { "colour": "#fcb6f1" },
    "Los Angeles Dodgers": { "colour": "#b6d8fc" },
    "Miami Marlins": { "colour": "#b6ddfc" },
    "Milwaukee Brewers": { "colour": "#f5f5ab" },
    "Minnesota Twins": { "colour": "#b6d8fc" },
    "New York Mets": { "colour": "#fcbbb6" },
    "New York Yankees": { "colour": "#b6ddfc" },
    "Oakland Athletics": { "colour": "#b6fcc3" },
    "Philadelphia Phillies": { "colour": "#fcb6f1" },
    "Pittsburgh Pirates": { "colour": "#f5f5ab" },
    "San Diego Padres": { "colour": "#f5f5ab" },
    "San Francisco Giants": { "colour": "#fcbbb6" },
    "Seattle Mariners": { "colour": "#b6fcc3" },
    "St. Louis Cardinals": { "colour": "#fcb6f1" },
    "Tampa Bay Rays": { "colour": "#b6d8fc" },
    "Texas Rangers": { "colour": "#b6ddfc" },
    "Toronto Blue Jays": { "colour": "#b6d8fc" },
    "Washington Nationals": { "colour": "#fcbbb6" }
  },

  "nhl": {
    "Anaheim Ducks": { "colour": "#f5f5ab" },
    "Utah Mammoth": { "colour": "#fcbbb6" },
    "Boston Bruins": { "colour": "#f5f5ab" },
    "Buffalo Sabres": { "colour": "#b6d8fc" },
    "Calgary Flames": { "colour": "#fcb6f1" },
    "Carolina Hurricanes": { "colour": "#fcb6f1" },
    "Chicago Blackhawks": { "colour": "#fcbbb6" },
    "Colorado Avalanche": { "colour": "#b6d8fc" },
    "Columbus Blue Jackets": { "colour": "#b6d8fc" },
    "Dallas Stars": { "colour": "#b6fcc3" },
    "Detroit Red Wings": { "colour": "#fcb6f1" },
    "Edmonton Oilers": { "colour": "#f5f5ab" },
    "Florida Panthers": { "colour": "#fcbbb6" },
    "Los Angeles Kings": { "colour": "#b6ddfc" },
    "Minnesota Wild": { "colour": "#b6fcc3" },
    "Montreal Canadiens": { "colour": "#fcb6f1" },
    "Nashville Predators": { "colour": "#f5f5ab" },
    "New Jersey Devils": { "colour": "#fcb6f1" },
    "New York Islanders": { "colour": "#b6d8fc" },
    "New York Rangers": { "colour": "#b6d8fc" },
    "Ottawa Senators": { "colour": "#fcbbb6" },
    "Philadelphia Flyers": { "colour": "#f5f5ab" },
    "Pittsburgh Penguins": { "colour": "#f5f5ab" },
    "San Jose Sharks": { "colour": "#b6ddfc" },
    "Seattle Kraken": { "colour": "#b6ddfc" },
    "St. Louis Blues": { "colour": "#b6d8fc" },
    "Tampa Bay Lightning": { "colour": "#b6d8fc" },
    "Toronto Maple Leafs": { "colour": "#b6d8fc" },
    "Vancouver Canucks": { "colour": "#b6fcc3" },
    "Vegas Golden Knights": { "colour": "#f5f5ab" },
    "Washington Capitals": { "colour": "#fcb6f1" },
    "Winnipeg Jets": { "colour": "#b6d8fc" }
  }
}


if args.sport == "NHLhockey":
    sport = "hockey"
    league = "nhl"
    sport_color="#c5a7e7"
    home_color = "#e7b0a7"
    away_color = "#e7a7da"
    K = 128
if args.sport == "MLBbaseball":
    sport = "baseball"
    league = "mlb"
    sport_color = "#a7e7b1"
    home_color = "#91ffa3"
    away_color = "#63b3ed"
    K = 128

if args.sport == "NBAbasketball":
    sport = "basketball"
    league = "nba"
    sport_color = "#e7bba7"
    home_color = "#e7b0a7"
    away_color = "#e7a7da"
    K = 64



def buildGraphic(api_data, previous_teams):
    today = datetime.datetime.now()
    last_7_days = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    teams = list(api_data.keys())

    previous_ranking = list(previous_teams.keys())

    print(teams, 'p')

    def getChange(team):
        now_pos = teams.index(team)
        last_pos = previous_ranking.index(team)

        if now_pos < last_pos:
            # climbed the ranking
            return f"<span style='color:#6eff92'>▲ {abs(now_pos-last_pos)}</span>"
        elif now_pos > last_pos:
            # went down
            return f"<span style='color:#ff6e6e'>▼ {abs(now_pos-last_pos)}</span>"
        elif now_pos == last_pos:
            # stayed
            return f"<span style='color:#bababa'>=</span>"




    html_content =f'''
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');
        html{{background-color: #232931; height: 100%;}}
        *{{font-family: "Ubuntu", sans-serif;}}

        h3{{
        text-align:left;
        }}
        .predictions{{
            width: 85%;
            height: 70%;
            text-align: center;
            flex-direction: column;
            margin: auto;
            justify-content: space-evenly;


        }}

        .game-row{{
            align-items: center;
            margin: 30px auto 10px auto;
            line-height: 1;
            white-space: nowrap;
            color: white;
            font-size: min( 6vh, 3.5vw );
            display: flex;
            justify-content: space-between;
            width: 80%;
        }}
        </style>

        <h1 style="text-align:center; font-size: 5vh; margin-top: 15px; margin-bottom: 5px; color:{sport_color}">{league.upper()} PowerRankings</h1>
        <h3 style="text-align:center; font-size: 3vh; color:white; margin: 5px;">Week of {last_7_days[-1]}</h3>
        <div class="predictions">
        <h3 class="game-row"><span style="color:{team_colours[league][teams[0]]['colour']}">#1: {teams[0]}</span>{getChange(teams[0])}</h3>
        <h3 class="game-row"><span style="color:{team_colours[league][teams[1]]['colour']}">#2: {teams[1]}</span>{getChange(teams[1])}</h3>
        <h3 class="game-row"><span style="color:{team_colours[league][teams[2]]['colour']}">#3: {teams[2]}</span>{getChange(teams[2])}</h3>
        <h3 class="game-row"><span style="color:{team_colours[league][teams[3]]['colour']}">#4: {teams[3]}</span>{getChange(teams[3])}</h3>
        <h3 class="game-row"><span style="color:{team_colours[league][teams[4]]['colour']}">#5: {teams[4]}</span>{getChange(teams[4])}</h3>
        <h3 class="game-row"><span style="color:{team_colours[league][teams[5]]['colour']}">#6: {teams[5]}</span>{getChange(teams[5])}</h3>
        <h3 class="game-row"><span style="color:{team_colours[league][teams[6]]['colour']}">#7: {teams[6]}</span>{getChange(teams[6])}</h3>
        <h3 class="game-row"><span style="color:{team_colours[league][teams[7]]['colour']}">#8: {teams[7]}</span>{getChange(teams[7])}</h3>
        <h3 class="game-row"><span style="color:{team_colours[league][teams[8]]['colour']}">#9: {teams[8]}</span>{getChange(teams[8])}</h3>
        <h3 class="game-row"><span style="color:{team_colours[league][teams[9]]['colour']}">#10: {teams[9]}</span>{getChange(teams[9])}</h3>

        '''




    html_content += "</div>"
    html_content+=  f"<h4 style='text-align:center; width: 100%; margin-top: 56%; left: 50%; transform: translateX(-50%); position:fixed; bottom:0; font-weight: 400; font-size: 3vh; color:white; margin: 5px;'>QuantusSports.pages.dev/{sport}</h4>"

    with open(f'{args.sport}_powerrankings.html', 'w') as file:
        file.write(html_content)

    abs_path = os.path.abspath(f"{args.sport}_powerrankings.html")
    file_url = f"file://{abs_path}"
    print(file_url)
    command = [
            "chromium",
            "--headless=new",
            f"--screenshot={f'{args.sport}_powerrankings.png'}",
            "--virtual-time-budget=5000",
            '--force-device-scale-factor=2',
            f'--run-all-compositor-stages-before-draw ',
            "--window-size=800,900",
            "--hide-scrollbars",
            file_url
        ]
    subprocess.run(command, check=True)



def getLast7Days(data, sport):
    print(data)
    today = datetime.datetime.now()
    last_7_days = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    print(last_7_days)
    games = []
    for i in data['games'].values():
        if i['date'] in last_7_days:
            games.append(i)


    teams = data['all']
    for team in teams.values():
        team['elo'] = 1000
        team['games'] = []

    for game in games:
        team1 = game['team_1']
        team2 = game['team_2']

        team1elo = teams[game['team_1']['team_name']]['elo']
        team2elo = teams[game['team_2']['team_name']]['elo']

        team1winprob = 1/(1+10**((team2elo-team1elo)/400))
        team2winprob = 1/(1+10**((team1elo-team2elo)/400))

        team1W = 0
        team2W = 0

        if team1['winner'] == False:
            team1W = 0
            team2W =1
        else:
            team1W = 1
            team2W = 0

        teams[team1['team_name']]['elo'] = team1elo + (K *(team1W-team1winprob))
        teams[team2['team_name']]['elo'] = team2elo + (K *(team2W-team2winprob))

    teams = dict(sorted(teams.items(), key=lambda item: item[1]['elo'], reverse=True))


    today = datetime.datetime.now()
    last_7_days = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6,14)]
    print(last_7_days)
    games = []
    for i in data['games'].values():
        if i['date'] in last_7_days:
            games.append(i)


    previous_teams = data['all']
    for team in previous_teams.values():
        team['elo'] = 1000
        team['games'] = []

    for game in games:
        team1 = game['team_1']
        team2 = game['team_2']

        team1elo = previous_teams[game['team_1']['team_name']]['elo']
        team2elo = previous_teams[game['team_2']['team_name']]['elo']

        team1winprob = 1/(1+10**((team2elo-team1elo)/400))
        team2winprob = 1/(1+10**((team1elo-team2elo)/400))

        team1W = 0
        team2W = 0

        if team1['winner'] == False:
            team1W = 0
            team2W =1
        else:
            team1W = 1
            team2W = 0

        previous_teams[team1['team_name']]['elo'] = team1elo + (K *(team1W-team1winprob))
        previous_teams[team2['team_name']]['elo'] = team2elo + (K *(team2W-team2winprob))

    previous_teams = dict(sorted(previous_teams.items(), key=lambda item: item[1]['elo'], reverse=True))
    print(previous_teams.keys())







    buildGraphic(teams, previous_teams)
    return



info = {}
with open(f"../{args.sport}/order.json", "r") as file:
    info = json.load(file)

with open(f"../{args.sport}/games.json", "r") as file:
    games = json.load(file)


info['games'] = games
getLast7Days(info, sport)





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

    load_dotenv(f"../{args.sport}.env")

    BLUESKY_HANDLE = os.getenv('BLUESKY_USERNAME')
    BLUESKY_PASSWORD = os.getenv('BLUESKY_PASSWORD')

    # Using a trailing "Z" is preferred over the "+00:00" format
    now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

    postNow = datetime.datetime.now()

    formatted_time = postNow.strftime("%I:%M %p")

    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_PASSWORD},

    )

    session = resp.json()

    accessJwt = session["accessJwt"]

    with open(f'{args.sport}_powerrankings.png', "rb") as f:
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
    #with open(f'{sport}/post.json') as postfile:
        #postinfo = json.load(postfile)

    posttext = f"{league.upper()} PowerRankings presented by Quantus{sport.capitalize()}\n\nQuantusSports.pages.dev/{sport}/powerrankings"

    facets = [
        {
            "index": {
                "byteStart": posttext.find(f"QuantusSports.pages.dev/{sport}/powerrankings"),
                "byteEnd": posttext.find(f"QuantusSports.pages.dev/{sport}/powerrankings") + len(f"QuantusSports.pages.dev/{sport}/powerrankings")
            },
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": "https://QuantusSports.pages.dev/{sport}/powerrankings"}]
        },
       # {
       #     "index": {
       #         "byteStart": posttext.find(config[sport]['tag']),
       #         "byteEnd": posttext.find(config[sport]['tag']) + len(config[sport]['tag'])
       #     },
       #     "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": config[sport]['tag'][1:]}]
       # }
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
            "aspectRatio": {"width": 800, "height": 900}
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
        resp.raise_for_status()
    except Exception as e:
        print('bluesky is beefing',e)
        attempts+=1
        if attempts < 3:
            create_post(sport)
    print('posted to bluesky')


create_post(sport)