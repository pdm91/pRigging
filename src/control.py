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
    
    def genCtrl(
                self, 
                _templateObj, 
                _name = "", 
                _groupExtsOverride = [],
                _gExts = [],
                _noGroups = False,
                _controlExtOverride = "",
                _cExt = "",
                _addConstraintToObj = [],
                _const = [],
                _orientToTemplate = True,
                _orient = True,
                _moveToTemplate = True,
                _move = True,
                _parent = ""
              ):
        
        """
            Method: genCtrl
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
                _addConstraintToObj:    Adds a constraint between the control and the template joint
                                        with the control as the driver. takes a list of strings
                                        representing constraints, "parent","orient","point" and "scale"
                                        are currently dealt with. If not set, or un-handled strings are
                                        entered no constraints are created
                _const:                 Short name for _addConstraintToObj
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
            
            #ensure pynode rather than unicode
            
            templateObj = pm.PyNode(_templateObj)
            
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
                
                self.m_control.setRotation(templateObj.getRotation(space = 'world'))
                
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
                        
            if _addConstraintToObj != [] or _const != []:
                
                #make a set from both argument lists removing duplicates
                
                constSet = set(_addConstraintToObj + _const)
                                
                #then cycle through the list of constraints to add 
                
                for constraint in constSet:
                    
                    self.m_outConstraints.append(self.addConstraint(constraint, templateObj,self.m_control))
            
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
                        
                    groupName = self.addExtToNames( [self.m_control], _grpExts[i])[0]
                    
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
                
        """--------------------"""  
                
    def getCtrl (self):
        
        """
            Method: getCtrl
                A method that returns the control              
            
            On Exit:                    retuns the control object                      
        """                                 
        
        return self.m_control
        
        """--------------------"""
        
    def getTopGrp (self):
        
        """
            Method: getTopGrp
                A method that returns top group of the control             
            
            On Exit:                    retuns the group                      
        """                                 
        
        if len(self.m_groups) != 0:
        
            return self.m_groups[0]
            
        else:
            
            return self.m_control
        
        """--------------------"""
        
    def offsetTopGroup (self, _x, _y, _z, _os = True, _r = True):
        
        """
            Method:
                a method to offset the top group of the control structure
                
            Inputs:
                _x:                     The x offset
                _y:                     The y offset
                _z:                     The z offset
                _os:                    defaults to true 
                _r:                     defaults to true
                
            On Exit:
                the top group of the control structure has been offset based 
                on the input
                
        """
        #set up the space defining string
        
        sp = "world"
        
        if _os == True:
            
            sp = "preTransform"
        
        #if relative = true
        if _r:
            
            if len(self.m_groups) == 0:
            
                self.m_control.translateBy((_x, _y, _z), space = sp)
            
            else:
                
                self.m_groups[0].translateBy((_x, _y, _z), space = sp)
        
        else:
             if len(self.m_groups) == 0:
            
                self.m_control.setTranslation((_x, _y, _z), space = sp)
            
             else:
                
                self.m_groups[0].setTranslation((_x, _y, _z), space = sp)
           
        """--------------------"""
        
    def addAttribute(self,
                _name,
                _type,
                _dv = 0,
                _max = 1,
                _min = -1,
                _setMax = False,
                _setMin = False):
        
        """
            Method: addAttribute
                a method to add an attribute to the control
                
            Inputs:
                _name:                  The name of the attribute
                _type:                  The type of data to be stored
                _dv:                    The default value, defaults to 0
                _max:                   The max value, default = 1
                _min:                   The min value, default = -1
                _setMax:                Whether or not to set the max value, defaults to False
                _setMin:                Whether or not to set the min value, defaults to False
                
            On Exit:                    The attribute has been created
            
        """
        
        return self.m_control.addAttr(_name, at = _type, dv = _dv, hxv = _setMax, hnv = _setMin, max = _max, min = _min, k = True)
                
        """--------------------"""
        
#----------END-Control-Class----------#  a
