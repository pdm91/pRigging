#----------Imports----------#

import pymel.core as pm
import pRigging.src.riggingbase as prb

#----------StartTabNovice-Class----------#

class StartTabNovice(prb.RiggingBase):
    
    """
        Class: StartTabNovice
            A class containing all of the code for generating the initial tab 
            for the novice dificulty rating 
        
        File: pRigging/src/ui/starttabnovice.py
        
        Contains:
            self.m_topLayout

        Imports:
            pymel.core as pm
            pRigging.src.riggingbase as prb     
    """
    
    def __init__(self,_parent,_guiInstance,_name):
        
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
        """
        
        #set the parent ui 
        
        pm.setParent(_parent)
        
        #and store a pointer to the gui instance for calling parent methods to add a tab 
        
        self.m_gui = _guiInstance
        
        #check if the name exists, if it does, add a number to make it unique
        
        result = False
             
        i = 1
                
        while not result:
                
            if pm.formLayout(_name, q = True, ex = True):
            
                _name = self.addExtToNames(self.removeExtFromNames([_name]), str(i))[0]
                
            else:
                
                result = True
                    
            i = i+1
        
        #set the layout
        
        self.m_topLayout =  pm.formLayout(_name, numberOfDivisions = 100)
        
        #add text
        
        self.m_step1Label = pm.text(label="Step1:", fn = "boldLabelFont")
        self.m_step1Text = pm.text(label = "Set the name for the rig", 
                                    ann = "Enter the name below, this name can be changed at any point",
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    ww = True)

        #rig label and name text field                   
        
        self.m_rigLabel = pm.text(label="Rig Name:")
        self.m_rigName = pm.textField(tx = "Rig",ann = "Enter the name of the rig here")
        
        #add more text
        
        self.m_step2Label = pm.text(label="Step2:", fn = "boldLabelFont")
        self.m_step2Text = pm.text(label = "Add a rig section", 
                                    ann = "click on on of the buttons below",
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    ww = True)
        
        #add buttons
        
        self.m_addArmButton = pm.button(l = "Add Arm", c= pm.Callback(self.m_gui.addTab, "arm"))
        
        self.m_addLegButton = pm.button(l = "Add Leg",c= pm.Callback(self.m_gui.addTab, "leg"))
        
        #attach the first text to the form
        
        self.m_topLayout.attachForm(self.m_step1Label, 'left', 20)
        self.m_topLayout.attachForm(self.m_step1Text, 'right', 20)
        self.m_topLayout.attachForm(self.m_step1Label, 'top', 20)
        self.m_topLayout.attachForm(self.m_step1Text,'top', 20)
        
        self.m_topLayout.attachControl(self.m_step1Text, 'left', 5, self.m_step1Label)
        
        #and then the rig label and name
        
        self.m_topLayout.attachForm(self.m_rigLabel, 'left', 30)
        self.m_topLayout.attachForm(self.m_rigName, 'right', 20)
                                  
        self.m_topLayout.attachControl(self.m_rigName, 'left', 5, self.m_rigLabel)
        self.m_topLayout.attachControl(self.m_rigName, 'top', 17, self.m_step1Text)
        self.m_topLayout.attachControl(self.m_rigLabel, 'top', 20, self.m_step1Text)
        
        #then the next text
        
        self.m_topLayout.attachControl(self.m_step2Text, 'left', 5, self.m_step2Label)
        
        self.m_topLayout.attachForm(self.m_step2Label, 'left', 20)
        self.m_topLayout.attachForm(self.m_step2Text, 'right', 20)
        
        self.m_topLayout.attachControl(self.m_step2Label, 'top', 20, self.m_rigName)
        self.m_topLayout.attachControl(self.m_step2Text, 'top', 20, self.m_rigName)
        
        #then the buttons
        
        self.m_topLayout.attachForm(self.m_addArmButton, 'left', 30)
        self.m_topLayout.attachForm(self.m_addArmButton, 'right', 20)
        
        self.m_topLayout.attachControl(self.m_addArmButton, 'top', 20, self.m_step2Text)
        
        self.m_topLayout.attachForm(self.m_addLegButton, 'left', 30)
        self.m_topLayout.attachForm(self.m_addLegButton, 'right', 20)
        
        self.m_topLayout.attachControl(self.m_addLegButton, 'top', 20, self.m_addArmButton)
        
    def getRigName(self):
        
        """
            Method: getRigName
                A method to retun the current contents of the name text field
                
            On Exit: returns the text
        """        
                                    
        return self.m_rigName.getText()
                                     

#----------END-StartTabNovice-Class----------#       