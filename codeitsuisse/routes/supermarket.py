import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/supermarket', methods=['POST'])
def evaluatePath():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    entries = data.get("tests");

    result = {
        'answers':{

        }
    }

    for key in entries.keys():
        _id = key
        result['answers'][_id] = shortest_path(entries[key]["maze"], entries[key]["start"], entries[key]["end"])

    logging.info("My result :{}".format(result))
    return json.dumps(result);

    
def shortest_path(maze, startingCoords, endingCoords):
    rows = len(maze)
    cols = len(maze[0])

    if rows == 0 or cols == 0:
        return 0

    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = []
    min_dist = rows*cols+1

    visited[startingCoords[0]][startingCoords[1]] = True
    queue.append((startingCoords[0], startingCoords[1], 0))

    while len(queue) != 0:
        currPos = queue.pop(0)
        i = currPos[0]
        j = currPos[1]
        dist = currPos[2]

        #check if we're at the end
        if i == endingCoords[0] and j == endingCoords[1]:
            min_dist = dist
            break

        #else we check if the rest are valid and put them in the queue
        #right
        if valid(maze, visited, i, j+1):
            visited[i][j+1] = True
            queue.append((i, j+1, dist+1))
        #left
        elif valid(maze, visited, i, j-1):
            visited[i][j-1] = True
            queue.append((i, j-1, dist+1))
        #up
        elif valid(maze, visited, i-1, j):
            visited[i-1][j] = True
            queue.append((i-1, j, dist+1))
        #down
        elif valid(maze, visited, i+1, j):
            visited[i+1][j] = True
            queue.append((i+1, j, dist+1))

    #if breakout of loop, could be because all not valid or a path was found
    if min_dist == rows*cols+1:
        return 0
    else:
        return min_dist


def valid(maze, visited, i, j):
    #valid if within the maze and not visited
    rows = len(maze)
    cols = len(maze[0])

    return i >= 0 and i < rows and j >= 0 and j < cols and visited[i][j] == False

    


