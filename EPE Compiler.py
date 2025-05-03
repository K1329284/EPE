import os
import re

def cap(string: str) -> str:
    if string:
        return string[0].upper() + string[1:].lower()
    return string

def collapse(value: str) -> str:
    if value != None:
        return str(value)
    return ""

def ternary(expression:bool, trueResult:object, falseResult:object) -> object:
    return trueResult if expression else falseResult

def getEPE() -> list[str]:
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # List all files in the directory and filter for .epe files
    epe_files = [file for file in os.listdir(current_dir) if file.endswith('.epe')]
    return epe_files

def readEPE(file_name:str) -> list[str]:
    with open(os.path.dirname(os.path.abspath(__file__)) + "\\" +file_name, 'r') as file:
        rawlines = file.readlines()

    lines = []
    for line in rawlines:
        # Strip whitespace from the line and check if it's not empty
        if line.strip():
            # Add the line to the compiled lines list
            lines.append(line.strip())

    return lines

"""EPE File Format:

OBJECT (X_POSITION, Y_POSITION, WIDTH, HEIGHT)
COLOR (RED, GREEN, BLUE, OPACITY)
MOVING (HORIZONTAL_DISTANCE, VERTICAL_DISTANCE, SPEED)
BLINKING (EXIST_TIME, MISSING_TIME)
COLLAPSING (TIME_TO_COLLAPSE)

"""

xoffset = 0
yoffset = 0
def parseEPEline(line: str) -> dict:
    global xoffset, yoffset
    
    line = line.upper()
    if line.startswith("FORCED "):
        line = line.replace("FORCED ", "FORCED")
    elif line.startswith("ACTIVE "):
        line = line.replace("ACTIVE ", "ACTIVE")
    elif line.startswith("LOCKED "):
        line = line.replace("LOCKED ", "LOCKED")
    elif line.startswith("Elastic "):
        line = line.replace("Elastic ", "Elastic")

    # Initialize the dictionary with None values
    data = {
        "type": None, "x": None, "y": None, "width": None, "height": None,
        "color": None, "special value": None, "is moving": "false",
        "x travel distance": None, "y travel distance": None, "travel time": None,
        "is flickering": "false", "existing time": None, "missing time": None,
        "is crumbling": "false", "crumble time": None,
        "is invisible": "false"
    }
    
    # Match object type and optional special value
    data["type"] = line.split(" ")[0]
    for section in line.split(" ")[1:]:
        if section.startswith("("):
            break
        if data["special value"] == None:
            data["special value"] = section + " "
        elif section != "":
            data["special value"] += section + " "
    
    # Match (x, y, width, height)
    size_match = re.search(r"\(([^)]*)\)", line)
    if size_match:
        values = re.split(r"[ ,]+", size_match.group(1))
        # For offset values and easy mass movement
        if data["type"] == "OFFSET":
            if len(values) >= 2:
                xoffset += int(values[0])
                yoffset += int(values[1])
            return False  # Return early for OFFSET, as it doesn't need further processing
        if data["type"] == "ORIGIN":
            xoffset = 0
            yoffset = 0
            return False  # Return early for ORIGIN, as it resets offsets
        if len(values) >= 4:
            data["x"], data["y"], data["width"], data["height"] = values[:4]
        elif len(values) >= 3:
            data["x"], data["y"], data["width"] = values[:3]
        elif len(values) >= 2:
            data["x"], data["y"] = values[:2]
    
    # Match COLOR tag
    color_match = re.search(r"COLOR\s*\(([^)]*)\)", line)
    if color_match:
        color_values = re.split(r"[ ,]+", color_match.group(1))
        if color_values[0].startswith("#"):
            data["color"] = f"COLOR.{color_values[0][1:]}"
        else:
            data["color"] = f"color({', '.join(color_values)})"
    
    # Match MOVING tag
    moving_match = re.search(r"MOVING\s*\(([^)]*)\)", line)
    if moving_match:
        data["is moving"] = "true"
        move_values = re.split(r"[ ,]+", moving_match.group(1))
        if len(move_values) >= 3:
            data["x travel distance"], data["y travel distance"], data["travel time"] = move_values[:3]
    
    # Match FLICKERING or BLINKING tag
    flicker_match = re.search(r"(?:FLICKERING|BLINKING)\s*\(([^)]*)\)", line)
    if flicker_match:
        data["is flickering"] = "true"
        flicker_values = re.split(r"[ ,]+", flicker_match.group(1))
        if len(flicker_values) >= 2:
            data["existing time"], data["missing time"] = flicker_values[:2]
    
    # Match CRUMBLING tag
    moving_match = re.search(r"CRUMBLING\s*\(([^)]*)\)", line)
    if moving_match:
        data["is crumbling"] = "true"
        move_values = re.split(r"[ ,]+", moving_match.group(1))
        if len(move_values) >= 1:
            data["crumble time"] = move_values[0]  # Use the first value as crumble time, if available
    
    # Match INVISIBLE tag
    if "INVISIBLE" in line:
        data["is invisible"] = "true"
    
    return data

import time
def typeToName(type:str) -> str:
    print(type.replace("-", "").replace("_", "").replace("'", "").upper())
    time.sleep(0.01)  # Add a small delay to allow for debugging
    match type.replace("-", "").replace("_", "").replace("'", "").upper():  # Normalize the type for matching
        case "WALL":
            return "Wall"
        case "HURDLE" | "HURD":
            return "Hurdle"
        case "PLATFORM" | "PLAT":
            return "Platform"
        case "PATH":
            return "Path"
        case "ERASER" | "KILLERWALL" | "DEATHWALL" | "KILLBRICK" | "LAVA":
            return "Eraser"
        case "CHECKPOINT" | "SPAWNPOINT" | "SAVEPOINT" | "SAVESPOT": 
            return "Checkpoint"
        case "FORCEDCHECKPOINT" | "FORCEDSAVEPOINT" | "FORCEDSPAWNPOINT" | "FORCEDSAVESPOT":
            return "ForcedCheckpoint"
        case "TELEPORTERIN" | "INTELEPORTER" | "TPIN" | "INTP":
            return "TeleporterIn"
        case "TELEPORTEROUT" | "OUTTELEPORTER" | "TPOUT" | "OUTTP":
            return "TeleporterOut"
        case "TELEPORTERINFORCED" | "FORCEDTELEPORTERIN" | "FORCEDTPIN" | "FORCEDINTP" | "INTPFORCED" | "TPINFORCED":
            return "TeleporterInForced"
        case "TELEPORTEROUTA" | "PROPORTIONALTELEPORTEROUT" | "PROPTELEPORTEROUT" | "TPOUTA" | "OUTTPA" | "PROPTPOUT" | "PROPOUTTP":
            return "TeleporterOutA"
        case "TELEPORTERTO" | "TOTELEPORTER":
            return "TeleporterTo"
        case "KEY" | "BUTTON" | "LEVER" | "SWITCH":
            return "Key"
        case "ACTIVEKEY" | "ACTIVEBUTTON" | "ACTIVELEVER" | "ACTIVESWITCH":
            return "ActiveKey"
        case "TRAMPOLINE" | "BOUNCEPAD":
            return "Trampoline"
        case "BOOSTER" | "SPEEDPAD":
            return "Booster"
        case "FORCEDBOOSTER" | "FORCEDSPEEDPAD":
            return "ForcedBooster"
        case "LOCKEDWALL" | "LOCKEDDOOR":
            return "LockedWall"
        case "LOCKEDERASER" | "LOCKEDKILLERWALL":
            return "LockedEraser"
        case "LOCKEDPLATFORM" | "LOCKEDPLAT":
            return "LockedPlatform"
        case "ELASTICWALL" | "BOUNCEWALL" | "RUBBERWALL":
            return "ElasticWall"
        case "TEXTBOX" | "TEXT":
            return "TextBox"
        case "TEXTTRIGGER" | "MESSAGETRIGGER" | "TRIGGER":
            return "TextTrigger"
        case "MUD" | "QUICKSAND" | "SLOWPAD":
            return "Mud"
        case "FORCEDMUD" | "FORCEDQUICKSAND" | "FORCEDSLOWPAD":
            return "ForcedMud"
        case "ICE" | "SMOOTHPAD":
            return "Ice"
        case "FORCEDICE" | "FORCEDSMOOTHPAD":
            return "ForcedIce"
        case "FLOOR" | "GROUND" | "BASE" | "FLOORING" | "BACKGROUND":
            return "Floor"
        case "VOID" | "EMPTYSPACE" | "OUTOFBOUNDS" | "DEATHZONE":
            return "Void"
        case "HOLE" | "PIT":
            return "Hole"
        case "CONVEYOR" | "CONVEYORBELT" | "PUSHPAD":
            return "Conveyor"
        case "FORCEDCONVEYOR" | "FORCEDCONVEYORBELT" | "FORCEDPUSHPAD":
            return "ForcedConveyor"
        case "WIN" | "FINISH":
            return "Win"
        case _:
            return type

def compileEPEline(line:str) -> str:
    if not line or line.strip() == "":
        return ""
    elif  line.startswith('//') or line.startswith('#'):
        return line.replace('#', '//') + "\n"  # Preserve comments in the output, replace # with // for JS compatibility
    parsed_line = parseEPEline(line)
    # Check if the line is valid
    if not parsed_line:
        return "" # Return empty string for OFFSET and ORIGIN
    if parsed_line['type'] == None:
        return f"println('invalid line: {line}');\n"
    returned = ''

    _type = typeToName(parsed_line['type'])
    _x = str(int(parsed_line['x']) + xoffset)
    _y = str(int(parsed_line['y']) + yoffset)
    _width = parsed_line['width']
    _height = parsed_line['height']
    _color = parsed_line['color']
    _special = parsed_line['special value']

    match _type:
        case 'Win' | 'Wall' | 'Hurdle' | 'Platform' | 'Path' | 'Eraser' | 'Hole' | 'Void' | 'Mud' | 'ForcedMud' | 'Ice' | 'ForcedIce' | 'Floor': 
            returned += f'{_type}({_x}, {_y}, {_width}, {_height}, {_color});'
        
        case 'Checkpoint' | 'ForcedCheckpoint' | 'TeleporterIn' | 'TeleporterInForced' | 'TeleporterOut' | 'TeleporterOutA' | 'TextTrigger':
            returned += f'{_type}({_x}, {_y}, {_special}, {_width if _width != None else '16'}, {_height if _height != None else '16'}, {_color});'
        
        case 'Key' | 'ActiveKey':
            returned += f'{_type}({_special}, {_x}, {_y}, {_width if _width != None else '6'}, {_height if _height != None else '6'}, {_color});'
        
        case 'Trampoline' | 'Booster' | 'ForcedBooster' | 'LockedWall' | 'LockedEraser' | 'LockedPlatform' | 'ElasticWall':
            returned += f'{_type}({_special}, {_x}, {_y}, {_width}, {_height}, {_color});'
        
        case 'Conveyor' | 'ForcedConveyor' | 'TeleporterTo' | 'TeleporterFrom':
            returned += f'{_type}({_x}, {_y}, {_width}, {_height}, {_special}, {_color});'
        
        case 'TextBox':
            returned += f'TextBox({_x}, {_y}, {_special}, {_width if _width != None else '20'}, {_color});'
        
        case _:
            returned += f"println('unknown type: ' + '{parsed_line['type']}');"
    
    returned += "\n"

    if parsed_line["is moving"] == "true":
        returned += f"ToMoving3({parsed_line['x travel distance']}, {parsed_line['y travel distance']}, {parsed_line['travel time']});\n"
    if parsed_line["is flickering"] == "true":
        returned += f"ToFlickering({parsed_line['existing time']}, {parsed_line['missing time']});\n"
    if parsed_line["is invisible"] == "true":
        returned += "ToInvisible();\n"
    if parsed_line["is crumbling"] == "true":
        returned += f"ToCrumbling({parsed_line['crumble time']});\n"
    
    return returned

def compileEPE(lines:list[str]) -> str:
    gamerules:dict[str,str] = {
        "TAB_NAME": "Evan's Parkour Engine",
        "DEBUG_MODE" : "false",
        "PLAYER_STARTING_X_POSITION": "0",
        "PLAYER_STARTING_Y_POSITION": "0",
        "GRAVITY_STRENGTH": "1",
        "PRINT_LAG_SPIKES": "false",
        "SQUISH_DOES_KILL": "true",
        "OPENING_TEXT": "WELCOME",
        "OPENING_TEXT_LIFESPAN": "1000",
        "PLAYER_SPEED": "1",
        "DRAW_LINK_CODES": "true",
        "FULL_SCREEN" : "true",  # Allow the game to be fullscreen, this can be overridden by the engine settings
        "WINDOW_WIDTH": "window.innerWidth",
        "WINDOW_HEIGHT": "window.innerHeight",
        "SHOW_TIMER": "true",
        "SHOW_DEATHS": "true",
        "SHOW_PERFORMANCE": "false",
        "SPEED_IS_LIMITED": "true",
    }

    # Gamerule handling
    breakLineIndex = -1
    # find line seperating rules from objects
    for i in range(len(lines)):
        if lines[i].upper() in "<START>":
            breakLineIndex = i
            break

    # Everything before <START> is gamerules, everything after is EPE objects

    for line in lines[:breakLineIndex]:
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            
            if key in gamerules:
                gamerules[key] = value
            else:
                print(f"Gamerule '{key}' not found. Line '{line}' will be ignored.")
                print(f"Gamerule options are {', '.join(gamerules.keys())}.")

    # Compile EPE lines until <END> is found
    compiledLines = ""
    for line in lines[breakLineIndex + 1:]:
        if line.upper() == "<END>":
            break
        else:
            compiledLines += compileEPEline(line)

    print(compiledLines)

    # Everything after <END> is ignored, it can be used for comments or other non-code purposes, but will not be compiled into the final code.

    # Everything after <START> and before <END> is EPE objects, we can now compile them into the final code

    # Add EPE's important code
    # load in empty_epe.html

    # This is a template for the EPE engine, it contains the basic ProcessingJS code for the EPE engine.
    with open(os.path.dirname(os.path.abspath(__file__)) + r"\empty_epe.txt", "r") as file:
        engineCode = file.read()

    # Add the gamerules to the top of the compiled code
    compiledLines = f'''
// Game Rules

// Name your game and put here, and how long its there.
var titleText = "{gamerules["OPENING_TEXT"]}"; var titleTime = {gamerules["OPENING_TEXT_LIFESPAN"]};
var player_starting_x_position = {int(gamerules["PLAYER_STARTING_X_POSITION"])*5};
var player_starting_y_position = {int(gamerules["PLAYER_STARTING_Y_POSITION"])*5};
var print_lag_spikes = {gamerules["PRINT_LAG_SPIKES"]};
var player_walking_speed = {gamerules["PLAYER_SPEED"]};
var gravity_strength = {gamerules["GRAVITY_STRENGTH"]};
var debugMode = {gamerules["DEBUG_MODE"]};
var show_timer = {gamerules["SHOW_TIMER"]};
var show_deaths = {gamerules["SHOW_DEATHS"]};
var show_performance = {gamerules["SHOW_PERFORMANCE"]};
var speed_is_limited = {gamerules["SPEED_IS_LIMITED"]};

// Should the player die when squished by a moving wall?
// If false it pushes the player inside the wall which may cause problems.
var squish_does_kill = {gamerules["SQUISH_DOES_KILL"]};
// Set this to false when you want the players to use trial and error to figure things out or be given what links to.
var do_draw_linking_codes = {gamerules["DRAW_LINK_CODES"]};
''' + engineCode + compiledLines

    # Add HTML wrapping
    compiledLines = f'<!DOCTYPE html><html> <head><title>{gamerules['TAB_NAME']}</title> </head><body><style>' + "#canvas{ position:fixed; left:0; top:0; width:100%; height:100%; } html, body { overflow: hidden; margin: 0 !important; padding: 0 !important; }" + '</style><!--This draws the canvas on the webpage --><canvas id="mycanvas"></canvas></body><!-- Include the processing.js library --><!-- See https://khanacademy.zendesk.com/hc/en-us/articles/202260404-What-parts-of-ProcessingJS-does-Khan-Academy-support- for differences --><script src="https://cdn.jsdelivr.net/processing.js/1.4.8/processing.min.js"></script> <script>var programCode = function(processingInstance)' + '{with (processingInstance) {size(' + gamerules["WINDOW_WIDTH"] + ', ' + gamerules["WINDOW_HEIGHT"] + '); frameRate(60);  ' + compiledLines + '}};var canvas = document.getElementById(\'mycanvas\'); canvas.width = +' + f"{gamerules['WINDOW_WIDTH']}" + '; canvas.width = +' + f"{gamerules['WINDOW_HEIGHT']}" + '; var processingInstance = new Processing(canvas, programCode);</script></html>'

    # Attempt to open the file and write the compiled code to it
    try:
        with open(os.path.dirname(os.path.abspath(__file__)) + "\\" + gamerules["TAB_NAME"] + ".html", "w+") as file:
            file.write(compiledLines)
    except Exception as e:
        return f"FILE_WRITE_ERROR '{e}'"

    return "SUCCESS"

print("EPE Compiler v1.0")
print("EPE (Evan's Parkour Engine) is a custom engine for simple parkour games.")
print("This script will compile EPE files into a format that can be used by the engine.")
print("Please ensure that the EPE files are in the same folder as this script.")

while True:
    print("\nChecking for EPE files...")
    EPEs = getEPE()
    if len(EPEs) == 0:
        print("No EPE files found in folder, please add them into the same folder as this script.")
        input("Press Enter when ready...")
        continue
    elif len(EPEs) == 1:
        print("Do you wish to compile the EPE file? (y/n) FILE: \"" + EPEs[0] + "\"")
        choice = input("Enter y or n: ")
        if choice.lower() == 'y':
            attemptCompile = compileEPE(readEPE(EPEs[0]))
            if attemptCompile == "SUCCESS":
                print("EPE file compiled successfully.")
                break
            else:
                print("EPE file compilation failed. Error code: " + attemptCompile)
                input("Press Enter to try again...")
                continue
        else:
            input("No? Reseting...")
            continue
    else:
        print("Mutliple EPE files found, please select one to compile:")
        for i, file in enumerate(EPEs):
            print(f"{i + 1}: {file}")
        choice = input("Enter the number of the file you wish to compile: ")
        try:
            choice = int(choice) - 1
            if choice < 0 or choice >= len(EPEs):
                raise ValueError("Invalid choice")
        except ValueError:
            print("Invalid input, please enter a number.")
            exit(1)
        print("Do you wish to compile the EPE file? (y/n) FILE: \"" + EPEs[choice] + "\"")
        choice = input("Enter y or n: ")
        if choice.lower() == 'y':
            attemptCompile = compileEPE(readEPE(EPEs[0]))
            if attemptCompile == "SUCCESS":
                print("EPE file compiled successfully.")
                break
            else:
                print("EPE file compilation failed. Error code: " + attemptCompile)
                input("Press Enter to try again...")
                continue
        else:
            input("No? Reseting...")
            continue
input("Press Enter to exit...")
