
import os

from c3d_parser.core.c3d_parser import parse_c3d


if __name__ == "__main__":
    data_directory = os.path.abspath("data")
    output_directory = os.path.abspath("output")

    for subdir, dirs, files in os.walk(data_directory):

        # Temporarily skip "general" directory.
        if subdir == os.path.join(data_directory, "general"):
            continue

        for file in files:
            c3d_path = os.path.abspath(os.path.join(subdir, file))
            parse_c3d(c3d_path, output_directory)
