

"""
Helper file containing utility functions for processing user query

This file is used by H_process_query.py
"""

import logging

# ---------------------------------------------


# Function to dictionaries read from file_data
def read_dicts(data, val):
    """
    Function to read curr_table for given predicate.
    """

    logging.info('Reading current table for %s', str(val))

    # val == data for which predicate to select
    sub = data[val][0]
    obj = data[val][1]
    uid = data[val][2]
    pred1 = data[val][3]
    pred2 = data[val][4]
    pred31 = data[val][5]
    pred32 = data[val][6]
    pred4 = data[val][7]
    uid2 = data[val][8]

    logging.info('Reading done.')
    return sub, obj, uid, pred1, pred2, pred31, pred32, pred4, uid2


# Function to prepare display for result
def prepare_display(selects, var, disp, res_s, res_o, res_u, res_p1, res_p2, res_p31, res_p32, res_p4, res_u2, res_pred):
    """
    Function to prepare display for result using var[] and disp[]
    """
    logging.info('At prepare_display()')

    temp1 = dict()

    for i in range(1, len(selects)):
        #print(selects[i]+'...')
        logging.info('Currently processing: %s', str(selects[i]))

        k1 = selects[i].strip('?')

        temp1[k1] = []

        if k1 in var['sub']:
            logging.info('Found it in var_sub.')
            temp1.setdefault(k1, [])
            for ele in disp[k1]:
                if ele in res_s:
                    temp1[k1].append(ele)

        elif k1 in var['obj']:
            logging.info('Found it in var_obj.')
            temp1.setdefault(k1, [])
            for ele in disp[k1]:
                if ele in res_o:
                    temp1[k1].append(ele)

        elif k1 in var['uid']:
            logging.info('Found it in var_uid.')
            temp1.setdefault(k1, [])
            for ele in disp[k1]:
                if ele in res_u:
                    temp1[k1].append(ele)

        elif k1 in var['pred1']:
            logging.info('Found it in var_pred1.')
            temp1.setdefault(k1, [])
            for ele in disp[k1]:
                if ele in res_p1:
                    temp1[k1].append(ele)

        elif k1 in var['pred2']:
            logging.info('Found it in var_pred2.')
            temp1.setdefault(k1, [])
            for ele in disp[k1]:
                if ele in res_p2:
                    temp1[k1].append(ele)

        elif k1 in var['pred31']:
            logging.info('Found it in var_pred31.')
            temp1.setdefault(k1, [])
            for ele in disp[k1]:
                if ele in res_p31:
                    temp1[k1].append(ele)

        elif k1 in var['pred32']:
            logging.info('Found it in var_pred32.')
            temp1.setdefault(k1, [])
            for ele in disp[k1]:
                if ele in res_p32:
                    temp1[k1].append(ele)

        elif k1 in var['pred4']:
            logging.info('Found it in var_pred4.')
            temp1.setdefault(k1, [])
            for ele in disp[k1]:
                if ele in res_p4:
                    temp1[k1].append(ele)

        elif k1 in var['uid2']:
            logging.info('Found k1 in var_uid2.')
            temp1.setdefault(k1, [])
            for ele in disp[k1]:
                if ele in res_u2:
                    temp1[k1].append(ele)

        elif k1 in var['pred']:
            logging.info('Found it in var_pred.')
            temp1.setdefault(k1, [])
            for ele in disp[k1]:
                if ele in res_pred:
                    temp1[k1].append(ele)
        else:
            logging.warning('Unknown SELECT variable.')

    logging.info('Preparing display done.')
    return temp1


# Function to find intersection of res_pred and pred dictionaries
def intersect_pred(res_s, res_o, res_pred, pred):
    """
    Function used to match res_table based on curr_pred_table
    """

    logging.info('Matching pred with res_pred...')

    to_remove = []
    for key1 in res_pred:
        if key1 in pred:
            for s1 in pred[key1]:

                for o1 in pred[key1][s1]:
                    if s1 in res_s and o1 in res_o:
                        if s1 not in res_pred[key1]:
                            if s1 in res_pred[key1]:
                                res_pred[key1][s1] = res_pred[key1][s1] + [o1]
                            else:
                                res_pred[key1][s1] = [o1]
                        else:
                            res_pred[key1] = dict()
                            res_pred[key1][s1] = [o1]

        else:
            to_remove.append(key1)

    for key in to_remove:
        for s1 in res_pred[key]:
            o11 = res_pred[key][s1]

            for o1 in o11:
                res_s.pop(s1, None)
                res_o.pop(o1, None)
        res_pred.pop(key, None)


    logging.info('Matching done.')

    return res_s, res_o, res_pred


# Function to trim dictionaries for parameters
def trim_dict(res_s, res_o, dict1):
    """
    Function used remove unnecessary triples from param_dict using res_table
    """

    logging.info('Trimming parameter dict...')

    # Create new empty dict
    new_dict = dict()

    # For each year
    for key in dict1:

        # For each triple
        for s1 in dict1[key]:

            for o1 in dict1[key][s1]:
                # Keep triple if in res_table
                if s1 in res_s and o1 in res_o:
                    # Copy to new_dict
                    if key in new_dict:
                        if s1 in new_dict[key]:
                            new_dict[key][s1] = new_dict[key][s1] + [o1]
                        else:
                            new_dict[key][s1] = [o1]
                    else:
                        new_dict[key] = dict()
                        new_dict[key][s1] = [o1]

    # Replace old dict with new_dict
    dict1 = new_dict

    logging.info('Trimmed.')
    return dict1


# Function to match dictionaries for predicate
def match_predicate(res_s, res_o, res_pred, curr_pred):
    """
    Function used take intersection of res_pred and current table
    """

    logging.info('Matching res_pred with curr_pred...')

    to_remove = []

    # For each p1 in res_pred
    for p1 in res_pred:
        # If in curr_table then copy all curr_pred[p1] into res_pred
        if p1 in curr_pred:
            for s1 in curr_pred[p1]:
                o1 = curr_pred[p1][s1]

                if s1 in res_s and o1 in res_o:
                    # Add triple into res_pred
                    if p1 in res_pred:
                        res_pred[p1][s1] = o1
                    else:
                        res_pred[p1] = dict()
                        res_pred[p1][s1] = o1

        else:
            # If not in curr_table, then remove p1 from res_pred
            to_remove.append(p1)

    for p1 in to_remove:
        res_pred.pop(p1)

    logging.info('Matched.')
    return res_pred


# Function to create dictionaries for all variable
def createDictsForAll(data):

    logging.info('Creating dicts for all predicates...')

    sub = dict()
    obj = dict()
    uid = dict()
    uid2 = dict()
    pred1 = dict()
    pred2 = dict()
    pred31 = dict()
    pred32 = dict()
    pred4 = dict()
    curr_pred = dict()

    # Select all predicates one by one
    for val in data:
        sub.update(data[val][0])
        obj.update(data[val][1])
        uid.update(data[val][2])
        pred1.update(data[val][3])
        pred2.update(data[val][4])
        pred31.update(data[val][5])
        pred32.update(data[val][6])
        pred4.update(data[val][7])
        uid2.update(data[val][8])

        for s1 in sub:
            for o1 in sub[s1]:
                if val in curr_pred:
                    curr_pred[val][s1] = o1
                else:
                    curr_pred[val] = dict()
                    curr_pred[val][s1] = o1

    logging.info('Dictionaries created.')

    return sub, obj, uid, pred1, pred2, pred31, pred32, pred4, uid2, curr_pred


# Function to match given parameter dict with res_table
def matchParameter(res_s, res_o, dict1, param1):
    """
    Function used to match S, O & Param with param
    """

    logging.info('At matchParameter()...')

    # Create temp_res_table for storing triples
    temp_sub = dict()
    temp_obj = dict()

    # For each triple
    for s1 in dict1[param1]:

        for o1 in dict1[param1][s1]:

            # Keep triple if in res_table
            if s1 in res_s and o1 in res_o:
                u1 = res_s[s1][o1]

                # Append in temp_res_s
                if s1 in temp_sub:
                    temp_sub[s1][o1] = u1
                else:
                    temp_sub[s1] = dict()
                    temp_sub[s1][o1] = u1

                # Append in temp_res_o
                if o1 in temp_obj:
                    temp_obj[o1][s1] = u1
                else:
                    temp_obj[o1] = dict()
                    temp_obj[o1][s1] = u1

    # Copy back to original res_table
    res_s = temp_sub
    res_o = temp_obj

    logging.info('Matched.')

    return res_s, res_o


# Function to match given object with result table
def matchObject(res_s, res_o, res_u, o1):
    """
    Function used when only object is given subject is variable
    """

    logging.info('At matchObject()...')

    res_s = dict()
    res_u = dict()

    # Check if given object is in res_table
    if o1 in res_o:

        # if yes, create res_table using it
        for s1 in res_o[o1]:
            u1 = res_o[o1][s1]

            # Add to subject dict
            if s1 in res_s:
                res_s[s1][o1] = u1
            else:
                res_s[s1] = dict()
                res_s[s1][o1] = u1

            # Add to unique-id dict
            if u1 in res_u:
                res_u[u1][s1] = o1
            else:
                res_u[u1] = dict()
                res_u[u1][s1] = o1

        # Keep only given object
        temp = res_o[o1]
        res_o = dict()
        res_o[o1] = temp
    else:
        # Else empty all res_tables
        res_o = dict()

    logging.info('Matched.')

    return res_s, res_o, res_u


# Function to match given subject with result table
def matchSubject(res_s, res_o, res_u, s1):
    """
    Function used when only subject is given object is variable
    """

    logging.info('At matchSubject()...')

    res_o = dict()
    res_u = dict()

    # Check if given object is in res_table
    if s1 in res_s:

        # if yes, create res_table using it
        for o1 in res_s[s1]:
            u1 = res_s[s1][o1]

            # Add to object dict
            if o1 in res_o:
                res_o[o1][s1] = u1
            else:
                res_o[o1] = dict()
                res_o[o1][s1] = u1

            # Add to unique-id dict
            if u1 in res_u:
                res_u[u1][s1] = o1
            else:
                res_u[u1] = dict()
                res_u[u1][s1] = o1

        # Keep only given subject
        temp = res_s[s1]
        res_s = dict()
        res_s[s1] = temp
    else:
        # empty all res_tables
        res_s = dict()

    logging.info('Matched.')

    return res_s, res_o, res_u


# Function to match given subject with result table
def matchUID(res_s, res_o, res_u, u1):
    """
    Function used when UID is given
    """

    logging.info('At matchUID()...')

    res_s = dict()
    res_o = dict()

    # Check if given object is in res_table
    if u1 in res_u:

        # if yes, create res_table using it
        for s1 in res_u[u1]:
            o1 = res_u[u1][s1]

            # Add to object dict
            if o1 in res_o:
                res_o[o1][s1] = u1
            else:
                res_o[o1] = dict()
                res_o[o1][s1] = u1

            # Add to subject dict
            if s1 in res_s:
                res_s[s1][o1] = u1
            else:
                res_s[s1] = dict()
                res_s[s1][o1] = u1

        # Keep only given UID
        temp = res_u[u1]
        res_u = dict()
        res_s[u1] = temp
    else:
        # empty all res_tables
        res_u = dict()

    logging.info('Matched.')

    return res_s, res_o, res_u


# Function to match both given subject and given object
def matchBoth(res_s, res_o, s1, o1):
    """
    Function used when both subject and object are given
    """

    logging.info('At matchBoth()...')

    # Create empty dicts
    sub = dict()
    obj = dict()
    uid = dict()

    # Check if both sub and obj are in res_table
    if s1 in res_s and o1 in res_o:
        val4 = res_s[s1][o1]

        # If yes, copy only that triple
        sub[s1] = dict()
        sub[s1][o1] = val4

        obj[o1] = dict()
        obj[o1][s1] = val4

        uid[val4] = dict()
        uid[val4][s1] = o1

    logging.info('Matched.')

    return sub, obj, uid



# Function to match xyz with res_s or res_o or res_u
def matchXYZ(res_s, res_o, res_u, pos, xyz, pos2):
    """
    Function used to match S, O & U with given s, o or u
    """

    logging.info('At matchXYZ()')
    logging.info('Got pos1: %d', int(pos))
    logging.info('Got pos2: %d', int(pos2))

    if pos == 1:
        logging.info('Matching xyz with res_s')
        to_remove = []
        to_append = []
        if pos2 == 1:
            logging.info('Found xyz as sub')
            sub = xyz

            logging.info('New subject matching with previous subject...')
            to_remove = []
            to_append = []
            for val1 in res_s:
                if val1 in sub:
                    #print('New subject to be added:', val1)

                    # Addition Process
                    s1 = val1
                    for o1 in sub[s1]:
                        u1 = sub[s1][o1]

                        # Append in res_o
                        if o1 in res_o:
                            res_o[o1][s1] = u1
                        else:
                            res_o[o1] = dict()
                            res_o[o1][s1] = u1

                        # Append in res_u
                        if u1 in res_u:
                            res_u[u1][s1] = o1
                        else:
                            res_u[u1] = dict()
                            res_u[u1][s1] = o1

                        to_append.append([s1, o1, u1])

                else:
                    to_remove.append(val1)

            # Append in res_s
            for [s1, o1, u1] in to_append:
                if s1 in res_s:
                    res_s[s1][o1] = u1
                else:
                    res_s[s1] = dict()
                    res_s[s1][o1] = u1

            # Removal Process
            for ele in to_remove:
                val1 = ele
                for val3 in res_s[val1]:
                    val4 = res_s[val1][val3]

                    res_u[val4].pop(val1)
                    res_o[val3].pop(val1)
                res_s.pop(val1)

            logging.info('Matched.')

        elif pos2 == 2:
            logging.info('Found xyz as obj')
            obj = xyz

            logging.info('New object matching with previous subject...')
            to_remove = []
            to_append = []
            for val1 in res_s:
                if val1 in obj:
                    # print('New subject to be added:', val1)

                    # Addition Process
                    o1 = val1
                    for s1 in obj[o1]:
                        u1 = obj[o1][s1]

                        # Append in res_o
                        if o1 in res_o:
                            res_o[o1][s1] = u1
                        else:
                            res_o[o1] = dict()
                            res_o[o1][s1] = u1

                        # Append in res_u
                        if u1 in res_u:
                            res_u[u1][s1] = o1
                        else:
                            res_u[u1] = dict()
                            res_u[u1][s1] = o1

                        to_append.append([s1, o1, u1])

                else:
                    to_remove.append(val1)

            # Append in res_s
            for [s1, o1, u1] in to_append:
                if s1 in res_s:
                    res_s[s1][o1] = u1
                else:
                    res_s[s1] = dict()
                    res_s[s1][o1] = u1

            # Removal Process
            for ele in to_remove:
                val1 = ele
                val33 = res_s[val1]
                for val3 in val33:
                    val4 = res_s[val1][val3]

                    res_u[val4].pop(val1)
                    res_o[val3].pop(val1)
                res_s.pop(val1)

            logging.info('Matched.')

        elif pos2 == 3:
            logging.info('Found xyz as uid')
            uid = xyz

            logging.info('New uid matching with previous subject...')
            to_remove = []
            to_append = []
            for val1 in res_s:
                if val1 in uid:
                    # print('New subject to be added:', val1)

                    # Addition Process
                    u1 = val1
                    for s1 in uid[u1]:
                        o1 = uid[u1][s1]

                        # Append in res_o
                        if o1 in res_o:
                            res_o[o1][s1] = u1
                        else:
                            res_o[o1] = dict()
                            res_o[o1][s1] = u1

                        # Append in res_u
                        if u1 in res_u:
                            res_u[u1][s1] = o1
                        else:
                            res_u[u1] = dict()
                            res_u[u1][s1] = o1

                        to_append.append([s1, o1, u1])

                else:
                    to_remove.append(val1)

            # Append in res_s
            for [s1, o1, u1] in to_append:
                if s1 in res_s:
                    res_s[s1][o1] = u1
                else:
                    res_s[s1] = dict()
                    res_s[s1][o1] = u1

            # Removal Process
            for ele in to_remove:
                val1 = ele
                val33 = res_s[val1]
                for val3 in val33:
                    val4 = res_s[val1][val3]

                    res_u[val4].pop(val1)
                    res_o[val3].pop(val1)
                res_s.pop(val1)

            logging.info('Matched.')

        else:
            logging.warning('Unknown pos2. Check function call')

    elif pos == 2:
        logging.info('Matching xyz with res_o')
        if pos2 == 1:
            logging.info('Found xyz as sub')
            sub = xyz

            logging.info('New subject matching with previous object...')
            to_remove = []
            to_append = []
            for val3 in res_o:
                if val3 in sub:
                    # print('New object to be added:', val3)

                    # Addition Process
                    s1 = val3
                    for o1 in sub[s1]:
                        u1 = sub[s1][o1]

                        # Append in res_u
                        if u1 in res_u:
                            res_u[u1][s1] = o1
                        else:
                            res_u[u1] = dict()
                            res_u[u1][s1] = o1

                        # Append in res_s
                        if s1 in res_s:
                            res_s[s1][o1] = u1
                        else:
                            res_s[s1] = dict()
                            res_s[s1][o1] = u1

                        to_append.append([o1, s1, u1])

                else:
                    to_remove.append(val3)

            # Append in res_o
            for [o1, s1, u1] in to_append:
                if o1 in res_o:
                    res_o[o1][s1] = u1
                else:
                    res_o[o1] = dict()
                    res_o[o1][s1] = u1

            # Removal Process
            for ele in to_remove:
                val3 = ele
                val1 = res_o[val3]

                for val11 in val1:
                    val4 = res_o[val3][val11]

                    res_s[val11].pop(val3)
                    res_u[val4].pop(val11)
                res_o.pop(val3)

            logging.info('Matched.')

        elif pos2 == 2:
            logging.info('Found xyz as obj')
            obj = xyz

            logging.info('New object matching with previous object...')
            to_remove = []
            to_append = []
            for val3 in res_o:
                if val3 in obj:
                    # print('New object to be added:', val3)

                    # Addition Process
                    o1 = val3
                    for s1 in obj[o1]:
                        u1 = obj[o1][s1]

                        # Append in res_u
                        if u1 in res_u:
                            res_u[u1][s1] = o1
                        else:
                            res_u[u1] = dict()
                            res_u[u1][s1] = o1

                        # Append in res_s
                        if s1 in res_s:
                            res_s[s1][o1] = u1
                        else:
                            res_s[s1] = dict()
                            res_s[s1][o1] = u1

                        to_append.append([o1, s1, u1])

                else:
                    to_remove.append(val3)

            # Append in res_o
            for [o1, s1, u1] in to_append:
                if o1 in res_o:
                    res_o[o1][s1] = u1
                else:
                    res_o[o1] = dict()
                    res_o[o1][s1] = u1

            # Removal Process
            for ele in to_remove:
                val3 = ele
                val1 = res_o[val3]

                for val11 in val1:
                    val4 = res_o[val3][val11]

                    res_s[val11].pop(val3)
                    res_u[val4].pop(val11)
                res_o.pop(val3)

            logging.info('Matched.')

        elif pos2 == 3:
            logging.info('Found xyz as uid')
            uid = xyz

            logging.info('New UID matching with previous object...')
            to_remove = []
            to_append = []
            for val3 in res_o:
                if val3 in uid:
                    # print('New object to be added:', val3)

                    # Addition Process
                    u1 = val3
                    for s1 in uid[u1]:
                        o1 = uid[u1][s1]

                        # Append in res_u
                        if u1 in res_u:
                            res_u[u1][s1] = o1
                        else:
                            res_u[u1] = dict()
                            res_u[u1][s1] = o1

                        # Append in res_s
                        if s1 in res_s:
                            res_s[s1][o1] = u1
                        else:
                            res_s[s1] = dict()
                            res_s[s1][o1] = u1

                        to_append.append([o1, s1, u1])

                else:
                    to_remove.append(val3)

            # Append in res_o
            for [o1, s1, u1] in to_append:
                if o1 in res_o:
                    res_o[o1][s1] = u1
                else:
                    res_o[o1] = dict()
                    res_o[o1][s1] = u1

            # Removal Process
            for ele in to_remove:
                val3 = ele
                val1 = res_o[val3]

                for val11 in val1:
                    val4 = res_o[val3][val11]

                    res_s[val11].pop(val3)
                    res_u[val4].pop(val11)
                res_o.pop(val3)

            logging.info('Matched.')

        else:
            logging.warning('Unknown pos2. Check function call')

    elif pos == 3:
        logging.info('Matching xyz with res_u')

        if pos2 == 1:
            logging.info('Found xyz as sub')
            sub = xyz

            logging.info('New subject matches with previous UID...')
            to_remove = []
            to_append = []
            for val4 in res_u:
                if val4 in sub:
                    # print('New subject to be added:', val4)

                    s1 = val4
                    for o1 in sub[s1]:
                        u1 = sub[s1][o1]

                        # Append in res_s
                        if s1 in res_s:
                            res_s[s1][o1] = u1
                        else:
                            res_s[s1] = dict()
                            res_s[s1][o1] = u1

                        # Append in res_o
                        if o1 in res_o:
                            res_o[o1][s1] = u1
                        else:
                            res_o[o1] = dict()
                            res_o[o1][s1] = u1

                        to_append.append([u1, s1, o1])

                else:
                    to_remove.append(val4)

            # Add required tuples
            for [u1, s1, o1] in to_append:
                if u1 in res_u:
                    res_u[u1][s1] = o1
                else:
                    res_u[u1] = dict()
                    res_u[u1][s1] = o1

            # Remove unwanted tuples
            for ele in to_remove:
                val4 = ele

                val11 = res_u[val4]
                for val1 in val11:
                    val3 = res_u[val4][val1]

                    res_s[val1].pop(val3)
                    res_o[val3].pop(val1)
                res_u.pop(val4)

            logging.info('Matched.')

        elif pos2 == 2:
            logging.info('Found xyz as obj')
            obj = xyz

            logging.info('New object matching with previous UID...')
            to_remove = []
            to_append = []
            for val4 in res_u:
                if val4 in obj:
                    # print('New subject to be added:', val4)

                    o1 = val4
                    for s1 in obj[o1]:
                        u1 = obj[o1][s1]

                        # Append in res_s
                        if s1 in res_s:
                            res_s[s1][o1] = u1
                        else:
                            res_s[s1] = dict()
                            res_s[s1][o1] = u1

                        # Append in res_o
                        if o1 in res_o:
                            res_o[o1][s1] = u1
                        else:
                            res_o[o1] = dict()
                            res_o[o1][s1] = u1

                        to_append.append([u1, s1, o1])

                else:
                    to_remove.append(val4)

            # Add required tuples
            for [u1, s1, o1] in to_append:
                if u1 in res_u:
                    res_u[u1][s1] = o1
                else:
                    res_u[u1] = dict()
                    res_u[u1][s1] = o1

            # Remove unwanted tuples
            for ele in to_remove:
                val4 = ele

                val11 = res_u[val4]
                for val1 in val11:
                    val3 = res_u[val4][val1]

                    res_s[val1].pop(val3)
                    res_o[val3].pop(val1)
                res_u.pop(val4)

            logging.info('Matched.')

        elif pos2 == 3:
            logging.info('Found xyz as uid')
            uid = xyz

            logging.info('New UID matching with previous UID...')
            to_remove = []
            to_append = []
            for val4 in res_u:
                if val4 in uid:
                    # print('New subject to be added:', val4)

                    u1 = val4
                    for s1 in uid[u1]:
                        o1 = uid[u1][s1]

                        # Append in res_s
                        if s1 in res_s:
                            res_s[s1][o1] = u1
                        else:
                            res_s[s1] = dict()
                            res_s[s1][o1] = u1

                        # Append in res_o
                        if o1 in res_o:
                            res_o[o1][s1] = u1
                        else:
                            res_o[o1] = dict()
                            res_o[o1][s1] = u1

                        to_append.append([u1, s1, o1])

                else:
                    to_remove.append(val4)

            # Add required tuples
            for [u1, s1, o1] in to_append:
                if u1 in res_u:
                    res_u[u1][s1] = o1
                else:
                    res_u[u1] = dict()
                    res_u[u1][s1] = o1

            # Remove unwanted tuples
            for ele in to_remove:
                val4 = ele

                val11 = res_u[val4]
                for val1 in val11:
                    val3 = res_u[val4][val1]

                    res_s[val1].pop(val3)
                    res_o[val3].pop(val1)
                res_u.pop(val4)

            logging.info('Matched.')

        else:
            logging.warning('Unmatched pos2. Check function call')

    else:
        logging.warning('Unmatched pos. Check function call')

    return res_s, res_o, res_u


# Function to add values.keys() to dict1[vars]
def add_vars_dict(dict1, var, values):
    """
    Function used to add given var.keys() to display dict
    """

    logging.info('Adding %s.keys to display...', str(var))
    if var not in dict1:
        dict1[var] = list(values.keys())
    else:
        dict1[var] = dict1[var] + list(values.keys())
    logging.info('Added.')
    return dict1
