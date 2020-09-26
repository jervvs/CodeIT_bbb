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

    result = 10^9 + 7
    rows = len(arr)
    cols = len(arr[0])
    for i in range(rows):
        tmp = arr[i]
        tmp.replace('X', '0')
        tmp = [int(i) for i in tmp]
        for j in range(cols-n+1):
            if 0 not in tmp[j:j+n]:
                result = min(result, sum(tmp[j+n]))

    if result != 10^9 + 7:
        result = 0

    logging.info("My result :{}".format(result))
    return json.dumps(result);



