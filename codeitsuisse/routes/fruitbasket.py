import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    data = request.get_data()
    data = json.loads(data)
    logging.info("data sent for evaluation {}".format(data))

    total = 0
    for item in data.keys():
        total += np.random.randint(1,100) * data[item]

    logging.info("My result :{}".format(total))
    result = "{}".format(total)
    return result