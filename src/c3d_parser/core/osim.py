
import os
import copy
import opensim as osim
import xml.etree.ElementTree as ET


osim_resources = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'osim_resources')
EXTERNAL_LOADS_TEMPLATE = ET.parse(os.path.join(osim_resources, 'external_loads_template.xml'))
IK_TASK_SET = os.path.join(osim_resources, 'ik_task_set.xml')


def perform_ik(osim_file, trc_file, output_file):
    model = osim.Model(osim_file)
    model.initSystem()

    ik_tool = osim.InverseKinematicsTool()
    ik_tool.setModel(model)
    ik_tool.setMarkerDataFileName(trc_file)
    ik_tool.set_IKTaskSet(osim.IKTaskSet(IK_TASK_SET))
    ik_tool.setOutputMotionFileName(output_file)
    ik_tool.set_report_errors(False)
    ik_tool.run()


def perform_id(osim_file, ik_file, grf_file, output_file):
    output_directory, output_file_name = os.path.split(output_file)
    external_loads_file = setup_external_loads(output_directory, grf_file)
    time_values = osim.TimeSeriesTable(ik_file).getIndependentColumn()

    model = osim.Model(osim_file)
    model.initSystem()

    id_tool = osim.InverseDynamicsTool()
    id_tool.setModel(model)
    id_tool.setCoordinatesFileName(ik_file)
    id_tool.setExternalLoadsFileName(external_loads_file)
    id_tool.setResultsDir(output_directory)
    id_tool.setOutputGenForceFileName(output_file_name)
    id_tool.setLowpassCutoffFrequency(6)
    id_tool.setStartTime(time_values[0])
    id_tool.setEndTime(time_values[-1])
    id_tool.run()

    os.remove(external_loads_file)


def setup_external_loads(output_directory, grf_file):
    grf_file_path = os.path.abspath(grf_file)
    grf_file_name = os.path.basename(grf_file)
    external_loads_file = os.path.join(output_directory, 'external_loads.xml')

    root = copy.deepcopy(EXTERNAL_LOADS_TEMPLATE.getroot())
    root.find("./ExternalLoads/datafile").text = grf_file_path
    root.find("./ExternalLoads/objects/ExternalForce[@name='externalforce_l']/data_source_name").text = grf_file_name
    root.find("./ExternalLoads/objects/ExternalForce[@name='externalforce_r']/data_source_name").text = grf_file_name

    tree = ET.ElementTree(root)
    tree.write(external_loads_file)

    return external_loads_file
