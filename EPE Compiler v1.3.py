import os
import re


"""
A compiler built for Evan's Parkour Engine (EPE), a custom engine for simple parkour games.
This script is also made by Evan, the creator of EPE.
The engine itself is written in ProcessingJS, a JavaScript library that allows for easy drawing and animation.
Whilst this script is written in Python, it compiles EPE files into a format that can be used by the engine.
And attached in this folder is the "EPE Editor.html" file, which allows you to get some EPE script basics made with a game-engine style environment.


|--- Version History ---|
| 
| -- v1.0 --
| Set up everything, added basic functions and parsing.
| 
| -- v1.1 --
| Added support for OFFSET and ORIGIN commands, which allow for easy mass movement of objects.
| 
| -- v1.2 --
| Added Wormhole and ForcedWormhole since it was somehow missing.
| 
| -- v1.3 --
| Added a ton of new possible alt-names for box types. My favorite are "ENTRANCE", "EXIT", "PUSHER", "MEANY", and "V" which are all useful or funny.
| Added support for boxify() and FloorEllipse type, which allows for easy creation of custom box objects.
|
|-----------------------|

"""

def cap(string: str) -> str:
    if string:
        return string[0].upper() + string[1:].lower()
    return string

def collapse(value: str) -> str:
    if value != None:
        return str(value)
    return ""

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
            if ";" in line:
                # If the line contains a semicolon, split it and add each part to the list
                parts = line.split(";")
                for part in parts:
                    if part.strip():
                        lines.append(part.strip() + ";")
            else:
                lines.append(line.strip())

    return lines

"""
EPE File Syntax:

GAME_RULE_1_NAME = VALUE_1
GAME_RULE_2_NAME = VALUE_2
GAME_RULE_N_NAME = VALUE_N

<START>
OBJECT (X_POSITION, Y_POSITION, WIDTH, HEIGHT)
COLOR (RED, GREEN, BLUE, OPACITY)
MOVING (HORIZONTAL_DISTANCE, VERTICAL_DISTANCE, SPEED)
BLINKING (EXIST_TIME, MISSING_TIME)
COLLAPSING (TIME_TO_COLLAPSE)
<END>

"""

def boxify(line: str) -> str:
    """ Converts a line with BOX properties into a type that can be used in the EPE engine."""
    # One part of the EPE is custom box objects, which are defined as [*Properties] BOX (X, Y, WIDTH, HEIGHT)
    # So basically this function will convert the properties into a type to be used in the EPE engine.

    try:

        line.replace("PAD", "JUMPABLE NONSOLID")  # Convert PAD to JUMPABLE NONSOLID for compatibility
        line.replace("ZONE", "FORCED NONSOLID")  # Convert ZONE to JUMPABLE NONSOLID for compatibility

        # first get the properties
        properties:list[str] = line.split("BOX")[0].strip().split(" ")
        props:list[str] = [prop for prop in properties if prop]  # Remove empty strings

        isLethal = any(keyword in props for keyword in ["DEADLY", "LETHAL", "KILLER", "DEATH", "DANGER", "DANGEROUS", "HURTFUL"])
        if isLethal and any(keyword in props for keyword in ["SAFE", "NONLETHAL"]):
            raise Exception("Cannot be both lethal and non-lethal at the same time.")

        isSolid = any(keyword in props for keyword in ["SOLID", "COLLISION", "BLOCK", "HARD", "UNPASSABLE"])
        if isSolid and any(keyword in props for keyword in ["NONSOLID", "SOFT"]):
            raise Exception("Cannot be both solid and non-solid at the same time.")
        
        isJumpable = any(keyword in props for keyword in ["JUMPABLE", "NONFORCED", "UNFORCED", "SHORT"])
        if isJumpable and any(keyword in props for keyword in ["FORCED", "TALL"]):
            raise Exception("Cannot be both jumpable and forced at the same time.")
        
        isBlack = any(keyword in props for keyword in ["BLACK", "DARK"])
        
        secondHalf = line.split("BOX")[1].strip()
        if not isLethal:
            if isSolid and isJumpable:
                return "HURDLE" + secondHalf  # Hurdle is a solid, jumpable object
            elif isSolid and not isJumpable:
                return "WALL" + secondHalf
            elif not isSolid and isJumpable:
                return "PLATFORM" + secondHalf
            elif not isSolid and not isJumpable:
                return "PATH" + secondHalf
        elif isLethal:
            if isSolid:
                return "ERASER" + secondHalf
            elif not isSolid:
                if isBlack:
                    return "VOID" + secondHalf
                return "HOLE" + secondHalf
            
        raise Exception("Invalid combination of properties. Please check the properties used in the BOX definition.")

    except Exception as e:
        print(f"Error trying to boxify line: {line}. Error: {e}")
        # Return all things as "Template" so it doesn't break the code by replacing everything from "BOX" and before to "Template"
        return "Template" + line.split("BOX")[1]


xoffset = 0
yoffset = 0
def parseEPEline(line: str) -> dict:
    global xoffset, yoffset

    # make any text outside quotes uppercase
    dividedLine = re.split(r'("[^"]*")', line)
    for i in range(len(dividedLine)):
        if i % 2 == 0:
            dividedLine[i] = dividedLine[i].upper()
    line = ''.join(dividedLine)

    if "BOX" in line:
        line = boxify(line)

    if line.startswith("FORCED "):
        line = line.replace("FORCED ", "FORCED")
    elif line.startswith("ACTIVE "):
        line = line.replace("ACTIVE ", "ACTIVE")
    elif line.startswith("LOCKED "):
        line = line.replace("LOCKED ", "LOCKED")
    elif line.startswith("ELASTIC "):
        line = line.replace("ELASTIC ", "ELASTIC")

    # Initialize the dictionary with None or "false" values
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
    time.sleep(0.01)  # Add a small delay for effect, can be removed if not needed
    match type.replace("-", "").replace("_", "").replace("'", "").upper():  # Normalize the type for matching
        case "WALL" | "SOLID" | "BLOCK" | "W" | "STOP":
            return "Wall"
        case "HURDLE" | "HURD" | "SHORTWALL" | "H" | "JUMPABLE":
            return "Hurdle"
        case "PLATFORM" | "PLAT" | "ZONE":
            return "Platform"
        case "PATH" | "PAD" | "WALKY":
            return "Path"
        case "ERASER" | "KILLERWALL" | "DEATHWALL" | "KILLBRICK" | "LAVA" | "E" | "X" | "L" | "OUCH" | "MEANY":
            return "Eraser"
        case "CHECKPOINT" | "SPAWNPOINT" | "SAVEPOINT" | "SAVESPOT" | "CP" | "SP" | "SAVE" | "YIPPEE": 
            return "Checkpoint"
        case "FORCEDCHECKPOINT" | "FORCEDSAVEPOINT" | "FORCEDSPAWNPOINT" | "FORCEDSAVESPOT" | "FCP" | "FYIPPEE":
            return "ForcedCheckpoint"
        case "TELEPORTERIN" | "INTELEPORTER" | "TPIN" | "INTP" | "TPI" | "TELEIN" | "INTELE" | "ENTRANCE":
            return "TeleporterIn"
        case "TELEPORTEROUT" | "OUTTELEPORTER" | "TPOUT" | "OUTTP" | "TPO" | "TELEOUT" | "OUTTELE" | "EXIT" | "EXIT1":
            return "TeleporterOut"
        case "TELEPORTERINFORCED" | "FORCEDTELEPORTERIN" | "FORCEDTPIN" | "FORCEDINTP" | "INTPFORCED" | "TPINFORCED" | "FTPIN" | "FTPI" | "FORCEDINTELE" | "FORCEDTELEIN" | "FORCEDENTRANCE" | "FENTRANCE":
            return "TeleporterInForced"
        case "TELEPORTEROUTA" | "PROPORTIONALTELEPORTEROUT" | "PROPTELEPORTEROUT" | "TPOUTA" | "OUTTPA" | "PROPTPOUT" | "PROPOUTTP" | "TPOA" | "TELEOUTA" | "OUTTELEA" | "EXITA" | "PROPEXIT" | "EXIT2":
            return "TeleporterOutA"
        case "TELEPORTERTO" | "TOTELEPORTER" | "TPTO" | "TP2" | "TT" | "GOTO" | "TELEPORTTO":
            return "TeleporterTo"
        case "WORMHOLE" | "TELEPORTERPAIR" | "LINKEDTELEPORTER" | "WH":
            return "Wormhole"
        case "FORCEDWORMHOLE" | "FORCEDTELEPORTERPAIR" | "FORCEDLINKEDTELEPORTER" | "FWH":
            return "ForcedWormhole"
        case "KEY" | "BUTTON" | "LEVER" | "SWITCH" | "BTN":
            return "Key"
        case "ACTIVEKEY" | "ACTIVEBUTTON" | "ACTIVELEVER" | "ACTIVESWITCH" | "AKEY" | "ABTN" | "ALVR":
            return "ActiveKey"
        case "TRAMPOLINE" | "BOUNCEPAD" | "TRAMP" | "BOUNCE" | "FORCEDTRAMPOLINE" | "FORCEDBOUNCEPAD" | "FORCEDTRAMP" | "FORCEDBOUNCE":
            return "Trampoline"
        case "BOOSTER" | "SPEEDPAD" | "BOOST" | "BSTR":
            return "Booster"
        case "FORCEDBOOSTER" | "FORCEDSPEEDPAD" | "FORCEDBOOST" | "FBSTR":
            return "ForcedBooster"
        case "LOCKEDWALL" | "LOCKEDDOOR" | "DOOR" | "LWALL" | "LDOOR" | "LW":
            return "LockedWall"
        case "LOCKEDERASER" | "LOCKEDKILLERWALL" | "LOCKEDDEATHWALL" | "LOCKEDKILLBRICK" | "LOCKEDLAVA" | "LERASER" | "LKILLER" | "LE":
            return "LockedEraser"
        case "LOCKEDPLATFORM" | "LOCKEDPLAT" | "LPLATFORM" | "LPLAT" | "LP":
            return "LockedPlatform"
        case "ELASTICWALL" | "BOUNCEOFF" | "BOUNCEWALL" | "RUBBER" | "RUBBERWALL" | "BOING" | "BOINGWALL" | "ELASTIC" | "EW":
            return "ElasticWall"
        case "TEXTBOX" | "TEXT":
            return "TextBox"
        case "TEXTTRIGGER" | "MESSAGETRIGGER" | "TRIGGER":
            return "TextTrigger"
        case "MUD" | "QUICKSAND" | "SLOWPAD" | "M":
            return "Mud"
        case "FORCEDMUD" | "FORCEDQUICKSAND" | "SLOWZONE" | "FMUD" | "FM":
            return "ForcedMud"
        case "ICE" | "SMOOTHPAD" | "FREEZEPAD" | "FROZEN" | "GLIDE":
            return "Ice"
        case "FORCEDICE" | "SMOOTHZONE" | "FORCEDFROZEN" | "FORCEDGLIDE" | "FREEZEZONE" | "FICE":
            return "ForcedIce"
        case "FLOOR" | "GROUND" | "BASE" | "FLOORING" | "BACKGROUND" | "RECTFLOOR" | "FLOORRECT" | "GROUNDRECT" | "BACKGROUNDRECT" | "RECTBACKGROUND" | "RECT":
            return "Floor"
        case "FLOORELLIPSE" | "RUG" | "OVALFLOOR" | "OVALGROUND" | "OVALBASE" | "OVALFLOORING" | "OVALBACKGROUND" | "FLOOROVAL" | "ELLIPSEFLOOR" | "ELLIPSEGROUND" | "ELLIPSEBASE" | "ELLIPSEFLOORING" | "ELLIPSEBACKGROUND" | "GROUNDELLIPSE" | "BACKGROUNDELLIPSE" | "ELLIPSE" | "OVAL" | "CIRCLE":
            # Handle different variations of floor ellipse
            return "FloorEllipse"
        case "VOID" | "EMPTYSPACE" | "OUTOFBOUNDS" | "DEATHZONE" | "V":
            return "Void"
        case "HOLE" | "PIT" | "LETHALPAD" | "FALL":
            return "Hole"
        case "CONVEYOR" | "CONVEYORBELT" | "PUSHPAD" | "PUSHER":
            return "Conveyor"
        case "FORCEDCONVEYOR" | "FORCEDCONVEYORBELT" | "PUSHZONE" | "FORCEDPUSHPAD" | "FORCEDPUSHER" | "FCONVEYOR" | "FPUSHER":
            return "ForcedConveyor"
        case "WIN" | "FINISH" | "END" | "GOAL":
            return "Win"
        case _:
            if type.startswith("FORCED"):
                return typeToName(type[7:])  # Remove "FORCED" prefix and try again
            return type

def compileEPEline(line:str) -> str:
    if not line or line.strip() == "":
        return ""
    elif  line.startswith('//') or line.startswith('#'):
        return line.replace('#', '//') + "\n"  # Preserve comments in the output, replace # with // for JS compatibility, multiline comments are not supported in this format.
    parsed_line = parseEPEline(line)
    # Check if the line is valid
    if not parsed_line:
        return "" # Return empty string for OFFSET and ORIGIN
    if parsed_line['type'] == None:
        return f"println('invalid line: {line}');\n"
    returned = ""

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
        
        case 'Checkpoint' | 'ForcedCheckpoint' | 'TeleporterIn' | 'TeleporterInForced' | 'TeleporterOut' | 'TeleporterOutA' | 'TextTrigger' | 'Wormhole' | 'ForcedWormhole':
            returned += f'{_type}({_x}, {_y}, {_special}, {_width if _width != None else '16'}, {_height if _height != None else '16'}, {_color});'
        
        case 'Key' | 'ActiveKey':
            returned += f'{_type}({_special}, {_x}, {_y}, {_width if _width != None else '6'}, {_height if _height != None else '6'}, {_color});'
        
        case 'Trampoline' | 'Booster' | 'ForcedBooster' | 'LockedWall' | 'LockedEraser' | 'LockedPlatform' | 'ElasticWall':
            returned += f'{_type}({_special}, {_x}, {_y}, {_width}, {_height}, {_color});'
        
        case 'Conveyor' | 'ForcedConveyor' | 'TeleporterTo' | 'ForcedTeleporterTo':
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
        "TAB_NAME": "",
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

    if not gamerules["TAB_NAME"]:
        gamerules["TAB_NAME"] = input("Please enter a name for the game: ")

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

print("EPE Compiler v1.1")
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
