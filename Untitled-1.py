x = """
WALL : color(100),
    STONE : color(100),
    
    ERASER : color(255, 166, 0),
    LAVA : color(255, 166, 0),
    
    HOLE : color(87, 58, 9),
    DIRT : color(87, 58, 9),
    
    VOID : color(-100,-100,-100),
    
    CHECKPOINT : color(117, 235, 106),
    
    MUD : color(107, 87, 52),
    
    ICE : color(135, 232, 227),
    
    BOOSTER : color(224, 224, 97),
    
    TRAMPOLINE : color(164, 70, 214),
    
    TELEPORTER : color(56, 235, 235),
    DIAMOND : color(56, 235, 235),
    
    SULFUR : color(73, 74, 39),
    CONVEYOR : color(73, 74, 39),
    
    LOCKED_PLATFORM : color(194),
    SILVER : color(194),
    
    GOLD : color(255, 213, 0),
    KEY : color(255, 213, 0),
    
    LOCKED_WALL : color(80),
    BASALT : color(80),
    
    LOCKED_ERASER : color(219, 69, 0),
    MAGMA : color(219, 69, 0),
    
    WORMHOLE : color(83, 0, 125),
    OBSIDIAN : color(83, 0, 125),
    
    FAINT : color(128,128,128,20),
    
    TELEPORTER_TO : color(0, 160, 255),
    OCEAN : color(0, 160, 255),
    
    WIN : color(255,240,200),
    AETHER : color(255,240,200),
    
    BLACK : color(0),
    GRAY : color(128),
    WHITE : color(255),
    
    RED : color(255, 0, 0),
    ORANGE : color(255, 128, 0),
    YELLOW : color(255, 255, 0),
    CHART : color(180, 255, 0),
    GREEN : color(0, 255, 0),
    JADE : color(0, 255, 160),
    CYAN : color(0, 255, 255),
    AZURE : color(0, 160, 255),
    BLUE : color(0, 0, 255),
    PURPLE : color(140, 0, 255),
    MAGENTA : color(255, 0, 255),
    ROSE : color(255, 0, 128),
    
    PINK : color(255, 128, 128),
    TAN : color(225, 200, 150),
    BROWN : color(128, 64, 32),"""

try:
    x = x.split("\n")
    with open("colors.txt", "a") as file:
        for i in x:
            i = i.split(":")
            file.write(i[0].strip() + "\n")
            
    input("")
except Exception as e:
    print(e)