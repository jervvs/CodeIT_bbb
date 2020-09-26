import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def get_line(x1,x2,y1,y2):
    m = (y1 - y2) / (x1 - x2)
    c = y1 - m * x1
    return (m,c)

def check_valid(min_maxes, x_, y_):
    min_x1, max_x1, min_y1, max_y1 = min_maxes
    if min_x1 <= x_ <= max_x1 and min_y1 <= y_ <= max_y1:
        return True
    else:
        return False


def line_intersection(line1, line2): # line1 = ([x1,y1], [x2,y2]), line2 = ([x3,y3], [x4,y4])
    x1,y1 = line1[0]
    x2,y2 = line1[1]
    x3,y3 = line2[0]
    x4,y4 = line2[1]
    min_maxes = [min(x1,x2), max(x1,x2), min(y1,y2), max(y1,y2)]
    # Both vertical lines
    if x1 == x2 and x3 == x4:
        return None
    # Line 1 is vertical
    elif x1 == x2:
        m2, c2 = get_line(x3,x4,y3,y4)
        y_ = m2 * x1 + c2
        # intersection = (x1, y_)
        if check_valid(min_maxes, x1, y_):
            return [x1,y_]
        else:
            return None
    # Line 2 is vertical
    elif x3 == x4:
        m1, c1 = get_line(x1,x2,y1,y2)
        y_ = m1 * x3 + c1
        # intersection = (x3, y_)
        if check_valid(min_maxes, x3, y_):
            return [x3,y_]
        else:
            return None
    # No vertical lines
    else:
        m1, c1 = get_line(x1,x2,y1,y2)
        m2, c2 = get_line(x3,x4,y3,y4)

        if m1 == m2:
            return None
        x_ = (c2 - c1) / (m1 - m2)
        y1 = m1 * x_ + c1
        y2 = m2 * x_ + c2

        if check_valid(min_maxes, x_, y1):
            return [x_, y1]
        else:
            return None


@app.route('/revisitgeometry', methods=['POST'])
def evaluate():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    shapeCoordinates = data.get("shapeCoordinates")
    lineCoordinates = data.get("lineCoordinates")

    n = len(shapeCoordinates)

    res = []
    for i in range(n):
        second_index = (i+1)%n
        line1 = [[shapeCoordinates[i]['x'], shapeCoordinates[i]['y']], [shapeCoordinates[second_index]['x'], shapeCoordinates[second_index]['y']]]
        line2 = [[lineCoordinates[0]['x'], lineCoordinates[0]['y']], [lineCoordinates[1]['x'], lineCoordinates[1]['y']]]
        intersection = line_intersection(line1, line2)
        if intersection != None:
            res.append({"x": intersection[0], "y": intersection[1]})


    logging.info("My result :{}".format(res))
    return json.dumps(res);



