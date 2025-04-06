# EPE
A toolkit for making simple parkour game using "Evan's Parkour Engine," All games made must be free for the public to play!
I made the EPE to allow my friends to use the already simplistic engine in an even more simplistic way using a custom compiler that turns EPEScript into ProcessingJS which is injected into the middle of the plain engine and creates a parkour game for you.

Introduction
  The syntax is as simple as I could make it.
  
  One unit in space is 5 pixels.
  One unit of speed is 1 pixel/frame.
  The (x,y) position is the top left corner of a box.
  The player's hitbox is a single point at it's center.
  
  Only the top most box has it's collision be in effect.
  Jumpable boxes have a light outline and have no effect while player is not on the ground.
  Forced boxes constantly have effect no matter the height of the player.
  Solid boxes have collision from the side, meaning they cannot be walked into. These can be forced or jumpable.
  Pad (non-solid) boxes have no side collision stopping the player from entering them, they can effect the player in many ways while they are inside. These can be forced or jumpable.
  Deadly objects kill the player on touch.
  
  There's around two-dozen box types each with 5-6 possible modifiers.
  Some boxes have special values like link codes that link them to other objects, force values to move the player by an amount, and positions to teleport the player to. These values always come right after the box name if the box type requires them.
  Boxes can also change color (they all have defaults), be invisible, move, blinking in and out of existence, or crumble when touched.
  Syntax explained in docs below.

Syntax
  The following are the main types of platforms. (A "~" following the name means it can be made FORCED)
  WALL, HURDLE, PLATFORM, PATH, ERASER, HOLE, VOID, CHECKPOINT~, MUD~, BOOSTER~, TELEPORTER-IN~, TELEPORTER-OUT, TELEPORTER-OUT-A, TELEPORTER-TO~, WORMHOLE~, KEY, ACTIVE-KEY, LOCKED-WALL, LOCKED-ERASER, LOCKED-PLATFORM, ELASTIC-WALL, TRAMPOLINE, CONVEYOR~.

  You want to put the name of the box type, followed by any special value like link codes, force multipliers, or coords.
  (commas are never needed!)
  BOX_TYPE_NAME {SPECIAL_VALUE} (X POSITION, Y POSITION, WIDTH, HEIGHT)

  Now any additional edits can be after, the most simple being "INVISIBLE" which can just be slapped at the end.
  "WALL (10 10 10 10) INVISIBLE" creates a 10x10 wall at (10,10) that you cannot see but has all of its effects.

  Next is "CRUMBLING" which takes one value, which is the time it takes to crumble in frames. It will shrink into nothing once touched and respawn after 5x the crumble time has passed.
  "PLATFORM (10 10 20 20) CRUMBLING (60)" creates a platform that is 20x20 at (10,10) that shrinks into nothing after one second of being touched and reappears after 5 seconds.

  I think you get the gist now, don't you?
  INVISIBLE
  CRUMLING (FRAMES IT TAKES TO CRUMBLE)
  FLICKERING (FRAMES EXISTING, FRAMES MISSING)
  MOVING (X TRAVEL DISTANCE, Y TRAVEL DISTANCE, TURN AROUND TIME)
  COLOR (RED, GREEN, BLUE, OPACITY) or COLOR #COLOR_NAME
  There's the five.
  Flickering exists for FRAMES EXISTING amount of frames before vanishing for FRAMES MISSING amount of frames. It's not just visual, the object literally doesn't exist during MISSING phase.
  Moving objects travel their x and y distance in the time given in frame before turning around and going back at the same rate.
  Color values go from 0-255, and color names can be basic colors or names of platforms. You could make a path that has the color of a hole to trick people with that!

  Finally, all the platform types. (all should have (X POS, Y POS, WIDTH, HEIGHT) after the special value, if it has one, or name.) (Special values seen below will be contained in curly braces)
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

  TRAMPOLINE {STRENGTH} 
  PAD, MAKES YOU JUMP

  ELASTIC-WALL {STRENGTH}
  SOLID, PUSHES YOU BACK, FORCED

  BOOSTER {STRENGTH}
  PAD, ACCELERATES YOU, FORCED?

  CONVEYOR {FORCE} // format the force as "x,y" not "(x,y)" or "x y"
  PAD, PUSHES YOU, FORCED?

  TELEPORTER-TO {POSITION} // format the position as "x,y" not "(x,y)" or "x y"
  PAD, TELEPORTS, FORCED?

  TELEPORTER-IN {LINK CODE}
  PAD, TELEPORTS, FORCED?

  TELEPORTER-OUT {LINK CODE}
  PAD, IS TELEPORTED TO

  TELEPORTER-OUT-A {LINK CODE}
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

What else?
  So there are some more things, such as gamerules that you can change.
  Your .epe file needs to have a <Start> and <End> tag.
  Gamerule setting happens before the <Start>
  Just say (rule name) = (value) on different lines for each rule you want to change from the default.
  Here are the defaults and rules for the less obvious ones:
        TAB_NAME = Evan's Parkour Engine
        DEBUG_MODE = false <<< Allows the use of the debug menu
        PLAYER_STARTING_X_POSITION = 0
        PLAYER_STARTING_Y_POSITION = 0
        GRAVITY_STRENGTH = 1
        PRINT_LAG_SPIKES = false
        SQUISH_DOES_KILL = true <<< should getting stuck kill them?
        OPENING_TEXT = WELCOME <<< the first thing they see
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
  Oh, and comments can be left with "//" or "#"
  Please do enjoy, the EPE is months of work between classes by one guy, me, Evan.

If you want to see an earlier version of the EPE with less platform types as a final product for ideas check out Septomolian Parkour "https://impossibleevan.itch.io/septomolian"
