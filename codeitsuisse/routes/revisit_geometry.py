import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

# https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines/20679579
def line_intersection(line1, line2): # line1 = ([x1,y1], [x2,y2]), line2 = ([x3,y3], [x4,y4])
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    if min(line1[0][0], line1[1][0]) <= x and x <= max(line1[0][0], line1[1][0]) and min(line1[0][1], line1[1][1]) <= y and y <= max(line1[0][1], line1[1][1]):
        return [x,y]
    else:
        return None

@app.route('/revisitgeometry', methods=['POST'])
def evaluateGeometry():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    shapeCoordinates = data.get("shapeCoordinates")
    lineCoordinates = data.get("lineCoordinates")

    n = len(shapeCoordinates)
    l = len(lineCoordinates)

    res = []
    for i in range(n):
        second_index = (i+1)%n
        line1 = [[shapeCoordinates[i]['x'], shapeCoordinates[i]['y']], [shapeCoordinates[second_index]['x'], shapeCoordinates[second_index]['y']]]
        if l == 2: # if only 2 point, no need to wrap around (last point, and 1st point)
            line2 = [[lineCoordinates[0]['x'], lineCoordinates[0]['y']],
                     [lineCoordinates[1]['x'], lineCoordinates[1]['y']]]
            intersection = line_intersection(line1, line2)
            if intersection != None:
                res.append({"x": intersection[0], "y": intersection[1]})
        else:
            for j in range(l):
                second_index = (j + 1) % l
                line2 = [[lineCoordinates[j]['x'], lineCoordinates[j]['y']],
                         [lineCoordinates[second_index]['x'], lineCoordinates[second_index]['y']]]


                if intersection != None:
                    res.append({"x":intersection[0], "y":intersection[1]})

    logging.info("My result :{}".format(res))
    return json.dumps(res);



