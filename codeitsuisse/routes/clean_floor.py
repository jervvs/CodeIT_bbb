import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def clean(arr):
    total = sum(arr)
    res = 1

    index = 1
    prev_one = 0 if arr[0] == 1 else -1

    while total != 0 and index < len(arr):
        if arr[index] == 1:
            arr[index] = 0
            if index != 1:
                res += 1
            total -= 1
            index += 1
        else:
            if prev_one >= 0:
                arr[index] = 1
                total += 1
                if index != 1:
                    res += 1
                for i in range(prev_one, index):
                    arr[i] = 0
                    res += 2

                arr[index] = 0
                index += 1
                prev_one = -1
            else:
                arr[index] = 1
                total += 1
                if index != 1:
                    res += 1
                prev_one = index
                index += 1

    if prev_one != -1:
        for i in range(prev_one, index-1):
            arr[i] = 0
            res += 1
    return res

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
        res['answers']['key'] = val

    logging.info("My result :{}".format(res))
    return json.dumps(res);



