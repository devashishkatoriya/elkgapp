
# File to compress JSON file using basic indexing

import msgpack
import time
import json


# --------------------------------------


# Function to read data from JSON file
def read_data(filename):
    """Function to read data from JSON file

    Arguments:
        filename {str} -- path of file to read

    Returns:
        data {dict()} -- dictionary inside the file
    """
    with open('./' + filename, 'r') as file:
        data = json.load(file)
    file.close()

    return data


# Main Function
def main(filename, index_file="./output_files/index3.msgpack", r_index_file = "./output_files/index3r.msgpack"):
    """Main Function to compress JSON file
    Creates an index file for future uncompression use

    Keyword Arguments:
        filename {str} -- JSON file to be compressed
        index_file {str} -- path to store index file (default: {"./output_files/index3.msgpack"})
        r_index_file {str} -- path to store reverse-index (default: {"./output_files/index3r.msgpack"})

    Returns:
        data {dict()} -- compressed JSON data
    """

    print('Compressing data...')
    cnt = 3000

    t1 = time.perf_counter()

    # Index dict
    matrix = dict()

    # Reverse Index dict
    matrix2 = dict()

    # Read original data from JSON file
    data = read_data(filename)

    # Progress Counter
    i = 0

    # Iterate over every string
    for key in data:
        for ele in data[key]:

            if i % 10000 == 0:
                print(i)
            i = i + 1

            ele[0] = ele[0].strip()
            if ele[0] not in matrix:
                matrix[ele[0]] = str(cnt)
                matrix2[str(cnt)] = ele[0]
                ele[0] = str(cnt)
                cnt = cnt + 1
            else:
                ele[0] = matrix[ele[0]]

            ele[1] = ele[1].strip()
            if ele[1] not in matrix:
                matrix[ele[1]] = str(cnt)
                matrix2[str(cnt)] = ele[1]
                ele[1] = str(cnt)
                cnt = cnt + 1
            else:
                ele[1] = matrix[ele[1]]

            ele[2] = ele[2].strip()
            if ele[2] not in matrix:
                matrix[ele[2]] = str(cnt)
                matrix2[str(cnt)] = ele[2]
                ele[2] = str(cnt)
                cnt = cnt + 1
            else:
                ele[2] = matrix[ele[2]]

        key = key.strip()
        matrix[key] = key
        matrix2[key] = key

    matrix2["0"] = "0"

    # Write Reverse Index file
    print('Writing reverse-index file...')
    with open(r_index_file, "wb") as outfile:
        packed = msgpack.packb(matrix2)
        outfile.write(packed)

    # Write Index file
    print('Writing index file...')
    with open(index_file, "wb") as outfile:
        packed = msgpack.packb(matrix)
        outfile.write(packed)

    t2 = time.perf_counter()

    print('Done!')
    print('Time taken for compressing:', (t2-t1))
    print()

    return data


# -----------------------------------

if __name__ == "__main__":
    main('./input_files/input.json')
