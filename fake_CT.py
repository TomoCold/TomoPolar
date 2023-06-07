# Classes only used  for easy development

class XRaySource:
    """XRaySource parameters"""
    IsHVOn = None  # Xray state. True is on. False for off
    Current = 100  # Tube current in muA
    Voltage = 60  # Tube voltage in kV
    IsCurrentStable = True  # Stability of current. True is stable. False is unstable
    IsVoltageStable = True  # Stability of voltage. True is stable. False is unstable
    IsInterlockClosed = True  # Door closed. True is closed. False is open
    WarmUp = False  # Is warm-up running? True is running. False is not running
    WarmUpRequired = False  # Is warm-up required. True is yes. False is no.

    @classmethod
    def HVOn(cls):
        """Switches X-ray on"""
        pass

    @classmethod
    def HVOn(cls, timeout):
        """Switches X-ray on and waits for stable condition (timeout in s)"""
        pass

    @classmethod
    def HVOff(cls):
        """Switches X-ray off"""
        pass

    def HVOff(cls, timeout):
        """Switches X-ray off and waits for stable condition (timeout in s)"""
        pass

    @classmethod
    def SetCurrent(cls, current):
        """Set current in muA"""
        pass

    @classmethod
    def SetVoltage(cls, voltage):
        """Set voltage in kV"""
        pass

    @classmethod
    def DoWarmUp(cls):
        """Start warm-up procedure"""
        pass

    @classmethod
    def GetFocusModes(cls):
        """
        Return string array of focus modes
        ("Small spot (8µm)", "Middle Spot (20µm)", "Large Spot (40µm)"
        """
        pass

    @classmethod
    def SetFocusMode(cls, focusMode):
        """Set focus mode (only "Small spot (8µm)" possible) """
        pass


class XRayDetector:
    """X-ray detector configuration"""
    ImageWidth = 2464  # image width in pixel
    ImageHeight = 2960  # image height in pixel
    Averages = 1  # number of averaged frames
    PixelSize = 100  # pixel size in microns
    ExposureTime = 0.2  # exposure time in s
    BinningMode = "1x1 Binning"

    @classmethod
    def GetImage(cls, channelIndex):
        """Get image from detector (channelIndex=0)"""
        pass

    @classmethod
    def SetExposureTime(cls, exposure):
        """Set exposure time in s"""
        pass

    @classmethod
    def SetAverages(cls, averages):
        """Set number of average frame"""
        pass

    @classmethod
    def GetBinningModes(cls, binning):
        """Get binning modes ("1x1 Binning", "2x2 Binning", "4x4 Binning)"""
        pass

    @classmethod
    def SetBinningMode(cls, binning):
        """Set binning mode ("1x1 Binning", "2x2 Binning", "4x4 Binning)"""
        pass

    @classmethod
    def SaveAsRaw(cls, savePath, usImg, measParams):
        """Save image usImg in path (str) savePath and associated mesaurement parameters (CTVariables.MeasParams) in
        a raw file """
        pass

    # SaveAsPng(cls, savePath, usImg, measParams) not implemented.

    @classmethod
    def SaveAsTiff(cls, savePath, usImg, measParams):
        """Save image usImg in path (str) savePath and associated measurement parameters (CTVariables.MeasParams) in
        a tiff file """
        pass


class Spec_RotY:
    """Rotation axis of specimen stage"""

    Position = 0  # position angle in degree
    GlobalRefRotX = 0  # Global reference position of RotX in degree
    GlobalRefRotY = 0  # Global reference position of RotY in degree
    GlobalRefRotZ = 0  # Global reference position of RotZ in degree
    GlobalRefX = 0  # Global reference position of axis X in mm
    GlobalRefY = 0  # Global reference position of axis Y in mm
    GlobalRefZ = 0  # Global reference position of axis Z in mm

    @classmethod
    def Move(cls, rot):
        """Move stage to angular position (degree)"""
        pass

    @classmethod
    def MoveAsync(cls, rot):
        """Move stage to angular position (degree) asynchronously"""
        pass

    @classmethod
    def SetVelocity(cls, vel):
        """Set axis velocity (degree/s)"""
        pass


class Spec_TransZ:
    """Zoom axis of specimen stage"""

    Position = 0  # position angle in degree
    GlobalRefRotX = 0  # Global reference position of RotX in degree
    GlobalRefRotY = 0  # Global reference position of RotY in degree
    GlobalRefRotZ = 0  # Global reference position of RotZ in degree
    GlobalRefX = 0  # Global reference position of axis X in mm
    GlobalRefY = 0  # Global reference position of axis Y in mm
    GlobalRefZ = 0  # Global reference position of axis Z in mm

    @classmethod
    def Move(cls, fod):
        """Move to a certain fod (focal-object distance) position (mm)"""
        pass

    @classmethod
    def MoveAsync(cls, fod):
        """Move to a certain fod (focal-object distance) position (mm) asynchronously"""
        pass

    @classmethod
    def SetVelocity(cls, vel):
        """Set axis velocity (mm/s)"""
        pass


class Spec_TransY:
    """Vertical axis of specimen stage"""

    Position = 0  # position angle in degree
    GlobalRefRotX = 0  # Global reference position of RotX in degree
    GlobalRefRotY = 0  # Global reference position of RotY in degree
    GlobalRefRotZ = 0  # Global reference position of RotZ in degree
    GlobalRefX = 0  # Global reference position of axis X in mm
    GlobalRefY = 100  # Global reference position of axis Y in mm
    GlobalRefZ = 0  # Global reference position of axis Z in mm

    # TODO not clear what is the difference with GlobalRef of Spec_RotY

    @classmethod
    def Move(cls, fod):
        """Move to a certain fod (focal-object distance) position (mm)"""
        pass

    @classmethod
    def MoveAsync(cls, fod):
        """Move to a certain fod (focal-object distance) position (mm) asynchronously"""
        pass

    @classmethod
    def SetVelocity(cls, vel):
        """Set axis velocity (mm/s)"""
        pass


class Det_TransZ:
    """Horizontal axis of detector"""

    Position = 0  # position angle in degree
    GlobalRefRotX = 0  # Global reference position of RotX in degree
    GlobalRefRotY = 0  # Global reference position of RotY in degree
    GlobalRefRotZ = 0  # Global reference position of RotZ in degree
    GlobalRefX = 0  # Global reference position of axis X in mm
    GlobalRefY = 0  # Global reference position of axis Y in mm
    GlobalRefZ = 0  # Global reference position of axis Z in mm

    @classmethod
    def Move(cls, fod):
        """Move to a certain fod (focal-object distance) position (mm)"""
        pass

    @classmethod
    def MoveAsync(cls, fod):
        """Move to a certain fod (focal-object distance) position (mm) asynchronously"""
        pass

    @classmethod
    def SetVelocity(cls, vel):
        """Set axis velocity (mm/s)"""
        pass


class CTVariables:
    """Other CT variables"""
    NoLoops = 1  # Get/Set number of loops
    LoopIndex = 1  # Current loop index (the number of steps is not shown by modifying manually in PreProcess)
    NoRepetitions = 1  # Get/Set number of repetitions
    RepetitionIndex = 1  # Current repetition index
    ProjectDirectory = "D:\\scans"  # project directory TODO check if overwrite default name
    Directory = ""  # no explanation by ProCon TODO check
    SampleName = 'A'  # Sample name TODO check if can be replaced afterwards the manually entered name
    MeasParameter = ""  # Measurement parameters (FDD, FOD, tube current, TimeStamp, etc.). What is inside is show
    # with "dir(object)".

