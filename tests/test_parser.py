
import os

from trc import TRCData

from c3d_parser import de_identify_c3d


if __name__ == "__main__":
    data_directory = os.path.abspath("data")
    output_directory = os.path.abspath("output")

    for subdir, dirs, files in os.walk(data_directory):

        # Temporarily skip "general" directory.
        if subdir == os.path.join(data_directory, "general"):
            continue

        for file in files:
            c3d_path = os.path.abspath(os.path.join(subdir, file))
            c3d_file_name = os.path.splitext(os.path.basename(c3d_path))[0]

            # De-identify the C3D data.
            de_identify_c3d(c3d_path, output_directory)

            # Extract TRC data from C3D file.
            trc_data = TRCData()
            trc_data.import_from(c3d_path)
            trc_file_path = os.path.join(output_directory, f"{c3d_file_name}.trc")
            trc_data.save(trc_file_path)
