import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    numberOfBooks = data.get("numberOfBooks");
    numberOfDays = data.get("numberOfDays");
    books = data.get("books");
    days = data.get("days");

    max_books = min(numberOfDays * 3, numberOfBooks)

    result = get_books(sorted(books)[0: max_books], days, 0, 0)
    logging.info("My result :{}".format(result))
    return json.dumps(result);


def get_books(books, days, book_index, books_read):
    try:
        book = books[book_index]
    except:
        return books_read # exceed every book

    res = books_read
    can_add = False

    for i in range(len(days)):
        if book <= days[i]:
            days[i] -= book # assume the book gets included in the day
            res_chosen = get_books(books, days, book_index+1, books_read+1) # recurse with the above assumption
            res = max(res, res_chosen)
            days[i] += book # book not read on that day
            can_add = True

    if not can_add: # can still take in at least 1 book
        return res

    res_not_chosen = get_books(books, days, book_index+1, books_read)
    res = max(res, res_not_chosen)
    return res





