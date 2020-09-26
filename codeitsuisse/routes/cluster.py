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
                    r_ = new_person[0] + direction[0]
                    c_ = new_person[1] + direction[1]

                    if r_>=0 and r_<rows and c_>=0 and c_<cols:
                        if str([r_,c_]) not in visited and arr[r_][c_] != '*':
                            new_infected.append([r_,c_])
                            visited[str([r_,c_])] = 1
    return res

# print(clusters(  [
#     ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
#     ["*", "0", "0", "0", "*", "*", "*", "*", "*"],
#     ["*", "*", "1", "*", "*", "*", "*", "*", "*"],
#     ["*", "0", "0", "0", "*", "*", "*", "*", "*"],
#     ["*", "*", "*", "*", "0", "*", "*", "*", "*"],
#     ["*", "*", "*", "*", "*", "0", "0", "*", "*"],
#     ["*", "*", "*", "*", "1", "*", "*", "*", "0"],
#     ["*", "*", "*", "*", "0", "*", "*", "0", "0"],
#     ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
#     ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
#     ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
#     ["*", "*", "1", "0", "0", "*", "*", "*", "*"],
#     ["*", "*", "*", "*", "*", "*", "*", "*", "*"]
#   ]))

@app.route('/cluster', methods=['POST'])
def evaluate():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    arr = data
    result = {'answer': clusters(arr)}

    logging.info("My result :{}".format(result))
    return json.dumps(result);






