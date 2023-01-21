
"""
File to create dicts() from JSON file -- Pre-Processing
"""

import msgpack
import time
from tqdm import tqdm


# --------------------------------------


# Utility function to create current sub, obj and uid dicts
def create_dicts(val):
    """
    Function to generate dictionaries for a single predicate
    """

    sub = dict()
    obj = dict()
    uid = dict()
    pred1 = dict()
    pred2 = dict()
    pred31 = dict()
    pred32 = dict()
    pred4 = dict()
    uid2 = dict()

    for i, _ in tqdm(enumerate(val)):

        '''if i % 10000 == 0:
            print('.')'''

        k = val[i]

        s1 = str(k[0])
        o1 = str(k[1])
        u1 = str(k[2])

        t1 = str(k[3])
        t2 = str(int(k[4]))
        t31 = str(int(k[5]))
        t32 = str(int(k[6]))
        u2 = str(k[7])

        

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
        if u1 != "0":
            if u1 in uid:
                uid[u1][s1] = o1
            else:
                uid[u1] = dict()
                uid[u1][s1] = o1

        # Add to pred1-dictionary
        if t1 != "-1":
            
            if t1 in pred1:
                if s1 in pred1[t1]:
                    pred1[t1][s1] = pred1[t1][s1] + [o1]
                else:
                    pred1[t1][s1] = [o1]
            else:
                pred1[t1] = dict()
                pred1[t1][s1] = [o1]

        # Add to pred2-dictionary
        if t2 != "-1":
            if t2 in pred2:
                if s1 in pred2[t2]:
                    pred2[t2][s1] = pred2[t2][s1] + [o1]
                else:
                    pred2[t2][s1] = [o1]
            else:
                pred2[t2] = dict()
                pred2[t2][s1] = [o1]

        # Add to pred31-dictionary
        if t31 != "-1":
            if t31 in pred31:
                if s1 in pred31[t31]:
                    pred31[t31][s1] = pred31[t31][s1] + [o1]
                else:
                    pred31[t31][s1] = [o1]
            else:
                pred31[t31] = dict()
                pred31[t31][s1] = [o1]

        # Add to pred32-dictionary
        if t32 != "-1":
            if t32 in pred32:
                if s1 in pred32[t32]:
                    pred32[t32][s1] = pred32[t32][s1] + [o1]
                else:
                    pred32[t32][s1] = [o1]
            else:
                pred32[t32] = dict()
                pred32[t32][s1] = [o1]

        # Add to pred4-dictionary
        '''if t4 in pred4:
            if s1 in pred4[t4]:
                pred4[t4][s1] = pred4[t4][s1] + [o1]
            else:
                pred4[t4][s1] = [o1]
        else:
            pred4[t4] = dict()
            pred4[t4][s1] = [o1]'''

        # Add to uid2-dictionary
        if u2 != "0":
            if u2 in uid2:
                uid2[u2][s1] = o1
            else:
                uid2[u2] = dict()
                uid2[u2][s1] = o1

    return sub, obj, uid, pred1, pred2, pred31, pred32, uid2


# Main Function
def main(data, base_file="./output_files/dictionaries.msgpack"):
    """Main function to create separate dicts from filename.msgpack
    These dicts are also stored in filename2.msgpack for future use (if req.)

    Keyword Arguments:
        data {dict} -- Data containing compressed predicates)
        base_file {str} -- File to store dicts (default: {'./output_files/dictionaries.msgpack'})

    Returns:
        None
    """

    predicate = dict()

    # Start time
    t1 = time.process_time()

    print('Creating dicts...')

    # Iterate over each predicate
    for key in tqdm(data):

        predicate = dict()

        val = data[key]
        sub, obj, uid, pred1, pred2, pred31, pred32, uid2 = create_dicts(val)
        predicate[key] = [sub, obj, uid, pred1, pred2, pred31, pred32,  uid2]

        # Write predicate into unique JSON file
        filename2 = base_file.split('.msgpack')[0] + "_" + str(key[1:-1].replace('/', '_').replace(':', '_')) + '.msgpack'
        with open(filename2, "wb") as outfile:
            packed = msgpack.packb(predicate)
            outfile.write(packed)
        print(key, 'written.')

    # End time
    t2 = time.process_time()

    print('Done.')
    print('Time taken for creating dictionaries:', (t2-t1))
    print()


# -----------------------------------

if __name__ == "__main__":
    print('---------This file will not run independently---------')
    main()
