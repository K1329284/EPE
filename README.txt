This  will  tell  you  the  syntax  to  use  for  the  EPE

There  are  many  types  of  objects.
Each  can  be  defined  by  an  x position, y position, width, and  height.
There  is  also  the  optional  color, invisible, moving, blinking, and other things specific to each platform type.

A standard unit is 5 pixels wide.
Jumpable objects will have a light outline rather than a dark one.
Collision is only counted for the top-most object so a path/platform/hole/hurdle/teleporter placed over a wall will allow the player to walk/jump through it.

Since you are pushed out of a platform BEFORE the current keyboard movements are checked, you can walk into a wall and wall run without falling into a hole or void below you. This also allows wall jumped.

The player's hitbox is a single point at their center. So a player can squeeze through a single-unit gap.

Objects that can be jumped over have a light outline and ones that cannot have a dark outline. (Only important for players to know, and play-testing)

The player can only jump a max of 50 units.

"Movement Speed" is actually pixels/frame rather than units/frame. This makes "Movement Speed" = units per 5 frames. Without this a speed of just 1 is too fast :(

Right clicking hides/shows text boxes.

Pressing "[" and "]" lets you draw a rectangle between two opposite corners, and pressing ctrl give you a copy-able command to create an object there.



















Now onto actual syntax, you have 2 choices.
OBJECT  X  Y  W  H           or           W*H  OBJECT  at (x,y)
For the first one, order matters, but the second can be in any order since each element will have its own syntax and is more readable. For this we will be showing both. Although, be sure to declare which you are using with "MODE" gamerule.

The most common differences between objects is if they can be jumped, if they kill, and if they are solid. A solid object cannot be walked thought (but can be jumped over if that's allowed). A non-solid object can be referred to as a "pad" or "platform" since it can be stood on. (If you jump onto a solid object, you cannot move without jumping again)

There are a list of preset colors that can be used with #COLOR_NAME. Or if you want to make a lava wall that looks like a normal wall you can do #STONE, #GRAY, or just #WALL (yep, names of default platform colors exist too in here) And use #(R,G,B,A) for a custom color.

Some objects require "link codes" which are strings that match to link to other platforms to make teleporter pairs, or lock-key pairs, etc. Checkpoints also have names that are displayed at the top when they are touched. ALL important strings are inputted as the first value followed by the rest. This isn't really important since the order can be whatever you want, but use quotes for this.

There are some special tags you can add at the start or end, these are INVISIBLE, FORCED, JUMPABLE that have no extra data attached. FORCED means it cannot be jumped anymore. INVISIBLE objects will not be drawn but still have affects the same as before.
Some other tags need extra data like ELASTIC(POWER), BLINKING(EXIST TIME, MISSING TIME), and MOVING(X DISTANCE, Y DISTANCE, TIME) which make objects behave in new ways.
Elastic objects cause you to bounce off with force you walked into them with multiplied by the power. 
Blinking objects exist for EXIST TIME frames before vanishing for MISSING TIME frames, they have no effects while missing.
Finally, moving objects move for TIME to make it to their new point (X DISTANCE, Y DISTANCE) units away before turning around and repeating it backwards.



Solid, cannot be jumped, and do nothing on contact.


Solid, can be jumped, and do nothing on contact.


Non-solid & do nothing on contact. (Dark outline)

PATH (X_POSITION, Y_POSITION, WIDTH, HEIGHT) 
Non-solid & do nothing on contact. (Light outline)

