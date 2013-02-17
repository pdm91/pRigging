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
                
                #cycle through the extensions
                
                for i in range((len(exts)-1),-1,-1):
                    
                    #set the group name
                        
                    groupName = self.addExtToNames( [ctrlName], exts[i])[0]

                    #if it is the first iteration

                    if i == (len(exts)-1):
                        
                        #add the new group over the control
                               
                        self.m_groups.insert(0, self.addGroupOverObj (groupName, self.m_control))
                        
                    else:
                        
                        #add the group over the last group
                        
                        self.m_groups.insert(0, self.addGroupOverObj (groupName, self.m_groups[0]))
            
            #check if either of the const keyword arguments had values set in them 
                        
            if _addConstToObj != [] or _const != 0:
                
                #make a set from both argument lists removing duplicates
                
                constSet = set(_addConstToObj + _const)
                
                #check the attributes of the object to make and set boolean values for them
                
                isTXD = _templateObj.tx.isConnected()
                isTYD = _templateObj.ty.isConnected()
                isTZD = _templateObj.tz.isConnected()
                isRXD = _templateObj.rx.isConnected()
                isRYD = _templateObj.ry.isConnected()
                isRZD = _templateObj.rz.isConnected()
                isSXD = _templateObj.sx.isConnected()
                isSYD = _templateObj.sy.isConnected()
                isSZD = _templateObj.sz.isConnected()
                                
                #then cycle through the list of constraints to add 
                
                for const in constSet:
                    
                    #swich through the const types with checks if the relevant attributes are
                    #already driven 
                    
                    if (const == "parent"
                    and not isTXD
                    and not isTYD
                    and not isTZD
                    and not isRXD
                    and not isRYD
                    and not isRZD):
                            
                        #set up a parent constraint between the control and the template object
                        
                        self.m_outConstraints.append(pm.parentConstraint(self.m_control,_templateObj, mo = True)) 
                    
                    elif (const == "orient"
                    and not isRXD
                    and not isRYD
                    and not isRZD):
                            
                        #set up an orientt constraint between the control and the template object
                        
                        self.m_outConstraints.append(pm.orientConstraint(self.m_control,_templateObj, mo = True)) 
                  
                    elif (const == "point"
                    and not isTXD
                    and not isTYD
                    and not isTZD):
                            
                        #set up a parent constraint between the control and the template object
                        
                        self.m_outConstraints.append(pm.pointConstraint(self.m_control,_templateObj, mo = True)) 

                    elif (const == "scale"
                    and not isSXD
                    and not isSYD
                    and not isSZD):
                            
                        #set up a parent constraint between the control and the template object
                        
                        self.m_outConstraints.append(pm.scaleConstraint(self.m_control,_templateObj, mo = True)) 
            
            #finally, if the _parent flag was set, parent the top of the control hierarchy under
            #the parent object specified
            
            if _parent != "":
                
                #if there are no groups
                
                if len(self.m_groups) == 0:
                    
                    #parent the control under the specified parent
                    
                    self.m_control.setParent(_parent)    
                    
                else:
                    #parent the top group under the parent
                    
                    self.m_groups[0].setParent(_parent)                        
                            

                
        """--------------------"""
                            
#----------END-Control-Class----------#  a

reload(prb)
test = Control()
sel = pm.ls(sl = True)[0]
test.genCTRL(sel, _const = ["point","orient","scale"], _parent = 'joint1')


