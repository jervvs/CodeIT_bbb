import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def get_good_genome(my_str):
    my_dict = {'A': 0, 'C': 0, 'G':0, 'T':0}
    for letter in my_str:
        my_dict[str(letter)] += 1

    num_ACGT = min(my_dict.values())
    num_CC = (my_dict["C"] - num_ACGT)//2

    if (my_dict["C"] - num_ACGT) % 2 == 1 and num_ACGT > 0: # Checks if we can get an extra CC instead
        num_ACGT -= 1
        num_CC += 1
    
    left = {}
    left["A"] = my_dict["A"] - num_ACGT
    left["C"] = my_dict["C"] - num_ACGT - num_CC
    left["G"] = my_dict["G"] - num_ACGT
    left["T"] = my_dict["T"] - num_ACGT

    result = ""

    for i in range(num_CC):
        if left["A"] >= 2:
            result += "AA"
            left["A"] -= 2
        result += "CC"
    for i in range(num_ACGT):
        if left["A"] >= 1:
            result += "A"
            left["A"] -= 1
        result += "ACGT"
    for letter in ["C", "G", "T"]:
        for i in range(left[letter]):
            if left["A"] >= 2:
                result += "AA"
                left["A"] -= 2
            result += letter
    result += "A"*left["A"]
    return result

@app.route('/intelligent-farming', methods=["POST"])
def get_gmo():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    entries = data.get("list");
    given_id = data.get("id");
    for i in range(len(entries)):
        new_genome = get_good_genome(entries[i]["geneSequence"])
        entries[i]["geneSequence"] = new_genome
    
    result = {
        "runId": given_id,
        "list":entries
    }

    logging.info("My result:{}".format(result))
    return json.dumps(result);