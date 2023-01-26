# elkgapp
ELKGapp: An Alternative Approach to Represent Multi-dimensional Meta-knowledge in the Web of Data Expert Systems With Applications

File details:
main.py : Main file which calls all modules automatically.
A_compress_json.py : This module compresses input json file to reduce memory footprint
B_create_dicts.py : This module is responsible for pre-processing of data. It creates dictionaries & indexes
C_user_queries.py : This module works on pre-processed data, asks for user query and returns the result. Also gives the option to store result in a file for future use
H_process_query.py : Contains helper functions which are used by C_user_queries.py
H_utility_functions.py : Helper file containing utility functions for processing user query. This file is used by H_process_query.py
