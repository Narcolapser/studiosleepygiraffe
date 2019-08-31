# Minecraft-Command-Craft
A set of scripts for converting blender models into single command # # # Minecraft-Command-Craft
A set of scripts for converting blender models into single command constructions in Minecraft. This system follows the Unix Philosophy and has each script perform one single task. Combine all of the scripts to create a full system from Blender to Minecraft. 

# Explanation of scripts

## Command Joiner
Takes a list of commands and joins them into a single tower. It can be run as a script, but know that it does not modify the commands in any way. The commands need to be converted into a relative format. 

## Command Relativizer
This script takes a command that uses absolute coordinates and translates them into relative coordinates with an offset specified. In this way, you can prepare a list of commands to be joined by command Joiner.

## mcpile
Taking a list of absolute commands, MCPile runs them through command Relativizer and Command Joiner. By doing so, it turns a list of raw, absolute commands into a list a single command.

## objtofill
This script takes an obj file, such as one exported from Blender, and turns it into a list of fill commands. The process of deciding what the fill should be is done by constructing a bounding box and rounding out to the next full block. It does no logic to figure out the best way to do the fills, that's your job in Blender. You need to create a collection of rectangular volumes. I may recreate this later in a way that does a proper voxel scribing, someday when I have the time Knuth had for typesetting. 

# Basic order of things
Build an object in Blender. You make a bounding box for every fill command. So each fill is a different object, that's important. Export that objects from Blender to an obj. Run objtofill.py on it. Save the output to a file. Run mcpile on that. Save the output to your clipboard, paste into a Minecraft command block.
