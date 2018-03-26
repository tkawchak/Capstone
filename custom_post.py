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
    
    # write some stuff first
    output += "(Time: "+str(now)+")\n"
    output += "(Start header for carving)\n"
    output += "G90\nG20\n[FC]\nG64 P.1\nS 2000\nM3\nG0 [ZH]\n"
    
    # vars to keep track of some commands
    lastcommand = ""
    lastfeedrate = ""
    lastplungerate = ""
    lastXpos = 0
    lastYpos = 0
    lastZpos = 0

    # treat the input line by line
    lines = inputstring.split("\n")
    for line in lines:
        # split the G/M command from the arguments
        line_split = line.split(" ")
        # handle case of G F XYZ commands (most common)
        if len(line_split) > 2:
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
        
        if feedrate != lastfeedrate:
            output += feedrate + "\n"

        # print out the command and the args
        output += command + " " + args + "\n"

        # store the latest command
        lastcommand = command
        lastfeedrate = feedrate
        
    # write some more stuff at the end
    output += "(Begin Footer)\n"
    output += "G00 [ZH]\nG00 [XH] [YH]\nM02"
    
    print "done postprocessing."
    return output

print __name__ + " gcode postprocessor loaded."

