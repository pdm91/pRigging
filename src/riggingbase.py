#----------Imports----------#

import pymel.core as pm

#----------RiggingBase-Class----------#

class RiggingBase:    
    
    """
        Class: RiggingBase
            A base class for the majority of the classes in the pRigging toolset,
            includes functionality that is needed throughout the toolset such as
            extension adding to names
        
        File: pRigging/src/riggingbase.py
        
        Contains:
        
        Imports:
            pymel.core as pm
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
        pass
        
        """--------------------"""
    
    def addExtToNames(self, _names, _ext):
        
        """
            Method: addExtToNames
                a method which adds the inputted extension onto the end of the names, separated
                by an underscore
            
            Inputs:
                self:                   A pointer to the instance of the RiggingBase class of which
                                        this method is being called
                _names:                 A list names to add the extension to
                _ext:                   the extension to add the names
            
            On Exit:                    The extensions have been added to the name strings                      
        """
        
        returnList = _names[:]
        
        #early breakout if no extension is supplied

        if _ext == "":
            
            return returnList
            
        for i in range (0, (len(_names))):
            
            #if neither the end of the name nor the start of the extension is an underscore
            
            if returnList[i][-1] != "_" and _ext[0] != "_":
                
                #add an underscore to the end of the name
                
                returnList[i] = returnList[i] + "_"
            
            #if both have one
                
            if returnList[i][-1] == "_" and _ext[0] == "_":
                
                #remove the underscore from the start of the extension
                
                _ext = _ext[1:]
                
            #add the extension to the name
            
            returnList[i] = returnList[i]+_ext
                            
            #and then remove any long,name path influence from the name
            
            index =  returnList[i].rfind("|")
            
            #check that there was an uderscore and only edit the name if there was
            
            if index >= 0:
            
                #set the new name to be the old name except what was after the undercore
                
                returnList[i] = returnList[i][index:]
        
        #return the list of names

        return returnList       
        
        """--------------------"""
        
    def removeExtFromNames(self, _names):
        
        """
            Method: removeExtToNames
                a method which removes an extension from a name by searching for the last underscore
            
            Inputs:
                self:                   A pointer to the instance of the RiggingBase class of which
                                        this method is being called
                _names:                 A list names to remove the extension from
            
            On Exit:                    The extensions have been removed from the name strings                       
        """
            
        for i in range (0, (len(_names))):
            
            returnList = _names [:]
            
            #find the last _ in the name
            
            index =  returnList[i].rfind("_")
            
            #check that there was an uderscore and only edit the name if there was
            
            if index >= 0:
            
                #set the new name to be the old name except what was after the undercore
                
                returnList[i] = returnList[i][:index]
                
            #and then remove any long,name path influence from the name
            
            index =  returnList[i].rfind("|")
            
            #check that there was an uderscore and only edit the name if there was
            
            if index >= 0:
            
                #set the new name to be the old name except what was after the undercore
                
                returnList[i] = returnList[i][index:]

        return returnList
        
        """--------------------"""
        
    def transAndOrientObj (self, _subject, _destObj, _move = True, _orient = True):
        
        """
            Method: transAndOrientObj
                a method which moves and rotates the subject object to match the destination object
            
            Inputs:
                self:                   A pointer to the instance of the RiggingBase class of which
                                        this method is being called
                _subject:               The object being moved
                _destObj:               Where the object is moving to
                _move:                  Whether to move or not, defaults to True
                _orient:                Whether to Rotate or not, defaults to True
            
            On Exit:                    the object has been moved and/or rotated to mach the destObj                       
        """
        
        if _move:
            
            #move subject to dest
            
            _subject.setTranslation(_destObj.getTranslation(space = 'world'), space = 'world')
        
        if _orient:
            
            #rotate to match dest
            
            _subject.setRotation(_destObj.getRotation(space = 'world'), space = 'world')       
        
        """--------------------"""
    
    def addGroupOverObj (self, _groupName, _obj, _orient = True):
        
        """
            Method: transAndOrientObj
                a method which moves and rotates the subject object to match the destination object
            
            Inputs:
                self:                   A pointer to the instance of the RiggingBase class of which
                                        this method is being called
                _groupName:             The name of the group to be made
                _obj:                   The object to put the group over
                _orient:                Whether or not to move the group to the same location as
                                        the object being grouped, defaults to true
            
            On Exit:                    A group has been added over the object                       
        """
        #ensure the selection is clear
        
        pm.select(cl=True)
        
        #make a new group with the name passed in
        
        newGroup = pm.group(n= _groupName)
        
        #move and orient the group to the object that will be grouped
        
        self.transAndOrientObj(newGroup, _obj)
        
        #and parent the object to the group
        
        _obj.setParent(newGroup)
        
        #return the group   
        
        return newGroup  
        
        """--------------------"""          

    def breakConnection (self, _attr,):
        
        """
            Method: breakConnection
                a method which breaks a connection driving an attribute and removes the driver if 
                there are no more connections from the driver and it is a constraint (to ensure meshes)
                are not removed if they're not driving anything
            
            Inputs:
                self:                   A pointer to the instance of the RiggingBase class of which
                                        this method is being called
                _attr:                  The attribute having it's connection broken
            
            On Exit:                    The connection has been removed                       
        """
        
        #check that the attribute is connected
        
        if _attr.isConnected():

            #save the driver object
            
            driver = _attr.connections()
            
            #make a set of the driver list for later comparison
            
            a = set(driver)
            
            #disconnect the attribute
            
            _attr.disconnect()
            
            #if the type of the driver was a constraint and there 
            #are no more connections
            
            if ("Constraint" in driver[0].nodeType()) and len(set(driver[0].outputs())-a) == 0:
                
                #remove the driver object
                
                pm.delete(driver[0])            
              
        
        """--------------------""" 
        
    def orientByAim(self,
                    _object,
                    _aimTarget,
                    _upObj = "",
                    _objUp = False,
                    _objRotUp = True,
                    _aimAxis = (1.0,0.0,0.0),
                    _upAxis = (0.0,1.0,0.0),
                    _leaveAim = False
                    ):
                        
        """
            Method: orientByAim
                a method which sets the rotaition of an object by aim constraining it to another object
            
            Inputs:
                self:                   A pointer to the instance of the RiggingBase class of which
                                        this method is being called
                _object:                The object to bw aimed
                _aimTarget:             The object that the aimed object will be pointing at
                _upObj:                 Defaults to an empty string, sets the object that will 
                                        define the up vector of the aim constraint, if not set,
                                        the world up will be used
                _objUp:                 Uses the object up  option which sets the up vector 
                                        to aim at the up object, defaults to false
                _objRotUp:              uses the objects rotation to set the up vector for the
                                        aim Constraint
                _aimVec:                Defines which axis to aim
                _upVec:                 Defines the up axis of the constraint
                _leaveAim:              Defaults to False, defines whether or not the aim constraint is left
                                        in existance 
            
            On Exit:                The object has been rotated to match the settings                       
        """
        
        #set the world up type string
        
        upType = "scene"
        
        if _objUp == True or _objRotUp == False and _upObj != "":
            
            upType = "object"
            
        elif _upObj != "":
            
            upType = "objectRotation"
            
        constraint = ""
            
        #make the constraint
        
        if _upObj == "":
            
            constraint= pm.aimConstraint(
                                _aimTarget,
                                _object, 
                                mo = False, 
                                aim = _aimAxis, 
                                u = _upAxis, 
                                wu = _upAxis, 
                                wut = upType
                                )
                                
        else:
            
            constraint= pm.aimConstraint(
                                _aimTarget,
                                _object, 
                                mo = False, 
                                aim = _aimAxis, 
                                u = _upAxis, 
                                wu = _upAxis,
                                wuo = _upObj, 
                                wut = upType
                                )
        
        #if the constraint is meant to be deleted
        
        if not _leaveAim:
            
            pm.delete(constraint)
                          
        """--------------------"""
        
    def addConstraint(self, _constraint, _drivenObj, _driverList,
                        _force = False, _f = False, 
                        _tx = False, _ty = False, _tz = False, _t = True,
                        _rx = False, _ry = False, _rz = False, _r = True,
                        _sx = False, _sy = False, _sz = False, _s = True
                      ):
            
        """
            Method: addConstraint
                A method that adds constraints from the driverList to the specified object
            
            Inputs:
                _constraint:            A string defining the constraint type
                _drivenObject:          The child object of the Constraint
                _driverList:            The driver objects
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
        
        if _constraint != "":
            
            #set boolean values for whether or not to constrain each transformation in each axis
            
            #create a boolean which says whether or not any of the translate, rotation, and scale 
            #attributes are connected
            
            doTrans = ((_drivenObj.tx.isFreeToChange()  
                        and _drivenObj.ty.isFreeToChange() 
                        and _drivenObj.tz.isFreeToChange() ) or (_f or _force)) and _t
            doRot = ((_drivenObj.rx.isFreeToChange() 
                        and _drivenObj.ry.isFreeToChange() 
                        and _drivenObj.rz.isFreeToChange() ) or (_f or _force)) and _r
                        
                        
            doScale = ((_drivenObj.sx.isFreeToChange()  
                        and _drivenObj.sy.isFreeToChange() 
                        and _drivenObj.sz.isFreeToChange() ) or (_f or _force)) and _s
            
            #then make a boolean for each transformation type which sayes whether all of the 
            #individual values were left at default
            
            transSet = _tx or _ty or _tz
            rotSet = _rx or _ry or _rz
            sclSet = _sx or _sy or _sz
            
            #switch through constraint types
            
            if (_constraint == "parent" and (doTrans or doRot)):
                
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
                                
                return pm.parentConstraint(_driverList,_drivenObj, mo = True, st = stList, sr = srList)
            
            #if orient constraint is chosen and the constraint is meant to be made
            
            elif (_constraint == "orient" and doRot):
                
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
                
                return pm.orientConstraint(_driverList,_drivenObj, mo = True, sk = srList)

            elif (_constraint == "point" and doTrans):
                
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
                
                return pm.pointConstraint(_driverList,_drivenObj, mo = True, sk = stList)

            elif (_constraint == "scale" and doScale):
                
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
                
                return pm.scaleConstraint(_driverList,_drivenObj, mo = True, sk = ssList)
            
            #for the polevector constraint
            
            elif (_constraint == "poleVector"):
                
                #set up a parent constraint between the control and the template object
                
                return pm.poleVectorConstraint(_driverList,_drivenObj)
                
        """--------------------"""
        
    def enforceHierarchy(self,_objList):
        
        """
            Method: enforceHierarchy
                A method to sort the objects in a list and return the list,
                returns an empty list if it is not in unbroken hierarchy
                
            Inputs:
                _objList:               The list of objects to sort
                                        
            On Exit:                    The list has been sorted and returned
                                        or an empty list if the list was not 
                                        an unbroken hierarchy                 
            
        """
        
        #set up the return list
        
        returnList = _objList     
        
        #cycle through for each element except for one
                
        for i in range(0, len(returnList)-1):
            
            #then cycle through each element except for one, with
            #one less each cycle
            
            j = 0
            while(j < len(returnList)-(i+1)): 
            
                #create a list of all the children and parents of the element one above the one currently being checked
                
                children = returnList[j+1].listRelatives(ad = True)
                parents = returnList[j+1].listRelatives(ap = True)
                
                #set up a variable to store the number of parents
                
                numparents = len(parents)
                checkVal = numparents - 1
                
                #if there was a parent
                
                if numparents != 0:
                    
                    #keep checking until the check value catches up, indicating the
                    #top most parent, and adding the parents to the list
                    
                    while numparents > checkVal:
                        parents = parents + parents[-1].listRelatives(ap = True)
                        numparents = len(parents) 
                        checkVal = checkVal+1
                
                #if the current element is a child of the one the lists relate to
                
                if returnList[j] in children:
                    
                    #swap the elements so the one higher up in the hierarchy has a lower index 
                    #(closer to the front)
                    
                    temp = returnList[j] 
                    returnList[j] = returnList[j+1]
                    returnList[j+1] = temp    
                
                #increment i
                
                j = j+1 
                
        #then ensure an unbroken hierarchy
        
        result = True
        
        #for each element appart from the last
        
        for i in range (0,len(returnList)-1):
            
            #if it isnt the first one
            
            if i != 0:
                
                #check that  the one bfore is it's direct parent
                
                if returnList[i].getParent() != returnList[i-1]:
                
                    result = False
                    
            #for all, check that the one after is a direct child
            
            if not returnList[i+1] in returnList[i].getChildren():
            
                result = False
                
        #if the result is True, return the list, otherwise return an
        #empty list
        
        if result:
            
            return returnList
        
        else:
            
            return []
        
        """--------------------"""
       
#----------END-RiggingBase-Class----------#  
