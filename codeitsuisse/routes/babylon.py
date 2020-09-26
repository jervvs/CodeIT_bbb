import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

import pip

logger = logging.getLogger(__name__)

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

install('mknapsack')
from mknapsack.algorithms import mtm

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateOptimalBooks():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    numberOfBooks = data.get("numberOfBooks");
    numberOfDays = data.get("numberOfDays");
    books = data.get("books");
    days = data.get("days");

    result, x, bt, glopt = mtm([1]*numberOfBooks, books, days)
    # result = get_books(books, days, 0, 0, numberOfBooks)
    logging.info("My result :{}".format(result))
    return json.dumps(result);




