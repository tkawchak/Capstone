#***************************************************************************
#*   (c) Yorik van Havre (yorik@uncreated.net) 2014                        *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************/


'''
This is an example postprocessor file for the Path workbench. It is used
to save a list of FreeCAD Path objects to a file.

Read the Path Workbench documentation to know how to convert Path objects
to GCode.
'''

import datetime
now = datetime.datetime.now()


# to distinguish python built-in open function from the one declared below
if open.__module__ == '__builtin__':
    pythonopen = open


def export(objectslist,filename):
    "called when freecad exports a list of objects"
    if len(objectslist) > 1:
        print "This script is unable to write more than one Path object"
        return
    obj = objectslist[0]
    if not hasattr(obj,"Path"):
        print "the given object is not a path"
    gcode = obj.Path.toGCode()
    gcode = parse(gcode)
    gfile = pythonopen(filename,"wb")
    gfile.write(gcode)
    gfile.close()


def parse(inputstring):
    "parse(inputstring): returns a parsed output string"
    print "postprocessing..."

    # List of currently supported GCode commands FreeCAD
    # Command 	Description 	Supported Arguments
    # G0 	rapid move 	X,Y,Z,A,B,C
    # G1 	normal move 	X,Y,Z,A,B,C
    # G2 	clockwise arc 	X,Y,Z,A,B,C,I,J,K
    # G3 	counterclockwise arc 	X,Y,Z,A,B,C,I,J,K
    # G81, G82, G83 	drill 	X,Y,Z,R,Q
    # G90 	absolute coordinates 	
    # G91 	relative coordinates 	
    # (Message) 	comment 

    command_translation = {
        "G0": "G00",  # rapid move
        "G1": "G01",  # normal (feed) move
        "G2": "G02"   # clockwise arc move
    }
    
    output = "(Custom GCode for SHARK HD4 CNC Machine)\n"
    output += "(Exported by FreeCAD)\n"
    # """
    # "( [TP_FILENAME] )"
    # "( File created: [DATE] - [TIME])"
    # "( for CNC Shark from Vectric )"
    # "( Material Size)"
    # "( X= [XLENGTH], Y= [YLENGTH], Z= [ZLENGTH])"
    # "( Z Origin for Material  = [Z_ORIGIN])"
    # "( XY Origin for Material = [XY_ORIGIN])"
    # "(      XY Origin Position  = X:[X_ORIGIN_POS], Y:[Y_ORIGIN_POS])"
    # "( Home Position)"
    # "(  X = [XH] Y = [YH] Z = [ZH])" 
    # "( Safe Z = [SAFEZ])"
    # "([FILE_NOTES])"
    # "(Toolpaths used in this file:)"
    # "([TOOLPATHS_OUTPUT])"
    # "(Tool used in this file: )"
    # "([TOOLNAME])"
    # "(|---------------------------------------)"
    # "(| Toolpath:- '[TOOLPATH_NAME]'    )"
    # "(|---------------------------------------)"
    # """

    # Speed of spindle - doesn't really matter?
    spindlespeed = "21000"
    rapidrate = "F50.0"
    # height of the router to move to when not cutting
    rapidheight = "Z0.2100"
    # start position of the router
    startX = "X0.000"
    startY = "Y0.000"
    # end position of the router
    endX = "X0.000"
    endY = "Y0.000"
    
    # write some stuff first
    output += "(Time: "+str(now)+")\n"
    output += "(Start header for carving)\n"
    output += "G90\nG20\n" + rapidrate + "\nG64 P.1\nS " + spindlespeed + "\nM3\nG0 " + rapidheight + "\n"
    
    # vars to keep track of some commands
    lastcommand = ""
    lastfeedrate = ""
    lastplungerate = ""
    lastXpos = "X0"
    lastYpos = "Y0"
    lastZpos = rapidheight

    # treat the input line by line
    lines = inputstring.split("\n")
    for line in lines:
        line = line.strip()
        if line == "" or line[0] == "(":
            continue
        
        # split the G/M command from the arguments
        line_split = line.split(" ")
        # handle case of G F XYZ commands (most common)
        if len(line_split) > 2 and "F" in line_split[1]:
            command, feedrate, args = line.split(" ", 2)
        # handle case of any other command with args
        elif len(line_split) > 1:
            command, args = line.split(" ", 1)
            feedrate = lastfeedrate
        # handle case of no args, just one command
        else:
            command = line
            args = ""
            feedrate = lastfeedrate
        
        # output command for debug purposes
        output += "(Command: " + command + ", Feed Rate: " + feedrate + ", args: " + args + ")\n"
        
        # translate the command from Standard GCode to Shark HD4 GCode
        output_command = command_translation[command]

        # format the command arguments
        output_commands = ""
        Xpos = lastXpos
        Ypos = lastYpos
        Zpos = lastZpos
        for arg in args.split(" "):
            if "X" in arg:
                Xpos = arg
            elif "Y" in arg:
                Ypos = arg
            elif "Z" in arg:
                Zpos = arg
            elif "I" in arg:
                Ipos = arg
            elif "J" in arg:
                Jpos = arg
            elif "K" in arg:
                Kpos = arg

        # only output the feedrate if it is different from before
        if feedrate != lastfeedrate:
            output += feedrate + "\n"

        # add the command
        output += output_command

        # determine which args to give to the output
        if output_command == "G02":
            output += " " + Xpos + " " + Ypos + " " + Ipos + " " + Jpos + "\n"
        elif output_command == "G01":
            output += " " + Xpos + " " + Ypos + " " + Zpos + "\n"
        elif output_command == "G00":
            output += " " + Xpos + " " + Ypos + " " + Zpos + "\n"
        else:
            raise ValueError("Unrecognized Command: " + output_command)
            return "(Unrecognized input Do not Carve!!)\n"  

        # store the latest command
        lastcommand = command
        lastfeedrate = feedrate
        lastXpos = Xpos
        lastYpos = Ypos
        lastZpos = Zpos
        
    # write some more stuff at the end
    output += "(Begin Footer)\n"
    output += "G00 " + rapidheight + "\nG00 " + endX + " " + endY + "\nM02"
    
    print "done postprocessing."
    return output

print __name__ + " gcode postprocessor loaded."

