import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def editDistDP(s1, s2): 
    len1 = len(s1) 
    len2 = len(s2) 
    if len1*len2 == 0:
        return len1+len2
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
    res, count = get_changes(s1, s2, dp)
    return (res, count, s2)

def get_changes(s1, s2, dp):
    count = 0
    s1 = list(s1)
    i = len(s1)
    j = len(s2)
    while(i>0 or j>0):
        if i==0 or j==0:
            if i == 0:
                count += 1
                s1.insert(i, '+' + s2[j-1])
                j-=1
            else:
                count += 1
                s1.insert(i-1, '-')
                i-=1
            continue

        if s1[i-1] == s2[j-1]:
            i-=1
            j-=1
        elif dp[i][j] == dp[i-1][j-1] + 1:
            # replace
            count += 1
            s1[i-1] = s2[j-1]
            i-=1
            j-=1
        elif dp[i][j] == dp[i-1][j] + 1:
            # delete
            count += 1
            s1.insert(i-1, '-')
            i-=1
        elif dp[i][j] == dp[i][j-1] + 1:
            # add
            count += 1
            s1.insert(i, '+' + s2[j-1])
            j-=1
    s1 = ''.join(s1)
    return (s1, count)


@app.route('/inventory-management', methods=["POST"])
def inventory_management():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    result = []
    for entry in data:
        entry_name = entry['searchItemName']
        products = entry["items"]
        
        mid_results = []
        for product in products:
            mid_results.append(editDistDP(entry_name, product))
        mid_results.sort(key = lambda x: (x[1],x[2]))
        final_results = []
        for i in range(min(len(mid_results), 10)):
            final_results.append(mid_results[i][0])
        
        answer = {
            "searchItemName": entry_name,
            "searchResult": final_results
        }

        result.append(answer)

    logging.info("My result :{}".format(result))
    return jsonify(result);
