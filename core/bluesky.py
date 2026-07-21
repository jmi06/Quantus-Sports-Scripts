import requests
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import time

def create_post(sport):

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

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    postNow = datetime.now()
    formatted_time = postNow.strftime("%I:%M %p")

    resp = requests.post(

        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_PASSWORD},

    )

    session = resp.json()

    with open(f'{sport}/post.png', "rb") as f:
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

    posttext = f"{config[sport]['platform']} Update as of {formatted_time}: \n{postinfo['winning_team']} beat {postinfo['losing_team']} {postinfo['score']} \nSee more at https://QuantusSports.vercel.app/ \n{config[sport]['tag']}"

    facets = [
        {
            "index": {
                "byteStart": posttext.find("https://QuantusSports.vercel.app/"),
                "byteEnd": posttext.find("https://QuantusSports.vercel.app/") + len("https://QuantusSports.vercel.app/")
            },
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": "https://QuantusSports.vercel.app/"}]
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