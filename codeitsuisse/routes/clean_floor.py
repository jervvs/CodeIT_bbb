import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def clean(arr):
    curr_index = 0
    moves = 0
    total = sum(arr)

    while total > 0:
        left = (curr_index == len(arr)-1) or (curr_index>0) and arr[curr_index-1]>0

        # take the step
        if left:
            curr_index -= 1
        else:
            curr_index += 1

        if arr[curr_index]>0:
            arr[curr_index] -= 1
            total -= 1
        else:
            arr[curr_index] += 1
            total += 1
        moves += 1
    return moves

@app.route('/clean_floor', methods=['POST'])
def clean_floor():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    res = {'answers': {

                    }
            }

    inputValue = data.get("tests");
    for key, value in inputValue.items():
        val = clean(value['floor'])
        res['answers'][key] = val

    logging.info("My result :{}".format(res))
    return json.dumps(res);



