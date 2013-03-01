#----------Imports----------#

import pymel.core as pm
import pRigging.src.riggingbase as prb

#----------ArmTabNovice-Class----------#

class ArmTabNovice(prb.RiggingBase):
    
    """
        Class: ArmTabNovice
            A class containing all of the code for generating an arm tab 
            for the novice dificulty rating 
        
        File: pRigging/src/ui/armtabnovice.py
        
        Contains:
            self.m_topLayout

        Imports:
            pymel.core as pm
            pRigging.src.riggingbase as prb     
    """
    
    def __init__(self,_parent,_guiInstance,_name, _arm):
        
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
        """
        
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
                
            if pm.formLayout(_name, q = True, ex = True):
            
                self.m_name = self.addExtToNames(self.removeExtFromNames([self.m_name]), str(i))[0]
                
            else:
                
                result = True
                    
            i = i+1
        
        #set the layout
        
        self.m_topLayout =  pm.formLayout(self.m_name, numberOfDivisions = 100)
        
        #set up the rig component
        
        self.m_arm = _arm
        
        #add text
        
        self.m_step1Label = pm.text(label="Arm", fn = "boldLabelFont")
        self.m_step1Text = pm.text(label = "Set the name for the rig", 
                                    ann = "Enter the name below, this name can be changed at any point",
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    ww = True)
        
        self.m_addArmButton = pm.button(l = "Add Arm", c= pm.Callback(self.m_gui.addTab, "arm"))
        
        self.m_addLegButton = pm.button(l = "Add Leg",c= pm.Callback(self.m_gui.addTab, "leg"))
        
        #attach the first text to the form
        
        self.m_topLayout.attachForm(self.m_step1Label, 'left', 20)
        self.m_topLayout.attachForm(self.m_step1Text, 'right', 20)
        self.m_topLayout.attachForm(self.m_step1Label, 'top', 20)
        self.m_topLayout.attachForm(self.m_step1Text,'top', 20)
        
        
        self.m_topLayout.attachForm(self.m_addArmButton, 'left', 30)
        self.m_topLayout.attachForm(self.m_addArmButton, 'right', 20)
        
        self.m_topLayout.attachControl(self.m_addArmButton, 'top', 20, self.m_step1Text)
        
        self.m_topLayout.attachForm(self.m_addLegButton, 'left', 30)
        self.m_topLayout.attachForm(self.m_addLegButton, 'right', 20)
        
        self.m_topLayout.attachControl(self.m_addLegButton, 'top', 20, self.m_addArmButton)
        
                                     

#----------END-ArmTabNovice-Class----------#       