Evan's Parkour Engine (EPE) Version 2.1
by "Impossible" Evan Brockett
(occasionally informal)

A toolkit for making simple bird's-eye-view parkour games using "Evan's Parkour Engine." All games made with this engine must be free for the public to play!
I created the EPE to help my friends easily use the engine with a custom compiler that converts EPEScript into ProcessingJS, generating a parkour game.

Introduction
  The syntax is as simple as I could make it.
  
  One unit in space is 5 pixels.
  One unit of speed is 1 pixel/frame.
  The (x,y) position is the top left corner of a box.
  The player's hitbox is a single point at its center.
  
  Jumpable boxes have a light outline and have no effect while player is not on the ground.
  The player can only jump ~50 units with the normal jump.
  Forced boxes constantly have effect no matter the height of the player.
  Solid boxes have collision from the side, meaning they cannot be walked into. These can be forced or jumpable.
  Pad (non-solid) boxes have no side collision stopping the player from entering them, they can effect the player in many ways while they are inside. These can be forced or jumpable.
  Deadly boxes kill the player on touch.
  Only the top most box has it's collision be in effect.
    - Important for overlapping boxes.
    - Extra important for wall-jumping.
      - The player can wall jump on a wall that is higher than the pad below it.
      - If both a wall and pad such as a void or hole share an edge, then attempting a wall jump will kill the player if the deadly pad is added after the solid one.
  
  There's around two-dozen box types each with 5-6 possible modifiers.
  Some boxes have special values like link codes that link them to other boxes, force values to move the player by an amount, and positions to teleport the player to. These values always come right after the box name if the box type requires them.
  Boxes can also change color (they all have defaults), be invisible, move, blinking in and out of existence, or crumble when touched.
  Syntax explained in docs below.

Syntax
  Comments can be added using "//" or "#".
  The following are the main types of boxes. A '~' following the name indicates that the box can be made FORCED, meaning its effect applies regardless of the player's height or position.
  WALL, HURDLE, PLATFORM, PATH, ERASER, HOLE, VOID, CHECKPOINT~, MUD~, BOOSTER~, TELEPORTER-IN~, TELEPORTER-OUT, TELEPORTER-OUT-A, TELEPORTER-TO~, WORMHOLE~, KEY, ACTIVE-KEY, LOCKED-WALL, LOCKED-ERASER, LOCKED-PLATFORM, ELASTIC-WALL, TRAMPOLINE, CONVEYOR~.

  You want to put the name of the box type, followed by any special value like link codes, force multipliers, or coords.
  Commas are not required.
  BOX_TYPE_NAME {SPECIAL_VALUE} (X POSITION, Y POSITION, WIDTH, HEIGHT)

  Now any additional edits can be after, the most simple being "INVISIBLE" which can just be slapped at the end.
  "WALL (10 10 10 10) INVISIBLE" creates a 10x10 wall at (10,10) that you cannot see but has all of its effects.

  Next is "CRUMBLING" which takes one value, which is the time it takes to crumble in frames. It will shrink into nothing once touched and respawn after 5x the crumble time has passed.
  "PLATFORM (10 10 20 20) CRUMBLING (60)" creates a platform that is 20x20 at (10,10) that shrinks into nothing after one second of being touched and reappears after 5 seconds.

  I think you get the gist now, don't you?
  INVISIBLE
  CRUMBLING (FRAMES IT TAKES TO CRUMBLE)
  FLICKERING (FRAMES EXISTING, FRAMES MISSING)
  MOVING (X TRAVEL DISTANCE, Y TRAVEL DISTANCE, TURN AROUND TIME)
  COLOR (RED, GREEN, BLUE, OPACITY) or COLOR (#COLOR_NAME)

  There's the five.

  Crumbling boxes shrink after being interacted with until disappearing for 5x their crumbling time.
  Flickering exists for FRAMES EXISTING amount of frames before vanishing for FRAMES MISSING amount of frames. It's not just visual, the box literally doesn't exist during MISSING phase.
  Moving boxes travel their x and y distance in the time given in frame before turning around and going back at the same rate.
  Color values go from 0-255, and color names can be basic colors or names of boxes. You could make a path that has the color of a hole to trick people with that!
  Here's all color presets (#):
    WALL
    STONE
    ERASER
    LAVA
    HOLE
    DIRT
    VOID
    CHECKPOINT
    MUD
    ICE
    BOOSTER
    TRAMPOLINE
    TELEPORTER
    DIAMOND
    CONVEYOR
    SULFUR
    LOCKED_PLATFORM
    SILVER
    GOLD
    KEY
    LOCKED_WALL
    BASALT
    LOCKED_ERASER
    MAGMA
    WORMHOLE
    OBSIDIAN
    FAINT
    TELEPORTER_TO
    OCEAN
    WIN
    AETHER

    BLACK
    GRAY
    WHITE
    RED
    ORANGE
    YELLOW
    CHART
    GREEN
    JADE
    CYAN
    AZURE
    BLUE
    PURPLE
    MAGENTA
    ROSE
    PINK
    TAN
    BROWN

  Finally, all the box types.
  All should have (X POS, Y POS, WIDTH, HEIGHT) after the special value, if it has one, or name.
  Special values seen below will be contained in curly braces. 
  Any positional special values must be formatted as "x,y" (destination coordinates) not "(x,y)" or "x y" because the parser expects a comma-separated string without spaces or parentheses.
  ("FORCED?" means it can be if specified as a "FORCED____")
  
  WALL
  SOLID, FORCED

  HURDLE
  SOLID, JUMPABLE

  PLATFORM
  PAD, FORCED

  PATH
  PAD, JUMPABLE

  ERASER
  DEADLY, SOLID

  HOLE/VOID
  DEADLY, JUMPABLE

  ICE
  PAD, NO FRICTION, FORCED?

  MUD
  PAD, SLOWS, FORCED?

  CHECKPOINT {MESSAGE} // Message must be inside quotes
  PAD, SETS SPAWN, FORCED?

  TRAMPOLINE {STRENGTH} 
  PAD, MAKES YOU JUMP

  ELASTIC-WALL {STRENGTH}
  SOLID, PUSHES YOU BACK, FORCED

  BOOSTER {STRENGTH} // Strength is a number
  PAD, ACCELERATES YOU, FORCED?

  CONVEYOR {FORCE} // Formatted as a positional value "x,y" according to the above rule.
  PAD, PUSHES YOU, FORCED?

  TELEPORTER-TO {POSITION} // Format position according to the above rule.
  PAD, TELEPORTS, FORCED?

  TELEPORTER-IN {LINK CODE} // Can be shortened many ways
  PAD, TELEPORTS, FORCED?

  TELEPORTER-OUT {LINK CODE} // Can be shortened many ways
  PAD, IS TELEPORTED TO

  TELEPORTER-OUT-A {LINK CODE} // Can be shortened many ways
  PAD, IS TELEPORTED TO, PRESERVES PROPORTIONS OF ENTRANCE

  WORMHOLE {LINK CODE}
  PAD, TELEPORTS TO AND FROM, FORCED?

  KEY {KEY CODE}
  PAD, SWITCHES BETWEEN ON AND OFF WHEN TOUCHED, STARTS NOT PRESSED

  ACTIVE-KEY {KEY CODE}
  PAD, SWITCHES BETWEEN ON AND OFF WHEN TOUCHED, STARTS PRE-PRESSED

  LOCKED-WALL {KEY CODE}
  SOLID (when not active), FORCED

  LOCKED-ERASER {KEY CODE}
  SOLID (when not active), FORCED (when not active), DEADLY

  LOCKED-PLATFORM {KEY CODE}
  PAD (when active, otherwise doesn't have any effect)

Naming convention:
  A lot of these names have alt-names that can be used.
  Like teleporters which can have TELEPORTER, TELE, or TP instead.
  TELEPORTER-TO can become TP2.
  And many others have names that might save you.
  Like: HURDLE -> HURD -> H
  Or the fact that all "FORCED-____"s can use "F-____" instead!
  Also all dashes or undescores do nothing when it comes to names, so feel free to use them or not.
  Suggest names you think should be added if you want, I'll add them if they don't overlap.
  Check typeToName() from the EPE Compiler python script to find all the names for each.

What else?
  So there are some more things, such as gamerules that you can change.
  Your .epe file needs to have a <Start> and <End> tag.
  Gamerule setting happens before the <Start>
  Just say (rule name) = (value) on different lines for each rule you want to change from the default.
  Here are the defaults and rules for the less obvious ones:
        TAB_NAME = "Evan's Parkour Engine"
        DEBUG_MODE = false <<< Allows the use of the debug menu
        PLAYER_STARTING_X_POSITION = 0
        PLAYER_STARTING_Y_POSITION = 0
        GRAVITY_STRENGTH = 1
        PRINT_LAG_SPIKES = false
        SQUISH_DOES_KILL = true <<< should getting stuck kill them?
        OPENING_TEXT = "WELCOME" <<< the first thing they see
        OPENING_TEXT_LIFESPAN = 1000 <<< how long it stays in frames
        PLAYER_SPEED = 1
        DRAW_LINK_CODES = true <<< should keys, locked boxes, teleporters, etc have their link codes shown?
        FULL_SCREEN = true
        WINDOW_WIDTH = window.innerWidth
        WINDOW_HEIGHT = window.innerHeight
        SHOW_TIMER = true <<< do you want the timer in the top right?
        SHOW_DEATHS = true <<< do you want the death count in the top right?
        SHOW_PERFORMANCE = false <<< do you want to see the red-black square that shows framerate?
        SPEED_IS_LIMITED = true <<< elastic walls and boosters can make you really fast, should it be limited to a realistic speed?
  I hope you enjoy using the EPE. It represents months of work completed between classes by its creator, Evan.

Obviously, there is also a built in editor called "EPE Editor.html" included in this folder. Here is how to use it:
  Using the '[' and ']' keys allows you to control the size of a rectangle called the "creator" (you can also use "p" and "o" or even "z" and "x").
  Pressing the 'debug' button in the bottom left allows for a variety of controls.

  'free-cam' -> allows to look around and edit without moving the player.
  'put player' -> puts the player at the location of the free-cam position.
  'copy code' -> copies the .epe formatted code into your clipboard (if it can't, it will be printed) with spots to edit things that are advanced. (anything with a special value) 
  'control selected' -> prints a usage guide and disables player movement.
  'mark line' -> adds a small comment '//marked' to the final outputted script.

  Pressing 'i' allows you to select the shape being hovered over with the mouse. A guide on scaling, moving, and deletion is printed when pressing 'control selected'.
  
  The rest make sense based off their names or you can test them out :3
  It's intended to be used to make single areas, exported, then using OFFSET(X,Y) to place it where needed.
  Also all levels have everything in the editor included in them! The only difference is that DEBUG_MODE is set to true in the editor.

If you want to see an earlier version of the EPE in action, which served as a foundation for the current engine and had fewer box types along with 22 levels for inspiration, check out Septomolian Parkour at "https://impossibleevan.itch.io/septomolian". This earlier project showcases the evolution of ideas that led to the creation of the EPE.

Files included in the repository:
  1. "README.txt": You are reading this right now.
  2. "EPE Compiler.py": The uncompiled script that can compile .epe scripts.
  3. "empty_epe.txt": Includes the raw code for most of the EPE, used by the compiler to append.
  4. "Original Septomolian Parkour.html": A copy of the original game that was made using an early version of the EPE.
  5. "EPE Editor.html": An empty EPE world with debug tools that can create boxes and give you the script with a button.
  6. "(An AI made this from the README).html": I had ChatGPT try and make a level, it sucks, I had to edit a few things, but 90% is by GaPiTer himself. 
  7. "test.epe": A small test script.
  8. "Daily Parkour.epe": The script for a community made level by r/DailyGames.
  9. "Daily Parkour.html": A community made level that will continue to have parts added.
  10. "Box Type Flowchart.png": Tells you the behavior of all box types that have behavior.
