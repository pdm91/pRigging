#----------Imports----------#

import pymel.core as pm
import pRigging.src.riggingbase as prb

#----------ArmTabExperienced-Class----------#

class ArmTabExperienced(prb.RiggingBase):
    
    """
        Class: ArmTabExperienced
            A class containing all of the code for generating an arm tab 
            for the Experienced dificulty rating 
        
        File: pRigging/src/ui/armtabexperienced.py
        
        Contains:
            self.m_topLayout

        Imports:
            pymel.core as pm
            pRigging.src.riggingbase as prb     
    """
    
    def __init__(self,_parent,_guiInstance,_name, _arm, _sideString):
        
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
                
            if pm.formLayout(self.m_name, q = True, ex = True):
            
                self.m_name = self.addExtToNames(self.removeExtFromNames([self.m_name]), str(i))[0]
                
            else:
                
                result = True
                    
            i = i+1
        
        #set the layout
        
        self.m_topLayout =  pm.formLayout(self.m_name, numberOfDivisions = 100)
        
        #set up the rig component
        
        self.m_arm = _arm
        
        #add text
        
        #-------------name elements generate-------------#
        
        self.m_nameLabel = pm.text(label="Limb Name:", fn = "boldLabelFont")                                    
        self.m_nameOverrideText = pm.textField(tx = "Arm", ann = "Enter the name of the rig section here")
        
        #-------------side elements generate-------------#
        
        self.m_sideLabel = pm.text(label="Add side specifier?", fn = "boldLabelFont", al = 'left')
        self.m_sideCheck = pm.checkBox(l = "", v = True)
        self.m_sideTextField = pm.textField(tx = _sideString, ann = "Enter the desired side specifier here")

        #-------------joint loading generate-------------#
        self.m_loadJointsButton = pm.button(l = "Load Joints")
        self.m_step4Label = pm.text(label="Select twist roots:", fn = "boldLabelFont", al = 'left')
        self.m_jointTable = pm.textScrollList()
        self.m_numTwistText = pm.text(label = "Twist joints per chain:")
        self.m_numTwistJntsVal = pm.intField(v = 3, ann = "Enter the number of twist joints to\n generate in each twist chain\n ignored if no joints selected to be\n the roots of twist chains")       
        
               
        #-------------Options generate-------------#
                
        self.m_optionsText = pm.text(label="Options:", fn = "boldLabelFont", al= 'left')                          
        
        #-------------initial options generate-------------#
        
        self.m_ikCheck = pm.checkBox(l = "IK", ann = "Generate an IK chain?", v = True)
        self.m_ikExtText = pm.text(l = "Extension: ") 
        self.m_ikExt = pm.textField(ann = "The extension for the IK chain", tx = "IK")
        self.m_fkCheck = pm.checkBox(l = "FK", ann = "Generate an FK chain?", v = True)
        self.m_fkExtText = pm.text(l = "Extension: ")
        self.m_fkExt = pm.textField(ann = "The extension for the FK chain", tx = "FK")
        
        #-------------additional options generate-------------#
         
        self.m_frame = pm.frameLayout(cll = True, cl = True, l = "Additional options")
        self.m_frameRow = pm.rowColumnLayout(nc = 2)
        pm.text(l = 'Joint Extension:' )
        self.m_jointExt = pm.textField(tx = "JNT")
        pm.text(l = 'Control Extension:')
        self.m_ControlExt = pm.textField(tx = "CTRL")
        pm.setParent(self.m_topLayout)
         
        #-------------final buttons generate-------------# 
                
        self.m_genRigButton = pm.button(l = "Generate Rig")
        self.m_reGenRigButton = pm.button(l = "Regenerate rig")
        
        #-------------misc control generate-------------#
        
        self.m_closeButton = pm.button(l = "Close Tab")
        
        #-------------name elements attach-------------#
        
        self.m_topLayout.attachForm(self.m_nameLabel, 'left',20)
        self.m_topLayout.attachForm(self.m_nameLabel, 'top',23)
        
        self.m_topLayout.attachForm(self.m_nameOverrideText, 'top', 20)
        self.m_topLayout.attachControl(self.m_nameOverrideText, 'left', 20, self.m_nameLabel)
        self.m_topLayout.attachPosition(self.m_nameOverrideText, 'right', 20,50)
        
        #-------------side elements attach-------------#
        
        self.m_topLayout.attachForm(self.m_sideLabel, 'left', 20)
        self.m_topLayout.attachControl(self.m_sideLabel, 'top', 20, self.m_nameOverrideText)
        self.m_topLayout.attachPosition(self.m_sideLabel, 'right', 20, 50)
                
        self.m_topLayout.attachForm(self.m_sideCheck, 'left', 20)
        self.m_topLayout.attachControl(self.m_sideCheck, 'top', 23, self.m_sideLabel)
        
        self.m_topLayout.attachControl(self.m_sideTextField, 'left', 20, self.m_sideCheck)
        self.m_topLayout.attachControl(self.m_sideTextField, 'top', 20, self.m_sideLabel)
        self.m_topLayout.attachPosition(self.m_sideTextField, 'right',20,50)
        
        #-------------joint loading attach-------------#
        
        self.m_topLayout.attachForm(self.m_loadJointsButton, 'left', 20)
        self.m_topLayout.attachControl(self.m_loadJointsButton, 'top', 20, self.m_sideTextField)
        self.m_topLayout.attachPosition(self.m_loadJointsButton, 'right',20,50)
        
        self.m_topLayout.attachForm(self.m_step4Label , 'left', 20)
        self.m_topLayout.attachControl(self.m_step4Label , 'top', 20, self.m_loadJointsButton)
        self.m_topLayout.attachPosition(self.m_step4Label , 'right',20,50)
        
        self.m_topLayout.attachForm(self.m_jointTable, 'left', 20)
        self.m_topLayout.attachControl(self.m_jointTable , 'top', 20, self.m_step4Label )
        self.m_topLayout.attachPosition(self.m_jointTable , 'right',20,50)
        self.m_topLayout.attachControl(self.m_jointTable, 'bottom', 20,self.m_numTwistJntsVal)
        
        self.m_topLayout.attachForm(self.m_numTwistText, 'left', 20)
        self.m_topLayout.attachForm(self.m_numTwistText, 'bottom', 23)
        
        self.m_topLayout.attachControl(self.m_numTwistJntsVal , 'left', 20, self.m_numTwistText)
        self.m_topLayout.attachPosition(self.m_numTwistJntsVal  , 'right',20,50)
        self.m_topLayout.attachForm(self.m_numTwistJntsVal , 'bottom', 20)
        
        #-------------Options attach-------------#
        
        self.m_topLayout.attachForm(self.m_optionsText, 'top', 20)
        self.m_topLayout.attachForm(self.m_optionsText, 'right', 20)
        self.m_topLayout.attachPosition(self.m_optionsText, 'left',20,50)        
        
        #-------------initial options generate-------------#
        
        self.m_topLayout.attachPosition(self.m_ikCheck, 'left',20,50)
        self.m_topLayout.attachControl(self.m_ikCheck, 'top', 20, self.m_optionsText)
        
        self.m_topLayout.attachControl(self.m_ikExtText, 'left', 20, self.m_ikCheck)
        self.m_topLayout.attachControl(self.m_ikExtText, 'top', 20, self.m_optionsText)
        
        self.m_topLayout.attachControl(self.m_ikExt, 'left', 20, self.m_ikExtText)
        self.m_topLayout.attachControl(self.m_ikExt, 'top', 20, self.m_optionsText)
        self.m_topLayout.attachForm(self.m_ikExt, 'right', 20)

        self.m_topLayout.attachPosition(self.m_fkCheck, 'left',20,50)
        self.m_topLayout.attachControl(self.m_fkCheck, 'top', 20, self.m_ikExt)
        
        self.m_topLayout.attachControl(self.m_fkExtText, 'left', 20, self.m_fkCheck)
        self.m_topLayout.attachControl(self.m_fkExtText, 'top', 20, self.m_ikExt)
        
        self.m_topLayout.attachControl(self.m_fkExt, 'left', 20, self.m_fkExtText)
        self.m_topLayout.attachControl(self.m_fkExt, 'top', 20, self.m_ikExt)        
        self.m_topLayout.attachForm(self.m_fkExt, 'right', 20)
        
        #-------------additional options generate-------------#
         
        self.m_topLayout.attachPosition(self.m_frame, 'left',20,50)
        self.m_topLayout.attachForm(self.m_frame, 'right',20)
        self.m_topLayout.attachControl(self.m_frame, 'top',20,self.m_fkExt)
        self.m_topLayout.attachControl(self.m_frame, 'bottom',20,self.m_genRigButton)
        
        #-------------final buttons generate-------------# 
        
        self.m_topLayout.attachForm(self.m_genRigButton, 'right', 20)
        self.m_topLayout.attachPosition(self.m_genRigButton, 'left', 20, 50)
        self.m_topLayout.attachControl(self.m_genRigButton, 'bottom', 20,self.m_reGenRigButton)
        
        self.m_topLayout.attachForm(self.m_reGenRigButton, 'right', 20)
        self.m_topLayout.attachPosition(self.m_reGenRigButton, 'left', 20, 50)
        self.m_topLayout.attachControl(self.m_reGenRigButton, 'bottom', 20, self.m_closeButton)
        
        #-------------misc control generate-------------#
        
        self.m_topLayout.attachPosition(self.m_closeButton, 'left', 20,50)
        self.m_topLayout.attachForm(self.m_closeButton, 'bottom',20)
        self.m_topLayout.attachForm(self.m_closeButton, 'right', 20)
                                             

#----------END-ArmTabExperienced-Class----------#       