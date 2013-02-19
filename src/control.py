#----------Imports----------#

import pymel.core as pm
import pRigging.src.riggingbase as prb

#----------Control-Class----------#

class Control(prb.RiggingBase):    
    
    """
        Class: Control
            A class that contains a control (a set of groups and a control(usually a
            nurbs curve)) and a list of all the constraints that it is the driver of
        
        File: pRigging/src/control.py
        
        Contains:
            self.m_control:         The control object (usually the nurbs curve)
            self.m_groups:          The groups above the control, ordered from highest
                                    to lowest in the hierarchy, with the last one being
                                    group immediately above the control in the hierarchy
                                    usually an _SDK group
            self.m_outConstraints:  The output constraints from the control, ones with
                                    the control as the driver
        
        Imports:
            pymel.core as pm
            pRigging.src.riggingbase as prb
            
        Inherits:
            prb.RiggingBase
    """
    
    def __init__(self):
        
        """
            Method: __init__
                A method called when the class is instanciated, sets up the attributes
                for the object
            
            Inputs:
                self:                   A pointer to the instance of the object being
                                        created.
        """
        #initialise the object's attributes
        
        self.m_control = None
        self.m_groups = []
        self.m_outConstraints = []
        self.m_ext = "CTRL"
        
        """--------------------"""
    
    def genCTRL(
                self, 
                _templateObj, 
                _name = "", 
                _groupExtsOverride = [],
                _gExts = [],
                _noGroups = False,
                _controlExtOverride = "",
                _cExt = "",
                _addConstToObj = [],
                _const = [],
                _orientToTemplate = True,
                _orient = True,
                _moveToTemplate = True,
                _move = True,
                _parent = ""
              ):
        
        """
            Method: genCTRL
                A method that generates a control based on an input object with optional additional
                inputs.
            
            Inputs:
                self:                   A pointer to the instance of the Control class of which
                                        this method is being called
                _templateObj:           An object used as a template for the control, e.g. a joint
                                        or IK handle, this is required.
                _name:                  An optional field, enter the base name, the extension will be
                                        added automatically. If not defined the name will be derived 
                                        from the object name.
                _groupExtsOverride:     A list of group extensions, defining how many groups to add
                                        above the control and how to extend them. If not set, the three
                                        default groups will be added over the control, orderd from highest
                                        to lowest in the hierarchy
                _gExts:                 Short name for _groupExtsOverride.
                _noGroups:              Defaults to false, if set, there will be no groups added to the
                                        control.
                _controlExtOverride:    Overrides the default CTRL extension when set, when an empty
                                        default is used
                _cExt:                  Short name for _controlExtOverride
                _addConstToObj:         Adds a constraint between the control and the template joint
                                        with the control as the driver. takes a list of strings
                                        representing constraints, "parent","orient","point" and "scale"
                                        are currently dealt with. If not set, or un-handled strings are
                                        entered no constraints are created
                _const:                 Short name for _addConstToObj
                _orientToTemplate:      Defaults to True, oriebnts the control to the template object
                                        passed in, if off it is alligned to the world
                _orient:                Short name for _orientToTemplate
                _moveToTemplate:        Defaults to True, moves the control to the same position as
                                        the template object, if not set it will remain at the offset
                _move:                  Shot name for _moveToTemplate
                _parent:                Defaults to empty string, if set to an object the control's
                                        top-most group will be parented under the object passed in
                
            
            On Exit:                    The control is generated based on the inputs.                         
        """
        
        #if there is a template object
        
        if _templateObj:
            
            #check if a control extension override is set
            
            if _controlExtOverride != "":
                
                #set the self.m_ext value to the override value
                
                self.m_ext = _controlExtOverride
                
            elif _cExt != "":
                
                self.m_ext = _cExt
                
            #check if a name is set
            
            ctrlName = ""
            
            if _name != "":
                
                #if one is set, use it
                
                ctrlName = self.addExtToNames([_name], self.m_ext)[0]
                
            #otherwise
            
            else:
                
                #set the name to be that of the template object
                #minus it's last extension
                
                ctrlName = self.removeExtFromNames([_templateObj])[0]

                #and add the new extension
                
                ctrlName = self.addExtToNames([ctrlName], self.m_ext)[0]

            #make the control

            self.m_control = pm.circle(name = ctrlName, nr = (1,0,0))[0] #index 0 as circle retuns the transform 
                                                                        #and the make nurbs circle node
            #if move is set to true or left at default
            
            if _moveToTemplate == True and _move == True:
                
                #move the control to the location of the template object
                
                self.m_control.setTranslation(_templateObj.getTranslation(space = 'world'))
                
            #if orient is set to true or left at default
            
            if _orientToTemplate == True and _orient == True:
                
                #rotate the control to match the orientation of the template object
                
                self.m_control.setRotation(_templateObj.getRotation(space = 'world'))
                
            #if _noGroups is false
            
            if not _noGroups:
                
                #set up the exts list with the default groups
                
                exts =["0","CONST","SDK"]
                
                #if override extensions were added using the long name
                #print _groupExtsOverride != []
                #print _gExts != []
                if _groupExtsOverride != []:
                    
                    exts = _groupExtsOverride
                    
                #if override extensions were added using the short name
                
                elif _gExts != []:
                    
                    exts = _gExts
                
                #add the groups
                
                self.addGroups(exts)
            
            #check if either of the const keyword arguments had values set in them 
                        
            if _addConstToObj != [] or _const != []:
                
                #make a set from both argument lists removing duplicates
                
                constSet = set(_addConstToObj + _const)
                                
                #then cycle through the list of constraints to add 
                
                for const in constSet:
                    
                    self.addConstraint(const, _templateObj)
            
            #finally, if the _parent flag was set, parent the top of the control hierarchy under
            #the parent object specified
            
            self.setCtrlParent(_parent)
                    
            #clear selection   
            
            pm.select(cl=True)                    
                            

                
        """--------------------"""
        
    def addGroups(self,_grpExts,_topOfHierarchy=True, _toh=True):
    
        """
            Method: addGroups
                A method that adds groups above the control based on the inputs
            
            Inputs:
                _grpExts:               Extensions which define what groups to add over the control,
                                        oirdered from highest to lowest in the desired hierarchy
                _topOfHierarchy:        An optional boolean value which states whether to put the 
                                        groups listed at the top of the control hierarchy or immediately
                                        above the control object.
                _toh                    Short name for top of hierarchy

            
            On Exit:                    The specified groups have been added to the control                       
        """
        
        #if the extension list is not an empty list
        
        if _grpExts != []:
            
                #set the insertion id
                
                insertId = 0
                
                if (_topOfHierarchy ==False or _toh == False) and len(self.m_groups) != 0:
                    
                     insertId = len(self.m_groups)-1
                     
                #set the object to parent the groups under
                
                parentObj = ""
                
                if insertId == 0 and len(self.m_groups) != 0:
                    
                    parentObj = self.m_groups[0].getParent()
                    
                elif insertId == 0 and len(self.m_groups) == 0:
                    
                    parentObj = self.m_control.getParent()
                    
                elif insertId != 0:
                    
                    parentObj = self.m_groups[insertId-1]
                
                #cycle through the extensions in reverse order
                
                for i in range((len(_grpExts)-1),-1,-1):
                    
                    #set the group name
                        
                    groupName = self.addExtToNames( self.removeExtFromNames([self.m_control]), _grpExts[i])[0]
                    
                    #if the caller has specified that thegroups should be inserted over the
                    #control object, or there are no groups and it is the first iteration

                    if ((_topOfHierarchy == False or _toh == False) or len(self.m_groups) == 0) and i == (len(_grpExts)-1):
                        
                        #add the new group over the control
                               
                        self.m_groups.insert(insertId, self.addGroupOverObj (groupName, self.m_control))
                        
                    else:
                        
                        #add the group over the last group
                        
                        self.m_groups.insert(insertId, self.addGroupOverObj (groupName, self.m_groups[insertId]))
   
                #fix the hierarchy
                
                self.m_groups[insertId].setParent(parentObj)
                
                #unselect all
                
                pm.select(cl=True)
                
        """--------------------"""
        
    def addConstraint(self, _const, _drivenObj, 
                        _force = False, _f = False, 
                        _tx = False, _ty = False, _tz = False, _t = True,
                        _rx = False, _ry = False, _rz = False, _r = True,
                        _sx = False, _sy = False, _sz = False, _s = True
                      ):
            
        """
            Method: addConstraint
                A method that adds constraints from the control to the specified object
            
            Inputs:
                _const:                 A string defining the constraint type
                _drivenObject:          The child object of the Constraint
                _force:                 Defaults to false, defines whther or not to replace 
                                        existing contraints with the one specified, if left false,
                                        the constraint will be put onto attributes that aren't 
                                        already controlled, is set to true any confilcting 
                                        connections will be broken and replaced witht he inputted 
                                        ones 
                _f:                     Short name for _force
                attribute specifics:    These are keyword arguments for each axis of translate
                                        rotate and scale, default to false, if all values pertinant
                                        to the specified constraint are false, defaults will be used
                                        (i.e. all of them) if any of them are set, those ones will be
                                        constrained and the ones left at the default of false will not.
                                        The _t, _r and _s keywords give the option to turn off all three
                                        axis in any given transformation type.  
                                        The keywords and default settings:
                                             
                        _tx = False, _ty = False, _tz = False, _t = True,
                        _rx = False, _ry = False, _rz = False, _r = True,
                        _sx = False, _sy = False, _sz = False, _s = True                 

            
            On Exit:                    The specified constraints have been added to the control                       
        """              
                      
        #first check that a constraint has been entered
        
        if _const != "":
            
            #set boolean values for whether or not to constrain each transformation in each axis
            
            #create a boolean which says whether or not any of the translate, rotation, and scale 
            #attributes are connected
            
            doTrans = ((not _drivenObj.tx.isConnected() 
                        and not _drivenObj.ty.isConnected()
                        and not _drivenObj.tz.isConnected()) or (_f or _force)) and _t
            doRot = ((not _drivenObj.rx.isConnected() 
                        and not _drivenObj.ry.isConnected()
                        and not _drivenObj.rz.isConnected()) or (_f or _force)) and _r
            doScale = ((not _drivenObj.sx.isConnected() 
                        and not _drivenObj.sy.isConnected()
                        and not _drivenObj.sz.isConnected()) or (_f or _force)) and _s
            
            #then make a boolean for each transformation type which sayes whether all of the 
            #individual values were left at default
            
            transSet = _tx or _ty or _tz
            rotSet = _rx or _ry or _rz
            sclSet = _sx or _sy or _sz
            
            #switch through constraint types
            
            if (_const == "parent" and (doTrans or doRot)):
                
                #set up skip strings based on the boolean inputs and checks
                
                stList = []
                srList = []
                
                #if translate is not meant to be contrained
                
                if not doTrans:
                
                    #add all of the strings to the list
                
                    stList = ["x","y","z"]
                    
                #otherwise
                
                else: 
                
                #if one or more of the translate axis flags are set
                
                    if transSet:
                        
                        #add the appropriate strings to the list
                        
                        if not _tx:
                            stList.append("x")
                        if not _ty:
                            stList.append("y")
                        if not _tz:
                            stList.append("z")
                            
                    #if force is set, break all rotate conenctions
                    
                    if _f or _force:
                        
                        self.breakConnection(_drivenObj.tx)
                        self.breakConnection(_drivenObj.ty)
                        self.breakConnection(_drivenObj.tz)
                
                #repeat for rotate
                        
                if not doRot:
                
                    srList = ["x","y","z"]
                                  
                else:
                    
                    if rotSet:
                    
                        #add the appropriate strings to the list
                        
                        if not _rx:
                            srList.append("x")
                        if not _ry:
                            srList.append("y")
                        if not _rz:
                            srList.append("z")
                            
                    if _f or _force:
                        
                        self.breakConnection(_drivenObj.rx)
                        self.breakConnection(_drivenObj.ry)
                        self.breakConnection(_drivenObj.rz)
    
                #set up a parent constraint between the control and the template object
                                
                self.m_outConstraints.append(pm.parentConstraint(self.m_control,_drivenObj, mo = True, st = stList, sr = srList)) 
            
            #if orient constraint is chosen and the constraint is meant to be made
            
            elif (_const == "orient" and doRot):
                
                srList = []
                
                #and some of the rotate axis flags have been set
                
                if rotSet:
                    
                    if not _rx:
                        srList.append("x")
                    if not _ry:
                        srList.append("y")
                    if not _rz:
                        srList.append("z")
                        
                #if force is set breack connections
                
                if _f or _force:
                        
                        self.breakConnection(_drivenObj.rx)
                        self.breakConnection(_drivenObj.ry)
                        self.breakConnection(_drivenObj.rz) 
                
                    
                #set up an orient constraint between the control and the template object
                
                self.m_outConstraints.append(pm.orientConstraint(self.m_control,_drivenObj, mo = True, sk = srList)) 

            elif (_const == "point" and doTrans):
                
                stList = []
                
                if transSet:
                    
                    #add the appropriate strings to the list
                    
                    if not _tx:
                        stList.append("x")
                    if not _ty:
                        stList.append("y")
                    if not _tz:
                        stList.append("z")
                        
                #if force is set breack connections
                
                if _f or _force:
                        
                        self.breakConnection(_drivenObj.tx)
                        self.breakConnection(_drivenObj.ty)
                        self.breakConnection(_drivenObj.tz)
                            
                #set up a parent constraint between the control and the template object
                
                self.m_outConstraints.append(pm.pointConstraint(self.m_control,_drivenObj, mo = True, sk = stList)) 

            elif (_const == "scale" and doScale):
                
                ssList = []
                
                if sclSet:
                    
                    #add the appropriate strings to the list
                    
                    if not _sx:
                        ssList.append("x")
                    if not _sy:
                        ssList.append("y")
                    if not _sz:
                        ssList.append("z")
                
                #if force is set breack connections
                
                if _f or _force:
                        
                        self.breakConnection(_drivenObj.sx)
                        self.breakConnection(_drivenObj.sy)
                        self.breakConnection(_drivenObj.sz)
                                    
                #set up a parent constraint between the control and the template object
                
                self.m_outConstraints.append(pm.scaleConstraint(self.m_control,_drivenObj, mo = True, sk = ssList)) 


        """--------------------"""            
    
    def setCtrlParent (self, _parent = "", _world = False):
        
        """
            Method: setCtrlParent
                A method that sets the parent of the control
            
            Inputs:
                _parent:                The parent object, defaults to an empty string
                _world:                 Boolean value defaulting to false, if true the 
                                        control is effectively unparented                
            
            On Exit:                    The specified constraints have been added to the control                       
        """
        
        if _world == True:
            
            #if there are no groups
            
            if len(self.m_groups) == 0:
                
                #parent the control under the specified parent
                
                self.m_control.setParent(world = True)    
                
            else:
                
                #parent the top group under the parent
                
                self.m_groups[0].setParent(world = True)  
        
        elif _parent != "":
            
            #if there are no groups
            
            if len(self.m_groups) == 0:
                
                #parent the control under the specified parent
                
                self.m_control.setParent(_parent)    
                
            else:
                
                #parent the top group under the parent
                
                self.m_groups[0].setParent(_parent)    
                
                                 
#----------END-Control-Class----------#  a
