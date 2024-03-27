
import os

from c3d_parser import read_c3d


if __name__ == "__main__":
    c3d_file = "data/Static01.c3d"
    file_path = os.path.abspath(c3d_file)
    c3d_data = read_c3d(file_path)
