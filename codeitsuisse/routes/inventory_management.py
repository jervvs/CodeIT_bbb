import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def editDistDP(s1, s2): 
    len1 = len(s1) 
    len2 = len(s2)
    dp = [[0 for i in range(len2 + 1)] 
             for j in range(len1 + 1)] 

    for i in range(len1 + 1): 
        dp[i][0] = i 
    for j in range(len2 + 1): 
        dp[0][j] = j 
    for i in range(1, len1 + 1): 
        for j in range(1, len2 + 1): 
            if s2[j - 1] == s1[i - 1]: 
                dp[i][j] = dp[i - 1][j - 1] 
            else: 
                dp[i][j] = 1 + min(dp[i][j - 1], 
                                   dp[i - 1][j - 1], 
                                   dp[i - 1][j])
    num_changes = dp[len1][len2]
    return (dp, num_changes)

def get_changes(s1, s2, dp):
    new_str = ''
    i = len(s1)
    j = len(s2)
    while(i>=0 and j>=0):
        if s1[i-1] == s2[j-1]:
            new_str = s1[i-1] + new_str
            i-=1
            j-=1
        elif dp[i][j] == dp[i-1][j-1] + 1:
            # replace
            new_str = s2[j-1] + new_str
            i-=1
            j-=1
            pass
        elif dp[i][j] == dp[i-1][j] + 1:
            # delete
            new_str = "-" + s1[i-1] + new_str
            i-=1
            pass
        elif dp[i][j] == dp[i][j-1] + 1:
            # add
            new_str = "+" + s2[j-1] + new_str
            j-=1
    return new_str

def find_similarity(search_item_name, item):
    dp, num_changes = editDistDP(search_item_name, item)
    new_str = get_changes(search_item_name, item, dp)
    return (num_changes, new_str[1:])

def manage_inventory(my_dict):
    search_item_name = my_dict["searchItemName"]
    items = my_dict["items"]

    my_list = []
    for item in items:
        num_changes, new_str = find_similarity(search_item_name, item)
        my_list.append((num_changes, new_str))

    my_list.sort(key=lambda x: x[0])
    results = []
    for item in my_list:
        results.append(item[1])
    return results

@app.route('/inventory-management', methods=["POST"])
def inventory_management():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    results = []
    for entry in data:
        results.append({
            "searchItemName": entry["searchItemName"],
            "searchResult": manage_inventory(entry["searchResult"])
        })

    logging.info("My result :{}".format(results))
    return jsonify(results);