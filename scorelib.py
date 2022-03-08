import json, os

def get_highscore(level):
    """ Returns (Dictionary) all highscores and usernames in resources/score.json of a certend level

        Args:
            level: string 'level'/'level1'/'level2'/'level3'    - filtervalue for the json syntax
    """
    # Filehandle read
    with open(os.path.join('resources', 'score.json'), 'r') as json_file:
        data = json.load(json_file)

    dict_score = {}

    for name in data:                               # Iterates through usernames
        values = data.get(name)                     # All key-value-pairs of json level
        for key in values.items():                  # Iterates through level pairs
            if key[0] == level and key[1] > 0:
                dict_score[name] = key[1]
    
    return {k: v for k, v in sorted(dict_score.items(), key=lambda item: item[1], reverse=True)}

def get_score(player):
    """ Returns (Dictionary) all Scors on every level of the player

        Args:
            player: string  - name of the player, reference for the .json
    """
    # Filehandle read
    with open(os.path.join('resources', 'score.json'), 'r') as json_file:
        data = json.load(json_file)

    if data.get(player) != None:                                        # Check if player exists, if not return a empty one
        return data.get(player)
    else:
        return {'level': 0, 'level1': 0, 'level2': 0, 'level3': 0}

def set_score(player, level, score):
    """ 
    """
    # Filehandle read
    with open(os.path.join('resources', 'score.json'), 'r') as json_file:
        data = json.load(json_file)

    if data.get(player) != None:                                                # Check if player exists, if not create a new one
        if data[player][level] < score:
            data[player][level] = score
    else:
        data[player] = {"level": 0, "level1": 0, "level2": 0, "level3": 0}
        data[player][level] = score

    # Filehandle write
    with open(os.path.join('resources', 'score.json'), 'w') as outfile:
        outfile.write(json.dumps(data))