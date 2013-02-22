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
        
        returnList = []
        
        #early breakout if no extension is supplied

        if _ext == "":
            
            return _names
            
        for i in range (0, (len(_names))):
            
            #if neither the end of the name nor the start of the extension is an underscore
            
            if _names[i][-1] != "_" and _ext[0] != "_":
                
                #add an underscore to the end of the name
                
                _names[i] = _names[i] + "_"
            
            #if both have one
                
            if _names[i][-1] == "_" and _ext[0] == "_":
                
                #remove the underscore from the start of the extension
                
                _ext = _ext[1:]
                
            #add the extension to the name
            
            returnList.append( _names[i] + _ext)
            
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
            
            returnList = _names
            
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
       
#----------END-RiggingBase-Class----------#  
