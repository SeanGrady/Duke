from gen_board import setupBags
from collections import defaultdict
import yaml
from yaml.representer import Representer
yaml.add_representer(defaultdict, Representer.represent_dict)

def printYaml(bag):
    move_names = yaml.load(open('move_types.yml'))
    sides = {0:'front', 1:'back'}
    pieces = {
        piece.name: {
            sides[index]: buildMoveDict(side, move_names) for index, side in enumerate(piece.actions)
        } for piece in bag
    }
    stream = file('yamlpieces.yaml', 'w')
    yaml.dump(pieces, stream)

def buildMoveDict(action_list, move_names):
    move_dict = defaultdict(list)

    for action in action_list:
        move_name = move_names[action[0]]
        if len(action) > 2:
            move_dict[move_name].append(
                {
                    'x': action[1],
                    'y': action[2],
                }
            )
        else:
            move_dict['special'] = move_name

    return move_dict

white_bag, black_bag, names = setupBags()
printYaml(white_bag)
