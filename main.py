import initialconversion
import A_compress_json
import B_create_dicts
import C_user_queries_v36msgpack



# --------------------------------------


def main():

    input_file = './input_files/generated_Rmk.nt'
    
    initialdata=initialconversion.main(input_file)
    
    compressed_data = A_compress_json.main(initialdata)
    
    B_create_dicts.main(compressed_data)

    C_user_queries_v36msgpack.main()

    return


# --------------------------------------

if __name__ == "__main__":
    main()
