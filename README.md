# Quantus Sports Scripts
The scripts in this repository serve are the main data fetching scripts for [Quantus Sports](https://github.com/jmi06/Quantus-Sports). The *core* directory is for the core leagues, team based sports leagues that utilize the ESPN hidden API. As more leagues or sports are added, new scripts may be created to satisfy certain needs.

### Scripts
- socialposts (Used to build graphics for the BlueSky account, separate from post game updates)
    - current_rankings.py 
    - power_rankings.py
    - predictions.py

- main.py (Fetches data, creates graphics for post game updates)
- csvgen.py (Generates CSV files of team's ratings over time)
- update_all_games.py (Used if something is out of date, fetches every game of the season)
