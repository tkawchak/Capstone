+================================================
+                                                
+ G Code - Vectric machine output configuration file   
+                                                
+================================================
+                                                
+ History                                        
+                                                
+ Who      When       What                         
+ ======== ========== ===========================
+ Tony     11/12/2007 Written                      
+ Mark     19/01/2009 Separated Plunge and cut feed, addded Arcs to name.    
+ Mark     16/02/2009 Added move to Home at EOF
+ Mark     08/09/2010 Added G64 and static spindle speed to header.
+ Dana     09/11/2011 Added DIRECT_OUTPUT option for new control panel
+ Brian    15/11/2011 Renamed as 3D Contour - Use Next Wave specified 
+                     G64 tolerance for 2D machining G64 tolerance for 3D machining  
+================================================

POST_NAME = "CNCShark-USB 3D Contour (inch) (*.tap)"

FILE_EXTENSION = "tap"

UNITS = "INCHES"

DIRECT_OUTPUT = "CNCShark|CNCShark_run.ini"

SUBSTITUTE = "({)}"

+------------------------------------------------
+    Line terminating characters                 
+------------------------------------------------

LINE_ENDING = "[13][10]"

+------------------------------------------------
+    Block numbering                             
+------------------------------------------------

LINE_NUMBER_START     = 0
LINE_NUMBER_INCREMENT = 10
LINE_NUMBER_MAXIMUM = 999999

+================================================
+                                                
+    Formating for variables                     
+                                                
+================================================

VAR LINE_NUMBER = [N|A|N|1.0]
VAR SPINDLE_SPEED = [S|A|S|1.0]
VAR CUT_RATE    = [FC|A|F|1.1]
VAR PLUNGE_RATE = [FP|A|F|1.1]
VAR X_POSITION = [X|A| X|1.4]
VAR Y_POSITION = [Y|A| Y|1.4]
VAR Z_POSITION = [Z|A| Z|1.4]
VAR ARC_CENTRE_I_INC_POSITION = [I|A| I|1.4]
VAR ARC_CENTRE_J_INC_POSITION = [J|A| J|1.4]
VAR X_HOME_POSITION = [XH|A| X|1.4]
VAR Y_HOME_POSITION = [YH|A| Y|1.4]
VAR Z_HOME_POSITION = [ZH|A| Z|1.4]

+================================================
+                                                
+    Block definitions for toolpath output       
+                                                
+================================================

+---------------------------------------------------
+  Commands output at the start of the file
+---------------------------------------------------

begin HEADER

"( [TP_FILENAME] )"
"( File created: [DATE] - [TIME])"
"( for CNC Shark from Vectric )"
"( Material Size)"
"( X= [XLENGTH], Y= [YLENGTH], Z= [ZLENGTH])"
"( Z Origin for Material  = [Z_ORIGIN])"
"( XY Origin for Material = [XY_ORIGIN])"
"(      XY Origin Position  = X:[X_ORIGIN_POS], Y:[Y_ORIGIN_POS])"
"( Home Position)"
"(  X = [XH] Y = [YH] Z = [ZH])" 
"( Safe Z = [SAFEZ])"
"([FILE_NOTES])"
"(Toolpaths used in this file:)"
"([TOOLPATHS_OUTPUT])"
"(Tool used in this file: )"
"([TOOLNAME])"
"(|---------------------------------------)"
"(| Toolpath:- '[TOOLPATH_NAME]'    )"
"(|---------------------------------------)"
"G90"
"G20"
"[FC]"
"G64 P.1"
"S 2000"
"M3"
"G0 [ZH]"

+---------------------------------------------------
+  Commands output for rapid moves 
+---------------------------------------------------

begin RAPID_MOVE

"[FC]"
"G00[X][Y][Z]"

+---------------------------------------------------
+  Commands output for the plunge move
+---------------------------------------------------

begin PLUNGE_MOVE

"[FP]"
"G1[X][Y][Z]"

+---------------------------------------------------
+  Commands output for the first feed rate move
+---------------------------------------------------

begin FIRST_FEED_MOVE

"[FC]"
"G01[X][Y][Z]"


+---------------------------------------------------
+  Commands output for feed rate moves
+---------------------------------------------------

begin FEED_MOVE

"G01[X][Y][Z]"

+---------------------------------------------------
+  Commands output for the first clockwise arc move
+---------------------------------------------------

begin FIRST_CW_ARC_MOVE

"[FC]"
"G02[X][Y][I][J]"


+---------------------------------------------------
+  Commands output for clockwise arc  move
+---------------------------------------------------

begin CW_ARC_MOVE

"G02[X][Y][I][J]"


+---------------------------------------------------
+  Commands output for the first counterclockwise arc move
+---------------------------------------------------

begin FIRST_CCW_ARC_MOVE

"[FC]"
"G03[X][Y][I][J]"


+---------------------------------------------------
+  Commands output for counterclockwise arc  move
+---------------------------------------------------

begin CCW_ARC_MOVE

"G03[X][Y][I][J]"

+---------------------------------------------------
+  Commands output for a new segment - toolpath
+---------------------------------------------------

begin NEW_SEGMENT
"(|---------------------------------------)"
"(| Toolpath:- '[TOOLPATH_NAME]'     )"
"(|---------------------------------------)"

+---------------------------------------------------
+  Commands output at the end of the file
+---------------------------------------------------

begin FOOTER

"G00 [ZH]"
"G00 [XH] [YH]"
"M02"

