def socialPostHTML(id):
    postInfo = {}
    with open(f'{args.sport}/post.json') as postFile:
        postInfo = json.load(postFile)

    if games[id]['team_1']['winner'] == True:

        postInfo['winning_team'] = games[id]['team_1']['team_name']
        postInfo['losing_team'] = games[id]['team_2']['team_name']

    elif games[id]['team_2']['winner'] == True:

        postInfo['winning_team'] = games[id]['team_2']['team_name']
        postInfo['losing_team'] = games[id]['team_1']['team_name']

