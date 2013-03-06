#----------Imports----------#

import pymel.core as pm
import pRigging.src.riggingbase as prb

#----------TabBase-Class----------#

class TabBase(prb.RiggingBase):
    
    """
        Class: TabBase
            A base class for all of the tab layouts
        
        File: pRigging/src/ui/tabbase.py
        
        Contains:
            self.m_type:            A variable to store the limb type
                                    used when rebuilding tabs due to a 
                                    change in skill level
            self.m_gui:             The instance of the gui class that 
                                    generated the tab
            self.m_name:            The name of the top layout which 
                                    contains all of the ui elements stored 
                                    within the tab
            self.m_topLayout:       The instance of the form layout which is
                                    the top-most layout of the tab ui
            self.m_rigElement:      The rig element that the tab relates to

        Imports:
            pymel.core as pm
            pRigging.src.riggingbase as prb     
    """
    
    def __init__(self,_parent,_guiInstance,_name, _rigElement, _type, _baseName):
        
        """
            Method: __init__
                A method called when the class is instanciated, sets up the attributes
            
            Inputs:
                self:                   A pointer to the instance of the object being
                                        created.
                _parent:                The parent ui element for the layout
                _guiInstance:           The instance of the GUI class
                _name:                  The name to attempt to call the tab, a unique
                                        name will be generated if the one passed in cannot be used
                _arm:                   The rig Component passed in by the ui
                _type:                  The type of tab that is being created
        """
        
        #set the type of the tab
        
        self.m_type = _type
        
        #set the parent ui 
        
        pm.setParent(_parent)
        
        #and store a pointer to the gui instance for calling parent methods to add a tab 
        
        self.m_gui = _guiInstance
        
        #check if the name exists, if it does, add a number to make it unique
        
        result = False
        
        #store the name
        
        self.m_name = _name
             
        i = 1
                
        while not result:
                
            if pm.formLayout(self.m_name, q = True, ex = True):
            
                self.m_name = self.addExtToNames(self.removeExtFromNames([self.m_name]), str(i))[0]
                
            else:
                
                result = True
                    
            i = i+1
        
        #set the layout
        
        self.m_topLayout =  pm.formLayout(self.m_name, numberOfDivisions = 100)
        
        #set up the rig component
        
        self.m_rigElement = _rigElement
        
        #store the rig base name and the side specifier
        
        self.m_rigName = _baseName
        
    def getTabType(self):
        
        """
            Method: getType
                A method to return the type of the tab

            On Exit:                Returns the type string
            
        """
        
        return self.m_type
                                       

#----------END-TabBase-Class----------#       
