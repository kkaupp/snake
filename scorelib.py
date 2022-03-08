import json, os



def get_highscore(level):
    #filehandle
    with open(os.path.join('resources', 'score.json'), 'r') as json_file:
        data = json.load(json_file)

    dict_score = {}

    for name in data:
        values = data.get(name)
        for key in values.items():
            if key[0] == level:
                dict_score[name] = key[1]
    
    return {k: v for k, v in sorted(dict_score.items(), key=lambda item: item[1], reverse=True)}

def get_score(player):
    # Filehandle
    with open(os.path.join('resources', 'score.json'), 'r') as json_file:
        data = json.load(json_file)

    return data.get(player)

def set_score(player, level, score):
    # Filehandle
    with open(os.path.join('resources', 'score.json'), 'r') as json_file:
        data = json.load(json_file)

    if data.get(player) != None:
        if data[player][level] > score:
            data[player][level] = score
    else:
        data[player] = {"level": 0, "level1": 0, "level2": 0, "level3": 0}
        data[player][level] = score

    with open(os.path.join('resources', 'score.json'), 'w') as outfile:
        outfile.write(json.dumps(data))

#print(get_highscore('level1'))
#print(get_score('player1'))
#print(set_score('player1', 'level1', 23))