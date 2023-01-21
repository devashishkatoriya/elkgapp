
"""
This file reads dataset from JSON file,
Asks for user query and
Return the result
"""

import os
import csv
import msgpack
import time
import logging

from H_process_query import process_query


# ----------------------------------------


# Function to read data from JSON dictionary
def read_from_json(dict_file):
    """
    Function used to read dataset from input.msgpack file
    """
    logging.info('At read_from_json()')

    with open('./' + dict_file, "rb") as data_file:
        byte_data = data_file.read()
    data = msgpack.unpackb(byte_data)

    logging.info('Read data from %s', dict_file)

    return data


# Function to read predicate dictionary from file
def get_predicate_val(data, pred):
    """
    Function to read predicate dictionary from file
    pred:   Pass the predicate whose dictionary you want
    """

    logging.info('Appending data_dict with %s...', str(pred))

    # Base location of dictionaries.msgpack
    base_file = "./output_files/dictionaries.msgpack"

    # Target predicate dictionary file to read
    filename2 = base_file.split('.msgpack')[0] + "_" + str(pred[1:-1].replace('/', '_').replace(':', '_')) + '.msgpack'

    # Read predicate dictionaries
    val = read_from_json(filename2)

    # Append it to data dictionary
    data.update(val)
    logging.info('Appended.')

    return data


# Function to convert ASK query to select query format
def convert_to_select(query):
    """
    Function to convert ASK query to select query format

    s_query = [
        'SELECT ?x ?i1 ?i2 ?i3 ?i4 ',
        'where {',
        '?x <http://purl.org/biotop/biotop.owl#derivesFrom>[,,(,),] <http://example.org/rdf_Document#D1> ?i1 ?i2 .',
        '?x <http://purl.org/biotop/biotop.owl#derivesFrom>[,,(,),] <o2> ?i3 ?i4 .',
        '}'
    ]
    """
    logging.info('At convert_to_select()')

    s_query = [
        'SELECT ?EMPTY',
        'WHERE {'
    ]

    variables = ""

    i = 1
    while (i <= len(query) - 2):

        line = query[i].split(' ')

        # Skip LIMIT clause
        if line[0].startswith('LIMIT') or line[0].startswith('limit') or line[0].startswith('}'):
            i = i + 1
            continue

        for item in query[i].split(' '):
            if item.startswith('?'):
                variables = variables + " " + str(item)

        s_query.append(query[i])

        i = i + 1

    s_query.append('}')
    s_query[0] = s_query[0] + variables

    logging.info('Converted query: %s', str(s_query))
    return s_query


# Function to write results to csv file
def write_csv_file(filename, result):
    """
    Writes result to csv file.
    """
    logging.info('At write_csv_file()')

    # Create writer for csv
    writer = csv.writer(open(filename, "w"))

    # Append result_vars row-wise
    for key, val in result.items():
        writer.writerow([key, val])

    logging.info('Results.CSV saved to %s', str(filename))

# Function to read query from terminal
def read_query():
    """
    Function to read query from user.
    """
    logging.info('At read_query()')

    query = []

    query = [
        'select ?s ?i ?i2',
        'where {',
        '?s <http://purl.org/biotop/biotop.owl#derivesFrom>[,,(,),] <http://example.org/rdf_Document#D1> ?i ?i2 .',
        '}'#,
        #'LIMIT 100'
    ]

    query = [
        'ASK {',
        '?x <http://purl.org/biotop/biotop.owl#derivesFrom>[,,(,),] <http://example.org/rdf_Document#D1> ?i1 ?i2 .',
        '?x <http://purl.org/biotop/biotop.owl#derivesFrom>[,,(,),] <http://example.org/rdf_Document#D2> ?i3 ?i4 .',
        '}'
    ]

    '''
    print('\nEnter your query:-\n')
    for line in iter(input, eoq):
        query.append(line)
    '''

    logging.info('User entered query: %s', str(query))

    return query


# Sort function
def bubble_sort(query, arr):
    """
    Simple bubble sort function to sort user queries.
    """
    logging.info('At bubble_sort()')

    for _ in range(0, len(arr)):
        for j in range(0, len(arr) - 1):
            if arr[j] > arr[j + 1]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp

                temp = query[j + 2]
                query[j + 2] = query[j + 3]
                query[j + 3] = temp

    logging.info('Bubble sorted.')

    return query


# Function to sort queries
def sort_queries(query, data):
    """
    Driver function for bubble sort.
    """

    # Create empty weights array
    arr = []
    for i in range(0, len(query) - 3):
        arr.append(0)

    print()
    logging.info('At sort_queries()')

    i = 2
    while i <= len(query) - 2:
        line = query[i].split(' ')

        # If not LIMIT or end of queries
        if line[0].startswith('LIMIT') or line[0].startswith('limit') or line[0].startswith('}'):
            arr[i-2] = 99999
            i = i + 1
            continue

        # When predicate is given
        if not line[1].startswith('?'):
            # logging.info('Predicate is given')
            val_k = line[1].split('[')

            if val_k[0] not in data:
                print('Loading data for', val_k[0])
                data = get_predicate_val(data, val_k[0])

            val = data[val_k[0]]
            arr[i-2] = len(val)
        else:
            # logging.info('Predicate is variable')
            arr[i-2] = 99999

        i = i + 1

    # Sort the queries using assigned weights
    query = bubble_sort(query, arr)

    print('Queries Sorted.')
    logging.info('Queries sorted: %s', str(query))

    return query


def check_limits(query, result):
    """
    Function to check if LIMIT is given in user query.
    If yes, removes extra triples from result.
    """

    logging.info('Checking for LIMIT...')

    # Position of LIMIT clause in user given query
    i = len(query) - 1

    # When LIMIT clause is given
    if query[i].startswith('LIMIT') or query[i].startswith('limit'):

        # Extract number of rows to limit
        n = int(query[i].split(' ')[1])
        logging.info('Got n = %d', n)

        # Remove extra rows
        for key in result:
            result[key] = result[key][:n]
    else:
        logging.info('User query does not contain LIMIT')

    logging.info('LIMIT processed.')
    return result


# Function to insert into data
def insert():
    """
    Function used to insert a triple into dataset.
    """

    logging.info('---------------------------->')
    logging.info('At insert()')

    # Location of output directory dictionary file
    base_file = "./output_files/dictionaries.msgpack"

    # Default values
    s1 = p1 = o1 = u1 = u2 = "-"
    t1 = -1.0
    t2 = t31 = t32 = t4 = -1

    # Read triple from user
    print('\nEnter the triple:-\n')

    ch = 'n'
    while ch != 'y':
        s1 = str(input('Enter subject:'))
        p1 = str(input('Enter predicate:'))
        o1 = str(input('Enter object:'))
        u1 = str(input('Enter uid:'))
        t1 = str(float(input('Enter param1:')))
        t2 = str(int(input('Enter param2:')))
        t31 = str(int(input('Enter param31:')))
        t32 = str(int(input('Enter param32:')))
        t4 = str(int(input('Enter param4:')))
        u2 = str(input('Enter uid2:'))

        # User confirmation
        ch = input('\nConfirm adding above triple (y/n): ')
    logging.info('Got s1: %s', s1)
    logging.info('Got p1: %s', p1)
    logging.info('Got o1: %s', o1)
    logging.info('Got u1: %s', u1)
    logging.info('Got t1: %s', t1)
    logging.info('Got t2: %s', t2)
    logging.info('Got t31: %s', t31)
    logging.info('Got t32: %s', t32)
    logging.info('Got t4: %s', t4)
    logging.info('Got u2: %s', u2)

    # Infer file name of predicate dictionary
    pred_file = base_file.split('.msgpack')[0] + "_" + str(p1[1:-1].replace('/', '_').replace(':', '_')) + '.msgpack'
    logging.info('Pred file will be: %s', pred_file)

    # Create empty dictionaries
    pred = dict()

    sub = dict()
    obj = dict()
    uid = dict()
    uid2 = dict()
    pred1 = dict()
    pred2 = dict()
    pred31 = dict()
    pred32 = dict()
    pred4 = dict()

    # Check if predicate dictionary alread exists
    if os.path.isfile(pred_file):
        logging.info('Predicate dictionary file exists.')

        # Read previous predicate file
        data = read_from_json(pred_file)

        # Read dictionaries of the file
        sub = data[p1][0]
        obj = data[p1][1]
        uid = data[p1][2]
        pred1 = data[p1][3]
        pred2 = data[p1][4]
        pred31 = data[p1][5]
        pred32 = data[p1][6]
        pred4 = data[p1][7]
        uid2 = data[p1][8]
    else:
        logging.info('Pred file does not exist.')

    ### Add new triple into predicate dictionaries ###
    # Add to subject dict
    if s1 in sub:
        sub[s1][o1] = u1
    else:
        sub[s1] = dict()
        sub[s1][o1] = u1

    # Add to object dict
    if o1 in obj:
        obj[o1][s1] = u1
    else:
        obj[o1] = dict()
        obj[o1][s1] = u1

    # Add to unique-id dict
    if u1 in uid:
        uid[u1][s1] = o1
    else:
        uid[u1] = dict()
        uid[u1][s1] = o1

    # Add to pred1-dictionary
    if t1 in pred1:
        if s1 in pred1[t1]:
            pred1[t1][s1] = pred1[t1][s1] + [o1]
        else:
            pred1[t1][s1] = [o1]
    else:
        pred1[t1] = dict()
        pred1[t1][s1] = [o1]

    # Add to pred2-dictionary
    if t2 in pred2:
        if s1 in pred2[t2]:
            pred2[t2][s1] = pred2[t2][s1] + [o1]
        else:
            pred2[t2][s1] = [o1]
    else:
        pred2[t2] = dict()
        pred2[t2][s1] = [o1]

    # Add to pred31-dictionary
    if t31 in pred31:
        if s1 in pred31[t31]:
            pred31[t31][s1] = pred31[t31][s1] + [o1]
        else:
            pred31[t31][s1] = [o1]
    else:
        pred31[t31] = dict()
        pred31[t31][s1] = [o1]

    # Add to pred32-dictionary
    if t32 in pred32:
        if s1 in pred32[t32]:
            pred32[t32][s1] = pred32[t32][s1] + [o1]
        else:
            pred32[t32][s1] = [o1]
    else:
        pred32[t32] = dict()
        pred32[t32][s1] = [o1]

    # Add to pred4-dictionary
    if t4 in pred4:
        if s1 in pred4[t4]:
            pred4[t4][s1] = pred4[t4][s1] + [o1]
        else:
            pred4[t4][s1] = [o1]
    else:
        pred4[t4] = dict()
        pred4[t4][s1] = [o1]

    # Add to uid2-dictionary
    if u2 in uid2:
        uid2[u2][s1] = o1
    else:
        uid2[u2] = dict()
        uid2[u2][s1] = o1

    # Add dictionaries to predicate dictionary
    pred[p1] = [sub, obj, uid, pred1, pred2, pred31, pred32, pred4, uid2]

    # Write modified dictionaries to hard disk file
    with open(pred_file, "wb") as outfile:
        packed = msgpack.packb(pred)
        outfile.write(packed)
    logging.info('Predicate %s written.', p1)

    print('Triple added successfully.')

    logging.info('insert() completed.')
    logging.info('<----------------------------')


# Function to convert query to compressed form
def compress_queries(query, indexes):
    """
    Function used to compress user queries as per index_file
    """

    # Check if indexes not in memory
    if indexes == dict():
        print('\nLoading compression indexes...')
        index_file='./output_files/index3.msgpack'
        logging.info('Loading decompression indexes from %s', index_file)
        with open(index_file, "rb") as data_file:
            byte_data = data_file.read()
        indexes = msgpack.unpackb(byte_data)
        logging.info('Loaded.')
        print('Loaded.')

    print('Compressing queries...')

    i = 2
    # For each user query
    while i <= len(query) - 2:
        line = query[i].split(' ')

        if line[0].startswith('LIMIT') or line[0].startswith('limit') or line[0].startswith('}'):
            i = i + 1
            continue

        # Check if sub is given
        if not line[0].startswith('?'):
            line[0] = indexes[line[0]]

        # Check if obj is given
        if not line[2].startswith('?'):
            line[2] = indexes[line[2]]

        # Create new compressed query line
        string = ""
        for k in line:
            string = string + k + " "

        # Replace the original query line
        query[i] = string

        # Move to next query
        i = i + 1

    logging.info('Queries compressed: %s', str(query))
    print('Queries compressed.')

    return query, indexes


# Function to uncompress results using reverse-index json file
def uncompress_result(result, rindexes):
    """
    Function used to uncompress results as per reverse index file

    result {dict}: Compressed result table after processing of query
    rindex_file {str}: Location of reverse index file
    """

    if rindexes == dict():
        print('\nLoading decompression indexes...')
        rindex_file='./output_files/index3r.msgpack'
        logging.info('Loading decompression indexes from %s', rindex_file)
        with open(rindex_file, "rb") as data_file:
            byte_data = data_file.read()
        rindexes = msgpack.unpackb(byte_data)
        print('Loaded.')
        logging.info('Loaded.')

    print('Decompressing results...')
    logging.info('Decompressing results...')

    # Uncompressed result_table
    result2 = dict()

    # For each ?var in res_table
    for key in result:
        result2[key] = []

        # Traverse through compressed results
        for i in result[key]:

            # If empty result, then skip
            if i == '':
                continue

            # Replace entry by uncompressed entry
            if i not in rindexes:
                result2[key].append(str(i))
            else:
                result2[key].append(rindexes[i])

    print('Done.')
    logging.info('Results decompressed.')

    return result2, rindexes


# Function to search from data
def search(data, indexes, rindexes):
    """
    SEARCH function, acts as driver for read_query and process_query
    """

    logging.info('---------------------------->')
    logging.info('At search()')

    # Taking query input from user
    print('\nEnter SELECT Query:-\n')
    query = read_query()
    print('\nGiven query:-\n', query)
    query, indexes = compress_queries(query, indexes)

    # Sort the queries based on predicate dictionary size
    t1 = time.perf_counter()
    query = sort_queries(query, data)
    t2 = time.perf_counter()
    print('\nTime taken to load data (in sec):', (t2-t1))

    # Processing the given query
    print('\nProcessing queries...')
    t3 = time.perf_counter()
    result = process_query(query, data)
    t4 = time.perf_counter()
    print('\nQuery processing done.')
    print('\nTime taken to process SELECT query (in sec):', (t4-t3))
    logging.info('Time taken to process SELECT query (in sec): %f', (t4-t3))

    # Check for and process LIMIT clause
    result = check_limits(query, result)

    # Uncompressing results to human readable form
    t5 = time.perf_counter()
    result, rindexes = uncompress_result(result, rindexes)
    t6 = time.perf_counter()
    print('\nTime taken to uncompress results (in sec):', (t6-t5))
    logging.info('Time taken to uncompress results (in sec): %f', (t6-t5))

    # Ask user if to display results on console
    ch = input('\nDo you want to see results (y/n) ? ')
    if ch in ('y', 'Y'):
        print('\nResult:\n', result)
    logging.info('Results seen: %s', str(ch))

    # Store results to .csv file
    out_csv_file = './output_files/output.csv'
    write_csv_file(out_csv_file, result)
    print('\nResults stored in CSV:', out_csv_file)

    logging.info('<----------------------------')

    return indexes, rindexes


# Function for ASK Query
def ask_query(data, indexes):
    """
    ASK function, acts as driver for read_query and process_query

    query = [
        'ASK {',
        '?x <http://purl.org/biotop/biotop.owl#derivesFrom>[,,(,),] <http://example.org/rdf_Document#D1> ?i1 ?i2 .',
        '?x <http://purl.org/biotop/biotop.owl#derivesFrom>[,,(,),] <o2> ?i3 ?i4 .',
        '}'
    ]
    """

    logging.info('---------------------------->')
    logging.info('At ask_query()')

    # Taking query input from user
    print('\nEnter ASK Query:-\n')
    query = read_query()
    print('\nGiven query:-\n', query)
    query = convert_to_select(query)
    query, indexes = compress_queries(query, indexes)
    query = sort_queries(query, data)

    # Processing the given query
    t3 = time.perf_counter()
    result = process_query(query, data)

    # Check for and process LIMIT clause
    result = check_limits(query, result)

    # Check if result table is non-empty
    ans = False
    for key in result:
        if result[key] != []:
            ans = True
            break

    t4 = time.perf_counter()

    print('\nASK Result:', ans)
    print('\nTime taken to process ASK query (in sec):', (t4-t3))
    logging.info('Time taken to process ASK query (in sec): %f', (t4-t3))

    logging.info('<----------------------------')

    return indexes


# Main Function
def main():
    """
    Main function
    """

    # Log file creation parameters
    logging._srcfile = None
    logging.logThreads = 0
    logging.logProcesses = 0
    logging.basicConfig(
        filename='program_log.log',
        filemode='w',
        format='%(asctime)s:%(levelname)s:%(message)s',
        level=logging.DEBUG
    )
    logging.info('Start.')

    # Create placeholder for predicate dictionaries
    data = dict()
    indexes = dict()
    rindexes = dict()

    while True:
        logging.info('---------------------------->')
        logging.info('At Program Menu.')
        print('\n\n------MENU------')
        print('1 for Insertion.')
        print('2 for SELECT.')
        print('3 for ASK.')
        print('0 to Exit.')
        print('----------------')
        choice = int(input('Enter your choice: '))

        logging.info('Selected choice: %s', str(choice))

        if choice == 1:
            insert()
        elif choice == 2:
            indexes, rindexes = search(data, indexes, rindexes)
        elif choice == 3:
            indexes = ask_query(data, indexes)
        elif choice == 0:
            print('\n\nThank you!')
            break
        else:
            print('Invalid option.')

    logging.info('Exit.')
    logging.info('<----------------------------')

# ----------------------------------------


if __name__ == '__main__':
    main()
