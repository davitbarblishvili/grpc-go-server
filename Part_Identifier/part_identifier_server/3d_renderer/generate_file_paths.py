import os

def generate_files():
    file_path = []
    dir_path = "/Users/dbarblishvili/go/src/grpc-go-course/Part_Identifier/part_identifier_server/3d_renderer/data/obj"
    for file in os.listdir(dir_path):
        file_path.append(os.path.join(dir_path, file))
    return file_path
