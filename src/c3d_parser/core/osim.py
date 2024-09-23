
import os
import opensim as osim


# TODO: Implement.
def scale_model():
    pass


def perform_ik(osim_file, trc_file, output_file):
    model = osim.Model(osim_file)
    model.initSystem()

    ik_tool = osim.InverseKinematicsTool()
    ik_tool.setModel(model)
    ik_tool.setMarkerDataFileName(trc_file)
    ik_tool.setOutputMotionFileName(output_file)
    ik_tool.run()


# TODO: Include GRF input.
def perform_id(osim_file, ik_file, grf_file, output_file):
    output_directory, output_file_name = os.path.split(output_file)

    model = osim.Model(osim_file)
    model.initSystem()

    id_tool = osim.InverseDynamicsTool()
    id_tool.setModel(model)
    id_tool.setCoordinatesFileName(ik_file)
    id_tool.setResultsDir(output_directory)
    id_tool.setOutputGenForceFileName(output_file_name)
    id_tool.run()
