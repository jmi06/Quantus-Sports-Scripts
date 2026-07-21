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
    "Atlanta Hawks": { "colour": "#FF6161" },
    "Boston Celtics": { "colour": "#a7e7b1" },
    "Brooklyn Nets": { "colour": "#C9C9C9" },
    "Charlotte Hornets": { "colour": "#8ea2fd" },
    "Chicago Bulls": { "colour": "#FF6161" },
    "Cleveland Cavaliers": { "colour": "#8ea2fd" },
    "Dallas Mavericks": { "colour": "#8ea2fd" },
    "Denver Nuggets": { "colour": "#8EC7FD" },
    "Detroit Pistons": { "colour": "#FF6161" },
    "Golden State Warriors": { "colour": "#FFF88F" },
    "Houston Rockets": { "colour": "#FF6161" },
    "Indiana Pacers": { "colour": "#8ea2fd" },
    "LA Clippers": { "colour": "#FF6161" },
    "Los Angeles Lakers": { "colour": "#bd8fff" },
    "Memphis Grizzlies": { "colour": "#8ea2fd" },
    "Miami Heat": { "colour": "#FF6161" },
    "Milwaukee Bucks": { "colour": "#a7e7b1" },
    "Minnesota Timberwolves": { "colour": "#8ea2fd" },
    "New Orleans Pelicans": { "colour": "#8ea2fd" },
    "New York Knicks": { "colour": "#ffb28f" },
    "Oklahoma City Thunder": { "colour": "#8ea2fd" },
    "Orlando Magic": { "colour": "#8ea2fd" },
    "Philadelphia 76ers": { "colour": "#FF6161" },
    "Phoenix Suns": { "colour": "#bd8fff" },
    "Portland Trail Blazers": { "colour": "#FF6161" },
    "Sacramento Kings": { "colour": "#bd8fff" },
    "San Antonio Spurs": { "colour": "#C9C9C9" },
    "Toronto Raptors": { "colour": "#FF6161" },
    "Utah Jazz": { "colour": "#8ea2fd" },
    "Washington Wizards": { "colour": "#8ea2fd" }
  },

  "mlb": {
    "Arizona Diamondbacks": { "colour": "#FF6161" },
    "Atlanta Braves": { "colour": "#8ea2fd" },
    "Baltimore Orioles": { "colour": "#ffb28f" },
    "Boston Red Sox": { "colour": "#FF6161" },
    "Chicago Cubs": { "colour": "#8EC7FD" },
    "Chicago White Sox": { "colour": "#C9C9C9" },
    "Cincinnati Reds": { "colour": "#FF6161" },
    "Cleveland Guardians": { "colour": "#8ea2fd" },
    "Colorado Rockies": { "colour": "#bd8fff" },
    "Detroit Tigers": { "colour": "#8ea2fd" },
    "Houston Astros": { "colour": "#8ea2fd" },
    "Kansas City Royals": { "colour": "#8EC7FD" },
    "Los Angeles Angels": { "colour": "#FF6161" },
    "Los Angeles Dodgers": { "colour": "#8ea2fd" },
    "Miami Marlins": { "colour": "#8ea2fd" },
    "Milwaukee Brewers": { "colour": "#8ea2fd" },
    "Minnesota Twins": { "colour": "#8ea2fd" },
    "New York Mets": { "colour": "#8ea2fd" },
    "New York Yankees": { "colour": "#8ea2fd" },
    "Oakland Athletics": { "colour": "#a7e7b1" },
    "Philadelphia Phillies": { "colour": "#FF6161" },
    "Pittsburgh Pirates": { "colour": "#C9C9C9" },
    "San Diego Padres": { "colour": "#FFF88F" },
    "San Francisco Giants": { "colour": "#C9C9C9" },
    "Seattle Mariners": { "colour": "#8ea2fd" },
    "St. Louis Cardinals": { "colour": "#FF6161" },
    "Tampa Bay Rays": { "colour": "#8ea2fd" },
    "Texas Rangers": { "colour": "#8ea2fd" },
    "Toronto Blue Jays": { "colour": "#8ea2fd" },
    "Washington Nationals": { "colour": "#FF6161" }
  },

  "nhl": {
    "Anaheim Ducks": { "colour": "#ffb28f" },
    "Utah Mammoth": { "colour": "#8ea2fd" },
    "Boston Bruins": { "colour": "#FFF88F" },
    "Buffalo Sabres": { "colour": "#8ea2fd" },
    "Calgary Flames": { "colour": "#FF6161" },
    "Carolina Hurricanes": { "colour": "#FF6161" },
    "Chicago Blackhawks": { "colour": "#FF6161" },
    "Colorado Avalanche": { "colour": "#bd8fff" },
    "Columbus Blue Jackets": { "colour": "#8ea2fd" },
    "Dallas Stars": { "colour": "#a7e7b1" },
    "Detroit Red Wings": { "colour": "#FF6161" },
    "Edmonton Oilers": { "colour": "#ffb28f" },
    "Florida Panthers": { "colour": "#FF6161" },
    "Los Angeles Kings": { "colour": "#C9C9C9" },
    "Minnesota Wild": { "colour": "#a7e7b1" },
    "Montreal Canadiens": { "colour": "#FF6161" },
    "Nashville Predators": { "colour": "#FFF88F" },
    "New Jersey Devils": { "colour": "#FF6161" },
    "New York Islanders": { "colour": "#ffb28f" },
    "New York Rangers": { "colour": "#8ea2fd" },
    "Ottawa Senators": { "colour": "#FF6161" },
    "Philadelphia Flyers": { "colour": "#ffb28f" },
    "Pittsburgh Penguins": { "colour": "#FFF88F" },
    "San Jose Sharks": { "colour": "#8ea2fd" },
    "Seattle Kraken": { "colour": "#8ea2fd" },
    "St. Louis Blues": { "colour": "#8ea2fd" },
    "Tampa Bay Lightning": { "colour": "#8ea2fd" },
    "Toronto Maple Leafs": { "colour": "#8ea2fd" },
    "Vancouver Canucks": { "colour": "#8ea2fd" },
    "Vegas Golden Knights": { "colour": "#C9C9C9" },
    "Washington Capitals": { "colour": "#FF6161" },
    "Winnipeg Jets": { "colour": "#8ea2fd" }
  }
}

if args.sport == "NHLhockey":
    sport = "hockey"
    league = "nhl"
    sport_color="rgb(189, 143, 255)"
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
    sport_color = "rgb(255, 178, 143)"
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
    html_content+=  f"<h4 style='text-align:center; width: 100%; margin-top: 56%; left: 50%; transform: translateX(-50%); position:fixed; bottom:0; font-weight: 400; font-size: 3vh; color:white; margin: 5px;'>QuantusSports.vercel.app/{args.sport}</h4>"

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

    posttext = f"{league.upper()} PowerRankings presented by Quantus{sport.capitalize()}\n\nQuantusSports.vercel.app/{args.sport}/powerrankings"

    facets = [
        {
            "index": {
                "byteStart": posttext.find(f"QuantusSports.vercel.app/{args.sport}/powerrankings"),
                "byteEnd": posttext.find(f"QuantusSports.vercel.app/{args.sport}/powerrankings") + len(f"QuantusSports.vercel.app/{args.sport}/powerrankings")
            },
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": "https://QuantusSports.vercel.app/{args.sport}/powerrankings"}]
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