import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluateSalad():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    n = data.get('number_of_salads')
    arr = data.get("salad_prices_street_map")

    res = 10 ** 9 + 7
    rows = len(arr)
    cols = len(arr[0])
    for i in range(rows):
        tmp = arr[i]
        tmp = [int(i) if i != 'X' else 0 for i in tmp]
        for j in range(cols - n + 1):
            if 0 not in tmp[j:j + n]:
                res = min(res, sum(tmp[j:j + n]))

    if res == 10 ** 9 + 7:
        res = 0

    result = {'result': res}
    logging.info("My result :{}".format(result))
    return json.dumps(result);


