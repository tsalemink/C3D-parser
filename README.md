# C3D-parser

### Installing the Python package:

It is recommended that you create a new virtual environment before installing this package, to
avoid any potential dependency conflicts with the packages already installed in your Python
environment.

If you intend to use this package directly from your Python environment you will also need to
install the OpenSim Python distribution yourself. This can be installed using Conda, or by building
the Python bindings from source. Development and testing have been done using Python 3.11 and
OpenSim 4.5, so we recommend installing those releases if possible. Though most recent Python and
OpenSim versions should work as well.

After activating your Python environment and installing OpenSim you can run
`pip install c3d-parser` to install the application. It can then be started by running the command
`c3d_parser`.


### Installing the Windows executable:

The latest release of the C3D-Parser also provides a Windows installer for setting up an executable
version of the application. Simply download and run _C3D-Parser-{release-version}.exe_ for any
release in the GitHub repository [_Releases_](https://github.com/tsalemink/C3D-parser/releases).


### Usage:

To process and analyse a session of gait data, first select your lab's marker-set using the "Lab"
drop-down (if your lab is not shown, or you require a marker set other than the one we provide
please see the section on [custom marker sets](#custom-marker-sets)). Next, select the local gait
session directory using the "Input" line-edit or associated directory chooser, and select a
directory to output the results. Each trial in the session will be automatically classified as
"Static" or "Dynamic", but you can override these classifications by right-clicking on the item
in question. You can exclude specific trials from the analysis by using the check-boxes provided.

Finally, the application also requires a collection of subject information for the processing step,
including height, weight, knee-widths and leg-lengths. This information will be automatically
filled using the metadata contained in your static C3D file, but you should check these values to
make sure they are accurate. Once you are ready, click "Process Data" to begin.

The application will create an OpenSim model using the input data and will run IK and ID. The
results from IK and ID will be displayed in the "Kinematic" and "Kinetic" tabs respectively.
You can select specific gait cycles and can choose to exclude them from the combined, normalised
results that are created at the end of the harmonisation process.

Once the "Harmonise Data" button is pressed, the user exclusions will be considered and the final
output files will be produced. All outputs are written to the user-defined output directory.


### Options:

A number of user settings are available under "View" -> "Options". The "Line Width" option refers
to the width of the lines displayed on the graphs in the visualisation tabs. Both "Data
Directories" define the starting directories used when choosing the "Input" and "Output" paths in
the main window. These settings are retained after you close the application.


### Custom marker sets:

The application pre-defines a number of lab-specific marker sets. If the marker sets we provide do
not fit your needs you can adjust one of the existing marker sets or create a new one from scratch
using the custom marker set dialog under "Marker" -> "Custom Marker Set".

You can import an initial mapping from one of the existing marker sets using the "Import" button.

We recommend that you specify your input session directory (using the "Input" line-edit in the main
window) before opening the custom marker set dialog, this way the drop-down menu associated with
each required marker will be populated with the list of markers defined in your static trial.
Otherwise, you will have to type in the marker names manually, which is time-consuming and prone
to errors. The dialog will also attempt to match any commonly named markers that it identifies in
your static trial.

Your custom marker set must define: "ASI", "KNE", "ANK", "MED", "HEE", either "PSI" or "SACR",
either "KNEM" or "KAX".


### Valid input data:

To be able to create an OpenSim model from your static C3D file, it must contain either: medial
knee markers; or KAD markers as well as knee-width values in the C3D metadata PROCESSING section
(so that we can calculate virtual positions for the medial markers based on the lateral knee marker
positions).

It is recommended that your static C3D file defines the subject's height and weight in the metadata
PROCESSING section, otherwise you will be prompted for this information.

Additionally, to be able to cover a wide range of inputs whilst keep the UI as minimal as possible,
we have had to adopt a fairly strict policy on what is considered a 'valid' gait event. If a foot
strike occurs over multiple force plates, we will be unable to use the GRF data associated with
that stance phase. This will also affect which gait cycles are considered valid when normalising
the results from ID.


### Feature Requests and Bug Reports:
If you would like to suggest a new feature for this application or report a bug you have discovered, please create a
"New Issue" using the appropriate template found in this repository's 
[_Issues_](https://github.com/tsalemink/C3D-parser/issues) page. Please check that your request does not match any 
existing issues.

Ongoing development of features and bug fixes can be tracked using the development 
[_Project_](https://github.com/users/tsalemink/projects/3) for this repository.
