# import logging
# import json

# from flask import request, jsonify;

# from codeitsuisse import app;

# logger = logging.getLogger(__name__)

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
        result += 50 * data[item]

    logging.info("My result :{}".format(result))
    result = "{}".format(result)
    return result