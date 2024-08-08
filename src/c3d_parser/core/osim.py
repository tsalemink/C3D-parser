
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


# TODO: Implement.
def perform_id(osim_file, trc_file, grf_file, output_file):
    with open(output_file, 'w') as file:
        pass
