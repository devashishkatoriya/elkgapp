
import A_compress_json
import B_create_dicts
import C_user_queries_v33


# --------------------------------------


def main():

    input_file = './input_files/input.json'

    compressed_data = A_compress_json.main(input_file)
    B_create_dicts.main(compressed_data)

    C_user_queries_v33.main()

    return


# --------------------------------------

if __name__ == "__main__":
    main()
