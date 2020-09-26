import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def get_good_genome(my_str):
    my_dict = {'A': 0, 'C': 0, 'G':0, 'T':0}
    for letter in my_str:
        my_dict[str(letter)] += 1
        
    possible = {'AACGT': ((2,1,1,1),15),
                'AACC': ((2,2,0,0),25),
                'AAC': ((2,1,0,0),0),
                'AAG': ((2,0,1,0),0),
                'AAT': ((2,0,0,1),0)}
    possible_nums = {'AACGT': 0, 'AACC': 0, 'AAC': 0, 'AAG': 0, 'AAT': 0}

    #outs = [return_list, points, last_dict, possible_nums]
    def recursive_call(my_dict, curr_str_list, possible, points, possible_nums): 
        # Base Case
        if my_dict['C']==0 and my_dict['G']==0 and my_dict['T']==0:
            if my_dict['A'] >= 3:                
                neg_points = my_dict['A'] // 3 * 10
                points -= neg_points
                my_dict['A'] = 0
                curr_str_list.extend(['AAA']*my_dict['A']//3)
                curr_str_list.extend(['A'*my_dict['A']%3])
            elif my_dict['A']>0:
                my_dict['A'] = 0
                curr_str_list.extend(['A'*my_dict['A']])
            return [curr_str_list, points, my_dict, possible_nums]

        out_list = []
        for key in possible.keys():
            if (my_dict['C'] - possible[key][0][1] >= 0 and my_dict['G'] - possible[key][0][2] >= 0
                and my_dict['T'] - possible[key][0][3] >= 0):

                new_dict = my_dict.copy()
                new_dict['A'] -= possible[key][0][0]
                new_dict['C'] -= possible[key][0][1]
                new_dict['G'] -= possible[key][0][2]
                new_dict['T'] -= possible[key][0][3]

                new_possible_nums = possible_nums.copy()
                new_possible_nums[key] += 1

                out_list.append(recursive_call(new_dict, curr_str_list + [key], possible, points+possible[key][1], new_possible_nums))
        return max(out_list, key=lambda x:x[1])

    if my_dict['A'] >= min(my_dict['C'], my_dict['G'], my_dict['T']):
        return_list, points, last_dict, new = recursive_call(my_dict, [], possible, 0, possible_nums)
        if last_dict['A'] >= 0:
            return ''.join(return_list)
        else:
            removal_num = abs(last_dict['A'])
            for i in range(len(return_list)):
                if removal_num <= 0:
                    break
                if return_list[i] == 'AACGT':
                    return_list[i] = 'ACGT'
                    removal_num -= 1
                else:
                    if removal_num >= 2:
                        removal_num -=2
                        return_list[i] = return_list[i][2:]
                    else:
                        removal_num -= 1
                        return_list[i] = return_list[i][1:]
            return ''.join(return_list)
    else:
        if my_dict['C'] - my_dict['A'] == 1:
            num_CC = 1
            num_ACGT = my_dict['A'] - 1
            num_C = (my_dict['C'] - num_ACGT) % 2
            num_G = my_dict['G'] - num_ACGT
            num_T = my_dict['T'] - num_ACGT
            return 'ACGT'*num_ACGT + 'CC'*num_CC + 'C'*num_C + 'G'*num_G + 'T'*num_T
        else:
            num_ACGT = my_dict['A']
            num_CC = (my_dict['C'] - num_ACGT) // 2
            num_C = (my_dict['C'] - num_ACGT) % 2
            num_G = my_dict['G'] - num_ACGT
            num_T = my_dict['T'] - num_ACGT
            return 'ACGT'*num_ACGT + 'CC'*num_CC + 'C'*num_C + 'G'*num_G + 'T'*num_T

@app.route('GMO', methods=["POST"])
def get_gmo():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    entries = data.get("list");
    given_id = data.get("id");
    
    for i in range(len(entries)):
        new_genome = get_good_genome(entries[i]["geneSequence"])
        entries[i]["geneSequence"] = new_genome

    logging.info("My result:{}".format(entries))
    return json.dumps({"id": given_id, "list": entries});