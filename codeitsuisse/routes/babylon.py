import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateBooks():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    numberOfBooks = data.get("numberOfBooks");
    numberOfDays = data.get("numberOfDays");
    books = data.get("books");
    days = data.get("days");


    result = get_books(books, days, 0, 0, numberOfBooks)
    logging.info("My result :{}".format(result))
    return json.dumps(result);

def get_books(books, days, book_index, books_read, book_length):
    if book_index == book_length:
        return books_read
    book = books[book_index]

    res = books_read
    can_add = False

    for i in range(len(days)):
        if book <= days[i]:
            days[i] -= book # assume the book gets included in the day
            res_chosen = get_books(books, days, book_index+1, books_read+1, book_length) # recurse with the above assumption
            res = max(res, res_chosen)
            days[i] += book # book not read on that day
            can_add = True

    if not can_add: # can still take in at least 1 book
        return res

    res_not_chosen = get_books(books, days, book_index+1, books_read, book_length)
    res = max(res, res_not_chosen)
    return res

# numberOfBooks= 5
# numberOfDays= 3
# books= [114, 111, 41, 62, 64]
# days= [157, 136, 130]
# print(get_books(books, days, 0, 0, numberOfBooks))





