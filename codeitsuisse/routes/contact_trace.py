import logging
import json
from collections import Counter

from flask import request, jsonify;
from collections import defaultdict
from copy import copy

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def count_differences(genome1, genome2):
    instructions1 = genome1.split('-')
    instructions2 = genome2.split('-')
    n = len(instructions1)
    diff = 0
    nonsilent = 0
    for i in range(n):
        if instructions1[i][0] != instructions2[i][0]:
            nonsilent += 1
            diff +=1
        for j in range(1,3):
            if instructions1[i][j] != instructions2[i][j]:
                diff += 1
    return (diff, nonsilent > 1)

def recurseToOrigin(finished, origin, current, cluster, tracemap, path, visited):
    if finished:
        path.append(current)
        return path

    path.append(current)
    o_diff = count_differences(tracemap[current[0]], tracemap[origin])
    min_diff = -1
    c_list = []

    for c in cluster:
        if visited[c] == 0:
            diff = count_differences(tracemap[current[0]], tracemap[c])
            if min_diff == -1 or min_diff>diff[0]:
                min_diff = diff[0]
                c_list = [[c, diff[1]]]
            elif min_diff == diff[0]:
                c_list.append([c, diff[1]])
    result = []

    if min_diff == o_diff[0] or min_diff == -1:
        result += recurseToOrigin(True, origin, [origin, o_diff[1]], cluster, tracemap, path[:], visited)
        for i in c_list:
            if visited[i[0]] == 0:
                visited_copy = copy(visited)
                visited_copy[i[0]] = 1
                result += recurseToOrigin(True, origin, i, cluster, tracemap, path[:], visited_copy)
    else:
        for i in c_list:
            if visited[i[0]] == 0:
                visited_copy = copy(visited)
                visited_copy[i[0]] = 1
                result += recurseToOrigin(False, origin,i, cluster, tracemap, path[:], visited_copy)
    return result

@app.route('/contact_trace', methods=['POST'])
def contact_trace():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    tracemap = {}
    cluster = []
    visited = defaultdict(int)

    infected_name = data['infected']['name']
    infected_genome = data['infected']['genome']
    origin_name = data['origin']['name']
    origin_genome = data['origin']['genome']

    tracemap[infected_name] = infected_genome
    tracemap[origin_name] = origin_genome

    for strand in data['cluster']:
        cluster.append(strand['name'])
        tracemap[strand['name']] = strand['genome']
    
    result = recurseToOrigin(False, origin_name, infected_name, cluster, tracemap, [], visited)
    count = 0
    path = []
    path_str = infected_name
    for i in result:
        if i[0] == infected_name and count > 0:
            count += 1
            path.append(path_str)
            path_str = infected_name
        elif i[0] == infected_name and count == 0:
            count += 1
        else:
            if i[1]:
                path_str+="*"
            path_str += ' -> '
            path_str += i[0]
    path.append(path_str)
    logging.info("My result :{}".format(path))
    return json.dumps(path)


