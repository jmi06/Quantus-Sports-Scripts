# New leader (and if they won to overtake)
# Season high elo (team and league) - only after 2 weeks
# Season low elo (team and league) - only after 2 weeks
# Upset alert - only after 2 weeks
# Biggest swing
"""
Not yet in use.
"""
import argparse
import pandas as pd
import core.csvgen as csvgen
import datetime
import json

parser = argparse.ArgumentParser()
parser.add_argument("--sport")
args = parser.parse_args()
print(args.sport)

with open(f'{args.sport}/order.json', 'r') as file:
    orderFile = json.load(file)


def new_leader():
    csvgen.byDate(args.sport)


    df = pd.read_csv(f"{args.sport}/eloDate.csv")

    today = datetime.date.today()

    yesterday = today - datetime.timedelta(days=1)

    yesterday = datetime.date.isoformat(yesterday)

    print(yesterday)
    yesterday_df = df.sort_values(by=yesterday, ascending=False)

    today_df = df.sort_values(by=today.isoformat(), ascending=False)
    print(df[yesterday].sort_values(ascending=False))

    print(type(today_df.iloc[0,0]))




new_leader()



