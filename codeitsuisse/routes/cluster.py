import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def clusters(arr):
    rows = len(arr)
    cols = len(arr[0])
    res = 0

    directions = [[-1,0], [-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1]]
    infected = [[r, c] for r in range(rows) for c in range(cols) if arr[r][c]=="1"]
    visited = {}

    for i in infected:
        if str(i) not in visited:
            visited[str(i)] = 1
            res += 1

            new_infected = [i]
            while len(new_infected) != 0:
                new_person = new_infected.pop(0)
                for direction in directions:
                    x = new_person[0] + direction[0]
                    y = new_person[1] + direction[1]

                    if x>=0 and x<cols and y>=0 and y<rows:
                        if str([x,y]) not in visited and arr[x][y] != '*':
                            new_infected.append([x,y])
                            visited[str([x,y])] = 1
    return res

@app.route('/cluster', methods=['POST'])
def evaluateCluster():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    arr = data
    result = {'result': clusters(arr)}

    logging.info("My result :{}".format(result))
    return json.dumps(result);






