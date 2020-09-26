# @app.route('/fruitbasket', methods=['POST'])
# def evaluateFruit():
    # data = request.get_data()
    # data = json.loads(data)
    # logging.info("data sent for evaluation {}".format(data))

    # appleAmount = data["maApple"]
    # watermelonAmount = data["maWatermelon"]
    # bananaAmount = data["maBanana"]

    # appleWeight = 70
    # watermelonWeight = 55
    # bananaWeight = 50

    # result = appleAmount*appleWeight + watermelonAmount*watermelonWeight + bananaAmount*bananaWeight

    # return result

import logging
import json
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    data = request.get_data()
    data = json.loads(data)
    logging.info("data sent for evaluation {}".format(data))

    # estimate = 0
    # for item in data.keys():
    #     estimate += (50 * data[item])

    # estimate = int(math.ceil(estimate/100.0))*100
    # logging.info("My result :{}".format(estimate))
    # result = "{}".format()
    return 0