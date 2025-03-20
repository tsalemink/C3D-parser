# C3D-parser

### Installing the Python package:

It is recommended that you create a new virtual environment before installing this package, to
avoid any potential dependency conflicts with the packages already installed in your Python
environment.

If you intend to use this package directly from your Python environment you will also need to
install the OpenSim Python distribution yourself. This can be installed using Conda, or by building
the Python bindings from source.

After activating your Python environment and installing OpenSim you can run
`pip install c3d-parser` to install the application. It can then be started by running the command
`c3d_parser`.

### Installing the Windows executable:

The latest release of the C3D-Parser also provides a Windows installer for setting up an executable
version of the application. Simply download and run _C3D-Parser-{release-version}.exe_ for any
release in the GitHub repository [_Releases_](https://github.com/tsalemink/C3D-parser/releases).

Please note that if you would like to inspect any debugging information while running the
application, you will need to run the application executable from your console. Just locate the
EXE after installation and call it: `{path-to-exe}\C3D-Parser.exe`

### Usage:

To process and analyse a session of gait data, simply select the local session directory using
the "Input" line-edit or associated directory chooser, then click "Parse C3D Data".

The application will create an OpenSim model using the input data and will run IK and ID. The
results from IK and ID will be displayed in the "Kinematic" and "Kinetic" tabs respectively.
The user can select specific gait cycles and can choose to exclude them from the data that will
be uploaded to the database.

Once the "Upload" button is pressed, the user exclusions will be considered and the final output
files will be produced. Currently, all outputs are written to an "_output" directory in the chosen
session directory.
