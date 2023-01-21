
"""
Helper file containing functions to process query

This file is used by C_user_queries.py
"""

import logging
from H_utility_functions import *


# ---------------------------------------------


# Function to process query
def process_query(query, data):
    """
    Function to process user query and generate result.
    """

    logging.info('---------------------------->')
    logging.info('At process_query()')

    # Display dictionary to store output triples
    disp = dict()

    # Result table
    res_s = dict()
    res_o = dict()
    res_u = dict()
    res_p1 = dict()
    res_p2 = dict()
    res_p31 = dict()
    res_p32 = dict()
    res_p4 = dict()
    res_u2 = dict()
    res_pred = dict()

    # Dictionary to store variables
    var = dict()
    var['sub'] = ['']
    var['obj'] = ['']
    var['uid'] = ['']
    var['pred'] = ['']
    var['pred1'] = ['']
    var['pred2'] = ['']
    var['pred31'] = ['']
    var['pred32'] = ['']
    var['pred4'] = ['']
    var['uid2'] = ['']

    # Iterate over user queries
    i = 2
    while i <= len(query) - 2:
        line = query[i].split(' ')

        # Skip LIMIT clause
        if line[0].startswith('LIMIT') or line[0].startswith('limit') or line[0].startswith('}'):
            i = i + 1
            continue

        print('\nStarting query: ' + str(i-1))
        logging.info('-----------------------------')
        logging.info('Starting query: %d', int(i-1))

        # Current Table
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

        # Used for pred_parameters processing
        val_k = line[1].split('[')

        #---------------------PREDICATE-IS-GIVEN--------------------------
        if not line[1].startswith('?'):
            logging.info('Predicate is not variable.')
            logging.info('Given predicate: %s', str(val_k[0]))


            # Create table for current query
            sub, obj, uid, pred1, pred2, pred31, pred32, pred4, uid2 = read_dicts(
                data, val_k[0])


            # First query processings ----------------
            if i == 2:
                logging.info('First query.')

                res_s, res_o, res_u = sub, obj, uid
                logging.info('Copied curr_table into res_table')
            else:
                logging.info('Query #%d', (i-1))


            # Subject and Object processing ----------------
            if not line[0].startswith('?') and not line[2].startswith('?'):
                logging.info('Case 1: Both subject and object are given.')

                s1 = line[0]
                o1 = line[2]

                logging.info('Given sub: %s', str(s1))
                logging.info('Given obj: %s', str(o1))

                res_s, res_o, res_u = matchBoth(res_s, res_o, s1, o1)

            elif line[0].startswith('?') and not line[2].startswith('?'):
                logging.info('Case 2: Subject is variable and object is given.')

                s1 = line[0].strip('?')
                o1 = line[2]

                logging.info('?v_sub: %s', str(s1))
                logging.info('Given obj: %s', str(o1))

                res_s, res_o, res_u = matchObject(res_s, res_o, res_u, o1)

                # Subject processing
                if s1 in var['sub']:
                    logging.info('Matching new subject with previous subject...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 1, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['obj']:
                    logging.info('Matching new subject with previous object...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 2, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['uid']:
                    logging.info('Matching new subject with previous UID...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 3, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['uid2']:
                    logging.info('Matching new subject with previous UID2...')
                    res_s, res_o, res_u2 = matchXYZ(
                        res_s, res_o, res_u2, 3, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['pred']:
                    logging.warning('New subject matches with previous predicate.')
                else:
                    logging.info('New subject is not matching with anything.')
                    logging.info('Adding %s to vars.', str(s1))
                    var.setdefault('sub', [])
                    var['sub'].append(s1)
                    disp = add_vars_dict(disp, s1, sub)

            elif not line[0].startswith('?') and line[2].startswith('?'):
                logging.info('Case 3: Subject is given and object is variable.')

                s1 = line[0]
                o1 = line[2].strip('?')

                logging.info('Given sub: %s', str(s1))
                logging.info('?v_obj: %s', str(o1))

                logging.info('Calling matchSubject() with given subject...')
                res_s, res_o, res_u = matchSubject(res_s, res_o, res_u, s1)

                # Object processing
                if o1 in var['sub']:
                    logging.info('Matching new object with previous subject...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 1, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['obj']:
                    logging.info('Matching new object with previous object...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 2, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['uid']:
                    logging.info('Matching new object with previous UID...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 3, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['uid2']:
                    logging.info('Matching new object with previous UID2...')
                    res_s, res_o, res_u2 = matchXYZ(
                        res_s, res_o, res_u2, 3, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['pred']:
                    logging.warning('New object matches with previous predicate.')
                else:
                    logging.info('New Object is not common with anything and is variable')
                    logging.info('Adding %s to vars.', str(o1))
                    var.setdefault('obj', [])
                    var['obj'].append(o1)
                    disp = add_vars_dict(disp, o1, obj)

            else:
                logging.info('Case 4: Both subject and object are variable.')

                s1 = line[0].strip('?')
                o1 = line[2].strip('?')

                logging.info('?v_sub: %s', str(s1))
                logging.info('?v_obj: %s', str(o1))

                # Subject processing
                if s1 in var['sub']:
                    logging.info('Matching new subject with previous subject...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 1, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['obj']:
                    logging.info('Matching new subject with previous object...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 2, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['uid']:
                    logging.info('Matching new subject with previous UID...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 3, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['uid2']:
                    logging.info('Matching new subject with previous UID2...')
                    res_s, res_o, res_u2 = matchXYZ(
                        res_s, res_o, res_u2, 3, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['pred']:
                    logging.warning('New subject matches with previous predicate.')
                else:
                    logging.info('New subject is not matching with anything.')
                    logging.info('Adding %s to vars.', str(s1))
                    var.setdefault('sub', [])
                    var['sub'].append(s1)
                    disp = add_vars_dict(disp, s1, sub)

                # Object processing
                if o1 in var['sub']:
                    logging.info('Matching new object with previous subject...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 1, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['obj']:
                    logging.info('Matching new object with previous object...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 2, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['uid']:
                    logging.info('Matching new object with previous UID...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 3, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['uid2']:
                    logging.info('Matching new object with previous UID2...')
                    res_s, res_o, res_u2 = matchXYZ(
                        res_s, res_o, res_u2, 3, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['pred']:
                    logging.warning('New object matches with previous predicate.')
                else:
                    logging.info('New Object is not common with anything.')
                    logging.info('Adding %s to vars.', str(o1))
                    var.setdefault('obj', [])
                    var['obj'].append(o1)
                    disp = add_vars_dict(disp, o1, obj)


            # UID Processing ----------------
            if line[3].startswith('?'):
                logging.info('UID is variable.')

                u1 = line[3].strip('?')
                logging.info('?v_uid: %s', str(u1))

                if u1 in var['sub']:
                    logging.info('Matching new UID with previous subject...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 1, uid, 3)
                    logging.info('Matching done.')
                elif u1 in var['obj']:
                    logging.info('Matching new UID with previous object...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 2, uid, 3)
                    logging.info('Matching done.')
                elif u1 in var['uid']:
                    logging.info('Matching new UID with previous uid...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 3, uid, 3)
                    logging.info('Matching done.')
                elif u1 in var['uid2']:
                    logging.info('Matching new UID with previous uid2...')
                    res_s, res_o, res_u2 = matchXYZ(
                        res_s, res_o, res_u2, 3, uid, 3)
                    logging.info('Matching done.')
                elif u1 in var['pred']:
                    logging.warning('New UID matches with previous predicate.')
                else:
                    logging.info('UID is new.')
                    logging.info('Adding %s to vars.', str(u1))
                    var.setdefault('uid', [])
                    var['uid'].append(u1)
                    disp = add_vars_dict(disp, u1, uid)
            else:
                logging.info('UID is given.')

                u1 = line[3]
                logging.info('Given UID: %s', str(u1))

                logging.info('Calling matchUID() with given UID...')
                res_s, res_o, res_u = matchUID(res_s, res_o, res_u, u1)


        #---------------------PREDICATE-IS-VARIABLE--------------------------
        else:
            logging.info('Predicate is a variable in user query.')

            p1 = val_k[0].strip('?')
            logging.info('?v_pred: %s', p1)

            # Create curr_table for variable predicate
            sub, obj, uid, pred1, pred2, pred31, pred32, pred4, uid2, curr_pred = createDictsForAll(data)

            # First query processings
            if i == 2:
                logging.info('First query.')
                res_s, res_o, res_u, res_pred = sub, obj, uid, curr_pred
                logging.info('Copied curr_table into res_table')
            else:
                logging.info('Query #: %d', int(i - 1))
                res_pred = match_predicate(res_s, res_o, res_pred, curr_pred)

            # Predicate processing ----------
            if p1 in var['sub']:
                logging.warning('Predicate matches with previous subject.')
            elif p1 in var['pred']:
                logging.warning('Predicate matches with previous predicate.')
            elif p1 in var['obj']:
                logging.warning('Predicate matches with previous object.')
            elif p1 in var['uid']:
                logging.warning('Predicate matches with previous uid.')
            elif p1 in var['uid2']:
                logging.warning('Predicate matches with previous uid2.')
            else:
                logging.info('Predicate is new.')
                logging.info('Adding %s to vars.', str(p1))
                var.setdefault('pred', [])
                var['pred'].append(p1)
                disp = add_vars_dict(disp, p1, curr_pred)

            # Subject processing ----------
            if line[0].startswith('?'):
                logging.info('Subject is variable.')
                s1 = line[0].strip('?')
                logging.info('?v_sub: %s', str(s1))
                if s1 in var['sub']:
                    logging.info('Matching new subject with previous subject...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 1, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['obj']:
                    logging.info('Matching new subject with previous object...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 2, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['uid']:
                    logging.info('Matching new subject with previous uid...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 3, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['uid2']:
                    logging.info('Matching new subject with previous uid2...')
                    res_s, res_o, res_u2 = matchXYZ(
                        res_s, res_o, res_u2, 3, sub, 1)
                    logging.info('Matching done.')
                elif s1 in var['pred']:
                    logging.warning('New subject matches with previous predicate.')
                else:
                    logging.info('Subject is new.')
                    logging.info('Adding %s to vars.', str(s1))
                    var.setdefault('sub', [])
                    var['sub'].append(s1)
                    disp = add_vars_dict(disp, s1, sub)
            else:
                logging.info('Subject is given.')

                s1 = line[0]
                logging.info('Given sub: %s', str(s1))

                logging.info('Calling matchSubject() with given subject...')
                res_s, res_o, res_u = matchSubject(res_s, res_o, res_u, s1)


            # Object processing ----------
            if line[2].startswith('?'):
                logging.info('Object is variable.')

                o1 = line[2].strip('?')
                logging.info('?v_obj: %s', str(o1))
                if o1 in var['sub']:
                    logging.info('Matching new object with previous subject...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 1, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['obj']:
                    logging.info('Matching new object with previous object...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 2, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['uid']:
                    logging.info('Matching new object with previous uid...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 3, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['uid2']:
                    logging.info('Matching new object with previous uid2...')
                    res_s, res_o, res_u2 = matchXYZ(
                        res_s, res_o, res_u2, 3, obj, 2)
                    logging.info('Matching done.')
                elif o1 in var['pred']:
                    logging.warning('New object matches with previous predicate.')
                else:
                    logging.info('Object is new.')
                    logging.info('Adding %s to vars.', str(o1))
                    var.setdefault('obj', [])
                    var['obj'].append(o1)
                    disp = add_vars_dict(disp, o1, obj)
            else:
                logging.info('Object is given.')
                o1 = line[2]
                logging.info('Given sub: %s', str(o1))
                logging.info('Calling matchObject() with given subject...')
                res_s, res_o, res_u = matchObject(res_s, res_o, res_u, o1)


            # UID Processing ----------
            if line[3].startswith('?'):
                logging.info('UID is variable.')

                u1 = line[3].strip('?')
                logging.info('?v_uid: %s', str(u1))

                if u1 in var['sub']:
                    logging.info('Match new UID with previous subject...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 1, uid, 3)
                    logging.info('Matching done.')
                elif u1 in var['obj']:
                    logging.info('Match new UID with previous object...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 2, uid, 3)
                    logging.info('Matching done.')
                elif u1 in var['uid']:
                    logging.info('Match new UID with previous UID...')
                    res_s, res_o, res_u = matchXYZ(
                        res_s, res_o, res_u, 3, uid, 3)
                    logging.info('Matching done.')
                elif u1 in var['uid2']:
                    logging.info('Match new UID with previous UID2...')
                    res_s, res_o, res_u2 = matchXYZ(
                        res_s, res_o, res_u2, 3, uid, 3)
                    logging.info('Matching done.')
                elif u1 in var['pred']:
                    logging.warning('New UID matches with previous predicate.')
                else:
                    print('UID is new.')
                    logging.info('Adding %s to vars.', str(u1))
                    var.setdefault('uid', [])
                    var['uid'].append(u1)
                    disp = add_vars_dict(disp, u1, uid)
            else:
                logging.info('UID is given.')
                u1 = line[3]
                logging.info('Given UID: %s', str(u1))
                logging.info('Calling matchUID() with given UID...')
                res_s, res_o, res_u = matchUID(res_s, res_o, res_u, u1)


        # ------------------PARAMETER-PROCESSING-------------------

        logging.info('Now processing predicate parameters...')

        # Splitting predicates
        val_k2 = val_k[1][:-1].split(',')
        logging.info('val_k2: %s', str(val_k2))

        # First parameter ----------
        if val_k2[0].startswith('?'):
            logging.info('First parameter variable')
            t1 = val_k2[0].strip('?')
            logging.info('?v_t1: %s', str(t1))

            if t1 in var['pred1']:
                logging.warning('First parameter is not new.')
            else:
                logging.info('First parameter is new.')
                pred1 = trim_dict(res_s, res_o, pred1)
                logging.info('Adding %s to vars.', str(t1))
                var.setdefault('pred1', [])
                var['pred1'].append(t1)
                disp = add_vars_dict(disp, t1, pred1)

                # If first query
                if i == 2:
                    logging.info('First query.')
                    res_p1 = pred1
                    logging.info('Copied curr_pred1 into res_p1')
                else:
                    logging.info('Not first query.')

        elif val_k2[0] == "":
            logging.info('First parameter not needed.')
        else:
            logging.info('First parameter given.')
            logging.info('Given t1: %s', str(val_k2[0]))

            # Keep matching triples
            if val_k2[0] in pred1:
                res_s, res_o = matchParameter(res_s, res_o, pred1, val_k2[0])
            else:
                logging.info('Given t1 is not in curr_table.')

                res_s = dict()
                res_o = dict()
                res_u = dict()
                res_p1 = dict()
                res_p2 = dict()
                res_p31 = dict()
                res_p32 = dict()
                res_p4 = dict()
                res_u2 = dict()
                logging.info('All res_tables emptied.')

        # Second parameter ----------
        if val_k2[1].startswith('?'):
            logging.info('Second parameter variable.')

            t2 = val_k2[1].strip('?')
            logging.info('?v_t2: %s', str(t2))

            # Match variable to previously known variable
            if t2 in var['pred2']:
                logging.info('Matching new t2 with previous pred2...')
                res_s, res_o, res_p2 = intersect_pred(res_s, res_o, res_p2, pred2)
                logging.info('Matching done.')
            elif t2 in var['pred31']:
                logging.info('Matching new t2 with previous pred31...')
                res_s, res_o, res_p31 = intersect_pred(res_s, res_o, res_p31, pred2)
                logging.info('Matching done.')
            elif t2 in var['pred32']:
                logging.info('Matching new t2 with previous pred32...')
                res_s, res_o, res_p32 = intersect_pred(res_s, res_o, res_p32, pred2)
                logging.info('Matching done.')
            else:
                logging.info('Second parameter is new.')
                pred2 = trim_dict(res_s, res_o, pred2)
                logging.info('Adding %s to vars.', str(t2))
                var.setdefault('pred2', [])
                var['pred2'].append(t2)
                disp = add_vars_dict(disp, t2, pred2)

                # If first query
                if i == 2:
                    logging.info('First query.')
                    res_p2 = pred2
                    logging.info('Copied curr_pred2 into res_p2')
                else:
                    logging.info('Not first query.')

        elif val_k2[1] == "":
            logging.info('Second parameter not needed.')
        else:
            logging.info('Second parameter given.')
            logging.info('Given t2: %s', str(val_k2[1]))

            # Keep matching triples
            if val_k2[1] in pred2:
                res_s, res_o = matchParameter(res_s, res_o, pred2, val_k2[1])
            else:
                logging.info('Given t2 is not in curr_table.')

                res_s = dict()
                res_o = dict()
                res_u = dict()
                res_p1 = dict()
                res_p2 = dict()
                res_p31 = dict()
                res_p32 = dict()
                res_p4 = dict()
                res_u2 = dict()
                logging.info('All res_tables emptied.')

        # Third1 parameter ----------
        val_k2[2] = val_k2[2][1:]
        if val_k2[2].startswith('?'):
            logging.info('Third1 parameter variable')
            t31 = val_k2[2].strip('?')
            logging.info('?v_t31: %s', str(t31))

            if t31 in var['pred2']:
                logging.info('Matching new t31 with previous pred2...')
                res_s, res_o, res_p2 = intersect_pred(res_s, res_o, res_p2, pred31)
                logging.info('Matching done.')
            elif t31 in var['pred31']:
                logging.info('Matching new t31 with previous pred31...')
                res_s, res_o, res_p31 = intersect_pred(res_s, res_o, res_p31, pred31)
                logging.info('Matching done.')
            elif t31 in var['pred32']:
                logging.info('Matching new t31 with previous pred32...')
                res_s, res_o, res_p32 = intersect_pred(res_s, res_o, res_p32, pred31)
                logging.info('Matching done.')
            else:
                logging.info('Third1 parameter is new.')
                pred31 = trim_dict(res_s, res_o, pred31)
                logging.info('Adding %s to vars.', str(t31))
                var.setdefault('pred31', [])
                var['pred31'].append(t31)
                disp = add_vars_dict(disp, t31, pred31)

                # If first query, copy curr_table into res_table
                if i == 2:
                    logging.info('First query.')
                    res_p31 = pred31
                    logging.info('Copied curr_pred31 into res_p31')
                else:
                    logging.info('Not first query.')

        elif val_k2[2] == "":
            logging.info('Third1 parameter not needed')
        else:
            logging.info('Third1 parameter given')
            logging.info('Given t31: %s', str(val_k2[2]))

            # Keep matching triples
            if val_k2[2] in pred31:
                res_s, res_o = matchParameter(res_s, res_o, pred31, val_k2[2])
            else:
                logging.info('Given t31 is not in curr_table.')

                # Otherwise empty all res_tables
                res_s = dict()
                res_o = dict()
                res_u = dict()
                res_p1 = dict()
                res_p2 = dict()
                res_p31 = dict()
                res_p32 = dict()
                res_p4 = dict()
                res_u2 = dict()

                logging.info('All res_tables emptied.')

        # Third2 parameter ----------
        val_k2[3] = val_k2[3][:-1]
        if val_k2[3].startswith('?'):
            logging.info('Third2 parameter variable')
            t32 = val_k2[3].strip('?')
            logging.info('?v_t32: %s', str(t32))

            if t32 in var['pred2']:
                logging.info('Matching new t32 with previous pred2...')
                res_s, res_o, res_p2 = intersect_pred(res_s, res_o, res_p2, pred32)
                logging.info('Matching done.')
            elif t32 in var['pred31']:
                logging.info('Matching new t32 with previous pred31...')
                res_s, res_o, res_p31 = intersect_pred(res_s, res_o, res_p31, pred32)
                logging.info('Matching done.')
            elif t32 in var['pred32']:
                logging.info('Matching new t32 with previous pred32...')
                res_s, res_o, res_p32 = intersect_pred(res_s, res_o, res_p32, pred32)
                logging.info('Matching done.')
            else:
                logging.info('Third2 parameter is new.')
                pred32 = trim_dict(res_s, res_o, pred32)
                logging.info('Adding %s to vars.', str(t32))
                var.setdefault('pred32', [])
                var['pred32'].append(t32)
                disp = add_vars_dict(disp, t32, pred32)

                # If first query
                if i == 2:
                    logging.info('First query.')
                    res_p32 = pred32
                    logging.info('Copied curr_pred32 into res_p32')
                else:
                    logging.info('Not first query.')

        elif val_k2[3] == "":
            logging.info('Third2 parameter not needed')
        else:
            logging.info('Third2 parameter given')
            logging.info('Given t32: %s', str(val_k2[3]))

            # Keep matching triples
            if val_k2[3] in pred32:
                res_s, res_o = matchParameter(res_s, res_o, pred32, val_k2[3])
            else:
                logging.info('Given t32 is not in curr_table.')

                res_s = dict()
                res_o = dict()
                res_u = dict()
                res_p1 = dict()
                res_p2 = dict()
                res_p31 = dict()
                res_p32 = dict()
                res_p4 = dict()
                res_u2 = dict()
                logging.info('All res_tables emptied.')

        # Fourth parameter ----------
        if val_k2[4].startswith('?'):
            logging.info('Fourth parameter variable')
            t4 = val_k2[4].strip('?')
            logging.info('?v_t4: %s', str(t4))

            if t4 in var['pred2']:
                logging.info('Matching new t4 with previous pred2...')
                res_s, res_o, res_p2 = intersect_pred(res_s, res_o, res_p2, pred4)
                logging.info('Matching done.')
            elif t4 in var['pred31']:
                logging.info('Matching new t4 with previous pred31...')
                res_s, res_o, res_p31 = intersect_pred(res_s, res_o, res_p31, pred4)
                logging.info('Matching done.')
            elif t4 in var['pred32']:
                logging.info('Matching new t4 with previous pred32...')
                res_s, res_o, res_p32 = intersect_pred(res_s, res_o, res_p32, pred4)
                logging.info('Matching done.')
            elif t4 in var['pred4']:
                logging.info('Matching new t4 with previous pred4...')
                res_s, res_o, res_p4 = intersect_pred(res_s, res_o, res_p4, pred4)
                logging.info('Matching done.')
            else:
                logging.info('Fourth parameter is new.')
                pred4 = trim_dict(res_s, res_o, pred4)
                logging.info('Adding %s to vars.', str(t4))
                var.setdefault('pred4', [])
                var['pred4'].append(t4)
                disp = add_vars_dict(disp, t4, pred4)

                # If first query
                if i == 2:
                    logging.info('First query.')
                    res_p4 = pred4
                    logging.info('Copied curr_pred4 into res_p4')
                else:
                    logging.warning('Not first query.')

        elif val_k2[4] == "":
            logging.info('Fourth parameter not needed')
        else:
            logging.info('Fourth parameter given')
            logging.info('Given t4: %s', str(val_k2[4]))

            # Keep matching triples
            if val_k2[4] in pred4:
                res_s, res_o = matchParameter(res_s, res_o, pred4, val_k2[4])
            else:
                logging.info('Given t4 is not in curr_table.')

                res_s = dict()
                res_o = dict()
                res_u = dict()
                res_p1 = dict()
                res_p2 = dict()
                res_p31 = dict()
                res_p32 = dict()
                res_p4 = dict()
                res_u2 = dict()
                logging.info('All res_tables emptied.')

        logging.info('Predicates parameters processing done.')


        # --------------UID2-PROCESSING--------------
        logging.info('Now, working with uid2.')
        if i == 2:
            logging.info('First query.')

            res_u2 = uid2
            logging.info('Copied curr_uid2 into res_uid2.')
        else:
            logging.info('Query #%d', int(i-1))

        # UID2 Matchings...
        if line[4].startswith('?'):
            logging.info('UID2 is variable.')

            u2 = line[4].strip('?')
            logging.info('?v_uid2: %s', str(u2))

            if u2 in var['sub']:
                logging.info('Matching new UID2 with previous subject...')
                res_s, res_o, res_u2 = matchXYZ(
                    res_s, res_o, res_u2, 1, uid2, 3)
                logging.info('Matching done.')
            elif u2 in var['obj']:
                logging.info('Matching new UID2 with previous object...')
                res_s, res_o, res_u2 = matchXYZ(
                    res_s, res_o, res_u2, 2, uid2, 3)
                logging.info('Matching done.')
            elif u2 in var['uid']:
                logging.info('Matching new UID2 with previous uid...')
                res_s, res_o, res_u2 = matchXYZ(
                    res_s, res_o, res_u2, 3, uid2, 3)
                logging.info('Matching done.')
            elif u2 in var['uid2']:
                logging.info('Matching new UID with previous uid2...')
                res_s, res_o, res_u2 = matchXYZ(
                    res_s, res_o, res_u2, 3, uid2, 3)
                logging.info('Matching done.')
            elif u2 in var['pred']:
                logging.warning('New UID2 matches with previous predicate.')
            else:
                logging.info('UID2 is new.')
                logging.info('Adding %s to vars.', str(u2))
                var.setdefault('uid2', [])
                var['uid2'].append(u2)
                disp = add_vars_dict(disp, u2, uid2)
        else:
            logging.info('UID2 is given.')
            u2 = line[4]
            logging.info('Given u2: %s', str(u2))
            logging.info('Calling matchUID() with given UID2...')
            res_s, res_o, res_u2 = matchUID(res_s, res_o, res_u2, u2)


        # print('Vars in query:', var)
        # print('Current res_s:', res_s)
        # print('Current res_o:', res_o)
        # print('Current res_u:', res_u)
        # print('Current res_u2:', res_u)
        # print('Disp dict:', disp)

        print('Query #'+str(i-1)+' processed.')
        logging.info('Query #%d processed.', (i-1))
        logging.info('-----------------------------')

        i = i + 1

    logging.info('All Queries Processed.')
    logging.info('-----------------------------')

    logging.info('Now preparing display for vars...')

    selects = query[0].split(' ')

    result = prepare_display(selects, var, disp, res_s, res_o, res_u, res_p1, res_p2, res_p31, res_p32, res_p4, res_u2, res_pred)

    logging.info('Done!')
    logging.info('<----------------------------')

    print('\nAll Queries Processed.')
    return result
