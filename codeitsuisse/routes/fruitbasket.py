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
    logging.info("data sent for evaluation {}".format(data))

    appleAmount = data.get("maApple")
    watermelonAmount = data.get("maWatermelon")
    bananaAmount = data.get("maBanana")

    appleWeight = 75
    watermelonWeight = 50
    bananaWeight = 50

    result = appleAmount * appleWeight + watermelonAmount * watermelonWeight + bananaAmount * bananaWeight

    logging.info("My result :{}".format(result))
    return json.dumps(result)