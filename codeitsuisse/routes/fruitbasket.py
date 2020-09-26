import logging
import json
import numpy as np
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    data = request.get_data()
    data = json.loads(data)
    logging.info("data sent for evaluation {}".format(data))

    result = 0
    for item in data.keys():
        estimate += np.random.randint(1,100) * data[item]

    result = int(result)
    logging.info("My result :{}".format(result))
    result = "{}".format(result)
    return result