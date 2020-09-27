import logging
import json
import numpy as np
from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/supermarket', methods=['POST'])
def supermarket():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    entries = data.get("tests");

    result = {
        'answers':{

        }
    }

    for key in entries.keys():
        _id = key
        result['answers'][_id] = search(entries[key]["maze"], entries[key]["start"], entries[key]["end"])

    logging.info("My result :{}".format(result))
    return json.dumps(result);


def check_surroundings(current_node, arr):
    surrounding_nodes = []
    x,y = current_node
    if x>0 and arr[y][x-1] == float('inf'):
        surrounding_nodes.append((x-1,y))

    if y<len(arr)-1 and arr[y+1][x] == float('inf'):   #Bottom Node
        surrounding_nodes.append((x, y+1))

    if x<len(arr[0])-1 and arr[y][x+1] == float('inf'):   #Right Node
        surrounding_nodes.append((x+1, y))

    if y>0 and arr[y-1][x] == float('inf'):        #Top Node
        surrounding_nodes.append((x, y-1))

    return surrounding_nodes

def search(grid, start, end):
    arr = grid.copy()
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == 1:
                arr[i][j] = None
            else:
                arr[i][j] = float('inf')
    
    arr[start[1]][start[0]] = 0

    current_node = start
    forefront_nodes = []

    while current_node != end:
        current_x, current_y = current_node
        current_value = arr[current_y][current_x]

        surrounding_nodes = check_surroundings(current_node, arr)

        for node in surrounding_nodes:
            x,y = node
            arr[y][x] = current_value + 1
            forefront_nodes.append((x,y,arr[y][x]))
        
        if forefront_nodes == []:
            return -1

        forefront_nodes.sort(key=lambda x: x[2])
        min_node = forefront_nodes.pop(0)
        current_node = [min_node[0], min_node[1]]
    
    return (arr[end[1]][end[0]] + 1)