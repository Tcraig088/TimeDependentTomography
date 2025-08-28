import enum

# The State of the projection handler
class ProjectionHandlerState(enum.Enum):
    Initialized = 100, 
    Saved = 101,
    Registered = 102,
    
    Checked = 200, 
    NewData = 201,
    ResetRequested = 202,
    SaveRequested = 203
    # TODO possible race condition
    # It is possible new data is added and a save is requested in which case which do you do first?

# The Type of projection being imported
class ProjectionType(str, enum.Enum):
    EMI = 'emi/ser', 
    MRC = 'mrc',
    EDXTXT = 'edx/txt',
    EDXBCF = 'edx/bcf',
    TIFF = 'Tiff'

# The Type of Alignment being performed
class AlignmentType(str, enum.Enum):
    # Tilt Series Alignment
    CCTiltAlign = 'Auto Align - FFT Cross Correlation', 
    
    # Image Manipulation
    Centre = 'Centre Image',
    Square = 'Make Square',
    Resize = 'Resize',
    
    #Background Removal
    BKGSubMedian = 'Background Subtraction',
    
    #Segmentation
    SegOtsu = 'Otsu Segmentation',
    
    #Filters
    FilterGaussian = 'Gaussian Filter'

# The Type of Plugin Being Used
class PluginType(str,enum.Enum):
    BeamDamage = 'Beam Damage Analysis', 
    SignalManipulation = 'Signal Manipulation',
    EDXAnalysis = 'EDX Analysis'

