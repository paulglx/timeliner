import platform, os, sys

# Check arguments

if len(sys.argv) < 2:
    print("Please provide a directory as an argument.")
    print("Example: python timeliner.py /Users/john/Movies/MyMovie")
    quit()

# Check if directory exists

if not os.path.isdir(sys.argv[1]):
    print("ERROR: The directory you provided doesn't exist.")
    quit()

# Check version

ver = platform.python_version_tuple()
if ver != ("2", "7", "18"):
    print(
        "ERROR: Timeliner should be ran using Python 2.7.18. You are using Python "
        + ".".join(ver)
        + "."
    )
    print("Install pyenv and run:")
    print("> pyenv install 2.7.18")
    print("> pyenv shell 2.7.18")
    quit()

##############################################################################

# Project Settings

directory = sys.argv[1]  # This is the directory containing the project folder
name = directory.split("/")[-1]  # This is the name of the project

settings = {
    "timelineFrameRate": 24,
    "timelineResolutionWidth": 1920,  # 1024
    "timelineResolutionHeight": 1080,  # 768
}

addBlanks = True  # Should Timeliner add a transition media between each clip ?
blankFilename = "Black 5s.mp4"  # This file should be in the Resources folder

##############################################################################

try:
    import DaVinciResolveScript as dvr_script
except ImportError:
    print("Please set the environment variables.")
    print("Run the following commands in the terminal:")

    if platform.system() == "Windows":
        print(
            """
set RESOLVE_SCRIPT_API="%PROGRAMDATA%\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\"
set RESOLVE_SCRIPT_LIB="C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll"
set PYTHONPATH="%PYTHONPATH%;%RESOLVE_SCRIPT_API%\\Modules\\"
"""
        )
    elif platform.system() == "Linux":
        print(
            """
RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting/"
RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/\""""
        )
    else:
        print(
            """
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/\""""
        )
    quit()


# Boilerplate
resolve = dvr_script.scriptapp("Resolve")
try:
    fusion = resolve.Fusion()
except:
    print("[ERROR] DaVinci Resolve isn't running.")
    print("Please launch DaVinci Resolve, open a new project and try again.")
    quit()
projectManager = resolve.GetProjectManager()

# Create project
projectManager.CreateProject(name + " (Timeliner)")
project = projectManager.GetCurrentProject()
for setting in settings:
    project.SetSetting(setting, settings[setting])

# Import Media
mediaPool = project.GetMediaPool()
mediaStorage = resolve.GetMediaStorage()

# Create Timeline
tl = mediaPool.CreateEmptyTimeline(name + " Timeline (Generated)")
timeline = project.GetTimelineByIndex(1)
project.SetCurrentTimeline(timeline)

# Sort files by prefix number
filenames = os.listdir(directory)
filenames = [
    f for f in filenames if f[0] != "."
]  # ignore files starting with . (such as .DS_STORE, etc)
sortedFilenames = sorted(filenames, key=lambda x: int(x.split(" ")[0]))
filePaths = [os.path.join(directory, filename) for filename in sortedFilenames]

# Get blank file to add between clips
blankFilePath = os.path.join(os.getcwd(), "Resources", blankFilename)

# Add clips to timeline, with blanks in between
if addBlanks:
    blankClip = mediaStorage.AddItemsToMediaPool(blankFilePath)
for file in filePaths:
    print(file)
    clip = mediaStorage.AddItemsToMediaPool(file)
    mediaPool.AppendToTimeline(clip)
    if addBlanks:
        if 1 in blankClip:
            blankClip[1].SetClipColor("Pink")
        else:
            print(
                "WARNING: Delete all files from media pool before running script. Your changes probably won't be saved."
            )
        mediaPool.AppendToTimeline(blankClip)
