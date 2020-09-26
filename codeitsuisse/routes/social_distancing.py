import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def find_perms(seats, people, space):
    min_seats = people*(space+1) - space
    extra_seats = seats - min_seats
    return perm(people, extra_seats)

def perm(people, extra_seats):
    i = max(people, extra_seats)
    res = 1

    for val in range(i+1, people+extra_seats+1):
        res *= val
        res /= val - i
    return int(res)

# print(find_perms(8, 3, 1))
# print(find_perms(7, 3, 1))
# print(find_perms(6, 2, 2))

@app.route('/social_distancing', methods=['POST'])
def evaluateSocialDistance():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    res = {'answers': {

                    }
            }

    inputValue = data.get("tests");
    for key, value in inputValue.items():
        val = find_perms(value['seats'], value['people'], value['spaces'])
        res['answers'][key] = val

    logging.info("My result :{}".format(res))
    return json.dumps(res);






