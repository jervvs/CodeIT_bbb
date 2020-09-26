import logging
import json
import numpy as np
from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateBabylon():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    numberOfBooks = data.get("numberOfBooks");
    numberOfDays = data.get("numberOfDays");
    books = data.get("books");
    days = data.get("days");

    dp = np.full([numberOfBooks] + [i + 1 for i in days], -1)
    result = maxWeight(days, books, numberOfBooks)

    # result = get_books(books, days, 0, 0, numberOfBooks)
    logging.info("My result :{}".format(result))
    return json.dumps(result);

# def get_books(books, days, book_index, books_read, book_length):
#     if book_index == book_length:
#         return books_read
#     book = books[book_index]
#
#     res = books_read
#     can_add = False
#
#     for i in range(len(days)):
#         if book <= days[i]:
#             days[i] -= book # assume the book gets included in the day
#             res_chosen = get_books(books, days, book_index+1, books_read+1, book_length) # recurse with the above assumption
#             res = max(res, res_chosen)
#             days[i] += book # book not read on that day
#             can_add = True
#
#     if not can_add: # can still take in at least 1 book
#         return res
#
#     res_not_chosen = get_books(books, days, book_index+1, books_read, book_length)
#     res = max(res, res_not_chosen)
#     return res

def maxWeight(days, arr, n, i=0):
    """
    :param n: number of books
    :param w1_r: capacity of bag1
    :param w2_r: capacity of bag2
    :param i: index of the book we are working on
    :return:
    """
    # Base case
    if i == n:
        return 0
    if eval('dp' + str([i]+days)) != -1:
        return eval('dp' + str([i]+days))

    # Variables to store the result of numberOfDays+1 parts of recurrence relation
    fill_none = 0
    fill = [0]
    for index, d in enumerate(days):
        if d >= arr[i]:
            days[index] -= arr[i]
            fill.append(1 + maxWeight(days, arr, n, i+1))
            days[index] += arr[i]

    fill_none = (1 + maxWeight(days, arr, n, i+1))
    exec('dp' + str([i]+days) + '=' + str(max(fill_none, max(fill))))

    return eval('dp' + str([i]+days))

# import numpy as np
# numberOfBooks= 5
# numberOfDays= 3
# books= [114, 111, 41, 62, 64]
# days= [157, 136, 130]
# dp = np.full([numberOfBooks] + [i+1 for i in days], -1)
# print(maxWeight(days, books, numberOfBooks))
# print(get_books(books, days, 0, 0, numberOfBooks))





