import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

# https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines/20679579
def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return None

@app.route('/revisitgeometry', methods=['POST'])
def evaluateIntersections():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    shapeCoordinates = data.get("shapeCoordinates")
    lineCoordinates = data.get("lineCoordinates")

    n = len(shapeCoordinates)
    l = len(lineCoordinates)

    res = []
    for i in range(n):
        second_index = (i+1)%n
        line1 = line([shapeCoordinates[i]['x'], shapeCoordinates[i]['y']], [shapeCoordinates[second_index]['x'], shapeCoordinates[second_index]['y']])
        line2 = line([lineCoordinates[0]['x'], lineCoordinates[0]['y']], [lineCoordinates[1]['x'], lineCoordinates[1]['y']])
        point = intersection(line1, line2)

        if point != None and max(shapeCoordinates[i]['x'], shapeCoordinates[second_index]['x']) <= point[0] and point[0] >= min(shapeCoordinates[i]['x'], shapeCoordinates[second_index]['x']) and \
            max(shapeCoordinates[i]['y'], shapeCoordinates[second_index]['y']) <= point[1] and point[1] >= min(shapeCoordinates[i]['y'], shapeCoordinates[second_index]['y']):
            res.append({"x": intersection[0], "y": intersection[1]})

    logging.info("My result :{}".format(res))
    return json.dumps(res);

# shapeCoordinates = [
#     { "x": 21, "y": 70 },
#     { "x": 72, "y": 70 },
#     { "x": 72, "y": 127 }
#   ]
# lineCoordinates = [
#     { "x": -58, "y": 56 },
#     { "x": -28, "y": 68 }
#   ]
#
# n = len(shapeCoordinates)
#
# res = []
# for i in range(n):
#     second_index = (i+1)%n
#     line1 = line([shapeCoordinates[i]['x'], shapeCoordinates[i]['y']], [shapeCoordinates[second_index]['x'], shapeCoordinates[second_index]['y']])
#     line2 = line([lineCoordinates[0]['x'], lineCoordinates[0]['y']], [lineCoordinates[1]['x'], lineCoordinates[1]['y']])
#     point = intersection(line1, line2)
#
#     if point != None and max(shapeCoordinates[i]['x'], shapeCoordinates[second_index]['x']) >= point[0] and point[0] >= min(shapeCoordinates[i]['x'], shapeCoordinates[second_index]['x']) and \
#         max(shapeCoordinates[i]['y'], shapeCoordinates[second_index]['y']) >= point[1] and point[1] >= min(shapeCoordinates[i]['y'], shapeCoordinates[second_index]['y']):
#         res.append({"x": point[0], "y": point[1]})
#
# print(res)


