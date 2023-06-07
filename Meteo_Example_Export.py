# Python Scripting (Python Engine 2.7.7)

# Available Python Libraries:
from fake_CT import XRayDetector, XRaySource, CTVariables, Spec_RotY, Spec_TransY, Spec_TransZ, Det_TransZ

# Day start
# 1) Do warm-up with GUI, if required
# 2) Check tomo settings with GUI (should be always the same, see scan_s). Including gain mode (who cannot be auto
# check after)
# 3) Remove sample from field of view, do a manual calibration with GUI (without OptimizeExposure)
# 4) In script, check operator name.

# For each sample :
# 1) Put the sample in tomo
# 2) Name your sample in script ("YYYYMMDD_SampleHolderName" for sample_name_prefix, and ['1', '2', '3', ...]
# for sample_name_suffix_s
# 3) Check the y_height positions for a given sample holder
# 4) Run script

# Comments
# No live cropping of projections (size 2960 x 2464)
# No script setting of gain mode
# Averages is always 1
# No drift correction except linear
# No automatic overwriting of folders and files (erase manually old unused folder to overwrite)
# TODO preTravelTime setup in CTVariables.MeasParameter ?
# TODO check if FocusMode is an attribute of Source, Velocity of Spec_RotY
# TODO take the time to reach permanent velocity
# TODO do one additional last proj exactly the same as start ?
# TODO check repository existence

# Declare your global variables here:
project_dir = "Z:\\RawTomo"
system_id = "TomoPolar"
operator = "Calonne_Hagenmuller"

# Declare your scan configuration here
scan_s = {
    'sample_name_prefix': "20230605_A_",
    'n_projections': 2960,
    't_prewarm': 60,
    'voltage': 60,
    'current': 100,
    'exposure': 0.3,
    'averages': 1,
    'binning': "1x1 Binning",
    'fod': 200,
    'parking_fod': 350,
    'y_height_s': [100, 110, 200],
    'sample_name_suffix_s': ['1', '2', '3', '4', '5', '6', '7'],
    'start_angle': 0,
    'end_angle': 360,
}


def apply_settings(voltage, current,
                   exposure, averages, binning,
                   fod, y_height_s, start_angle,
                   n_projections):
    """
    Home-made function to set up the initial conditions of a scan.
    """

    print("Setting scan parameters ...")
    XRay_changed = False
    Detector_changed = False
    Spec_changed = False

    # CT Variables
    CTVariables.ProjectDirectory = project_dir
    CTVariables.NoLoops = n_projections

    # Source settings
    if XRaySource.Current != current:
        XRaySource.SetCurrent(current)
        XRay_changed = True

    if XRaySource.Voltage != voltage:
        XRaySource.SetVoltage(voltage)
        XRay_changed = True

    # Detector settings
    if averages != 1:
        raise ValueError("Averages must be 1")
    if XRayDetector.Averages != averages:
        XRayDetector.SetAverages(averages)
        Detector_changed = True

    if XRayDetector.ExposureTime != exposure:
        XRayDetector.SetExposureTime(exposure)
        Detector_changed = True

    if XRayDetector.BinningMode != binning:
        XRayDetector.SetBinningMode(binning)
        Detector_changed = True

    # Stage settings
    if Spec_TransZ.Position != fod:
        Spec_TransZ.Move(fod)
        Spec_changed = True

    if Spec_RotY.Position != start_angle:
        Spec_RotY.Move(start_angle)
        Spec_changed = True

    if Spec_TransY.Position != y_height_s[0]:
        Spec_TransY.Move(y_height_s[0])
        Spec_changed = True

    print('Detector changed:', Detector_changed)
    print('Source changed:', XRay_changed)
    print('Stage changed:', Spec_changed)

    if Detector_changed:
        raise ValueError("The detector settings were changed. Scan aborted. Do a manual calibration and restart "
                         "script.")


def export_settings():
    """
    Export current settings to xml file. Used in X-Aid import.
    """

    path_proj = CTVariables.ProjectDirectory + "\\" + CTVariables.SampleName + '\\Projections\\proj_%04d.raw'
    output = "<?xml version=\"1.0\"?>" + \
             "\n" + \
             "<RecipeConfiguration xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"" + \
             " xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"" + \
             " ConfiguratorVersion=\"1.0.0.0\">" + \
             "\n" + \
             "\t<ProjectDescritpion" + \
             " CtSytemID=\"" + system_id + "\"" + \
             " UserName=\"" + operator + "\"" + \
             " SampleName=\"" + CTVariables.SampleName + "\"" + \
             " TimeStamp=\"" + CTVariables.MeasParameter.TimeStamp + "\"" + \
             " ImageFileSpecifier=\"" + path_proj + "\"" + \
             " Index1Start=\"0\"" + \
             " Index1End=\"2959\"" + \
             " Index2Start=\"0\"" + \
             " Index2End=\"0\"" + \
             " />" + \
             "\n" + \
             "\t<ProjectionDescritpion" + \
             " NumPixelX=\"2960\"" + \
             " NumPixelY=\"2464\"" + \
             " CropLeft= \"0\"" + \
             " CropRight= \"0\"" \
             " CropTop=\"0\"" + \
             " CropBottom=\"0\"" + \
             " PixelSizeX=\"100\"" + \
             " PixelSizeY=\"100\"" + \
             " BitDepth=\"16\"" + \
             " RawHeaderSize=\"2048\"" + \
             " HorizontalShift=\"0\"" + \
             ">" + \
             "\n" + \
             "\t\t<FileFormat>RawUInt16</FileFormat>" + \
             "\n" + \
             "\t</ProjectionDescritpion>" + \
             "\n" + \
             "\t<AxialCTRecipeParameter" + \
             " RecipeName=\"Axial CT\"" + \
             " NoLoops=\"" + CTVariables.NoLoops + "\"" + \
             " FDD=\"" + CTVariables.MeasParameter.FDD + "\"" + \
             " FOD=\"" + CTVariables.MeasParameter.FOD + "\"" + \
             " DoFastScan=\"true\"" + \
             " FastAveraging=\"false\"" + \
             " StartAngle=\"" + CTVariables.MeasParameter.StartAngle + "\"" + \
             " EndAngle=\"" + CTVariables.MeasParameter.EndAngle + "\"" + \
             " PreTravelTime=\"300\"" + \
             " DelayPerStep=\"0\"" + \
             " DriftCorrection=\"false\"" + \
             " RingCorrection=\"false\"" + \
             " />" + \
             "\n" + \
             "\t<Devices>" + \
             "\n" + \
             "\t\t<DetectorConfiguration" + \
             " DeviceID=\"XRayDetector\"" + \
             " ExposureTime=\"" + XRayDetector.ExposureTime + "\"" + \
             " NAverage=\"" + XRayDetector.Averages + "\"" + \
             " BinningMode=\"" + XRayDetector.BinningMode + "\"" + \
             " />" + \
             "\n" + \
             "\t\t<SourceConfiguration" + \
             " DeviceID=\"XRaySource\"" + \
             " Voltage=\"" + XRaySource.Voltage + "\"" + \
             " Current=\"" + XRaySource.Current + "\"" + \
             " FocalSpotMode=\"" + XRaySource.FocusMode + "\"" + \
             " />" + \
             "\n" + \
             "\t\t<StageConfiguration" + \
             " DeviceID=\"Spec_RotY\"" + \
             " Position=\"" + Spec_RotY.Position + "\"" + \
             " Acceleration=\"160\"" + \
             " Velocity=\"" + Spec_RotY.Velocity + "\"" + \
             " />" + \
             "\n" + \
             "\t\t<StageConfiguration" + \
             " DeviceID=\"Det_TransZ\"" + \
             " Position=\"" + Det_TransZ.Position + "\"" + \
             " Acceleration=\"0\"" + \
             " Velocity=\"10\"" + \
             " />" + \
             "\n" + \
             "\t\t<StageConfiguration" + \
             " DeviceID=\"Spec_TransZ\"" + \
             " Position=\"" + Spec_TransZ.Position + "\"" + \
             " Acceleration=\"100\"" + \
             " Velocity=\"10\"" + " />" + \
             "\n" + \
             "\t</Devices>" + \
             "\n" + \
             "</RecipeConfiguration>"

    import xml.dom.minidom
    xml.dom.minidom.parseString(output)
    print(output)


def PreProcessing():
    """
    Define here your preprocessing procedure like HVon, SetCurrent etc.
    """
    # Setting the scan parameters
    apply_settings(**scan_s)

    # Lighting the Xrays
    if not XRaySource.IsHVOn:
        XRaySource.HVOn(scan_s['t_prewarm'])

    # Define how many times NextStep will be called
    CTVariables.NoLoops = len(scan_s['y_height_s'])


def NextStep():
    """
    Handle here your individual CT steps like GetImage(0), SaveImage(), move() etc.
    The function NextStep is called 'CTVariables.NoLoops' times.
    Since this function is made for a regular axial-CT a work-around has to be applied
    in case of individual scans with special movements.
    Make use of loops to conduct multiple scans as shown below.
    """

    CTVariables.SampleName = scan_s['sample_name_prefix'] + scan_s['sample_name_suffix_s'][CTVariables.LoopIndex]

    if Spec_TransZ.Position != scan_s['y_height_s'][CTVariables.LoopIndex]:
        Spec_TransZ.Move(scan_s['y_height_s'][CTVariables.LoopIndex])

    if Spec_RotY.Position != scan_s['start_angle']:
        Spec_RotY.SetVelocity(60)
        Spec_RotY.Move(scan_s['start_angle'])

    velocity = (scan_s['start_angle'] - scan_s['end_angle']) / (scan_s['n_projections'] * scan_s['exposure'])
    Spec_RotY.SetVelocity(velocity)

    for step in range(0, scan_s['n_projections']):
        angle_step_start = Spec_RotY.Position
        print(angle_step_start)
        img = XRayDetector.GetImage(0)
        path = CTVariables.ProjectDirectory + "\\" + CTVariables.SampleName + '\\Projections\\proj_' + str(
            step).zfill(4) + '.raw'
        XRayDetector.SaveAsRaw(path, img, CTVariables.MeasParameter)

    export_settings()
    Spec_RotY.SetVelocity(60)


def PostProcessing():
    """
    Handle here your postprocessing procedure like HVOff, move to start etc.
    """

    print('Switching X-Ray Off')
    XRaySource.HVOff()


def StopCT():
    """
    Handle here your stop procedure.
    Function is called in the case of an error or when the measurement is aborted.
    """
    print('Switching X-Ray Off')
    XRaySource.HVOff()
