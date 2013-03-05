#----------Imports----------#

import pymel.core as pm
import pRigging.src.ui.tabbase as ptb
import pRigging.src.ui.tabsettings as pts

#----------ArmTabIntermediate-Class----------#

class ArmTabIntermediate(ptb.TabBase):
    
    """
        Class: ArmTabIntermediate
            A class containing all of the code for generating an arm tab 
            for the intermediate dificulty rating 
        
        File: pRigging/src/ui/armtabintermediate.py
        
        Contains:
            self.m_topLayout

        Imports:
            pymel.core as pm
            pRigging.src.ui.tabbase as ptb
            pRigging.src.ui.tabsettings as pts
    """
    
    def __init__(self,_parent,_guiInstance, _settings):
        
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
        
        #initialise the base class
        
        ptb.TabBase.__init__(self,_parent,_guiInstance,_settings.m_tabName, _settings.m_rigElement, 'arm')
        
        #and initialise variables to stor the settings that are not stores by a ui element
        
        self.m_doSideSpecify = _settings.m_doSideSpecify
        self.m_sideSpecifier = _settings.m_sideSpecifier
        self.m_ikExt = _settings.m_ikExt
        self.m_fkExt = _settings.m_fkExt
        self.m_jntExt = _settings.m_jntExt
        self.m_ctrlExt = _settings.m_ctrlExt
        
        #-------------step 1 text generate-------------#
        
        self.m_step1Label = pm.text(label="1:", fn = "boldLabelFont")
        self.m_step1Text = pm.text(label = "Build the joints", 
                                    ann = "Build the template joint chain for your arm, \ndon't worry about twist joints",
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    w = 120,
                                    ww = True)
                                    
        
        #-------------step 1 control generate-------------#
        
        self.m_jointToolButton = pm.button(l = "Joint Tool")
        
        #-------------step 2 text generate-------------#
        
        self.m_step2Label = pm.text(label="2:", fn = "boldLabelFont")
        self.m_step2Text = pm.text(label = "Override limb name?", 
                                    ann = "Can be left at Arm if you wish",
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    w = 120,
                                    ww = True)
        
        #-------------step 2 control generate-------------#
        
        self.m_nameOverrideCheck =  pm.checkBox(ann = "override the limb name?", v = False, l = "")
        self.m_nameOverrideText = pm.textField(tx = _settings.m_limbName, ann = "Enter the name of the rig here", en = False)
        
        #-------------step 3 text generate-------------#
        
        self.m_step3Label = pm.text(label="3:", fn = "boldLabelFont")
        self.m_step3Text = pm.text(label = "Select and load the template joints", 
                                    ann = "The joints must be in an unbroken and single hirerarchy\n there must not be more than one child of any selected\n joint also selected",
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    h = 20,
                                    ww = True)
                                    
        #-------------step 3 control generate-------------#
        
        self.m_jointTable = pm.textScrollList()
        
        for tempJnt in _settings.m_jntList:
            self.m_jointTable.append(tempJnt)
        
        self.m_loadJointsButton = pm.button(l = "Load Joints")
        
        #-------------step 4 text generate-------------#
                
        self.m_step4Label = pm.text(label="4:", fn = "boldLabelFont")
        self.m_step4Text = pm.text(label = "Select, in the boxbelow, which joints, if any, you want to be the root of a twist chain",
                                    ann = "Note: If the last joint is selected \nit will be disregarded as it not \nwithin the scope of this joint chain", 
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    h = 20,
                                    ww = True)
        
        #-------------step 5 text generate-------------#
                
        self.m_step5Label = pm.text(label="5:", fn = "boldLabelFont")
        self.m_step5Text = pm.text(label = "Select options and generate",
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    h = 20,
                                    ww = True)
        
        #-------------step 5 control generate-------------#
        
        self.m_ikCheck = pm.checkBox(l = "IK", ann = "Generate an IK chain?", v = _settings.m_doIK)
        self.m_fkCheck = pm.checkBox(l = "FK", ann = "Generate an FK chain?", v = _settings.m_doFK)
        
        self.m_numTwistText = pm.text(label = "Number of twist joints to be generated:",
                                    al = "left",
                                    ann = "Enter the number of twist joints to\n generate in each twist chain\n ignored if no joints selected to be\n the roots of twist chains",
                                    fn = "smallBoldLabelFont",
                                    h = 20,
                                    ww = True)
        self.m_numTwistJntsVal = pm.intField(v = _settings.m_numTwistJnts, ann = "Enter the number of twist joints to\n generate in each twist chain\n ignored if no joints selected to be\n the roots of twist chains")       
                
        self.m_genRigButton = pm.button(l = "Generate Rig")
        self.m_reGenRigButton = pm.button(l = "Regenerate rig")
        
        #-------------misc control generate-------------#
        
        self.m_closeButton = pm.button(l = "Close Tab")
        

        #-------------step 1 text attach-------------#
        
        self.m_topLayout.attachForm(self.m_step1Label, 'left', 20)
        self.m_topLayout.attachForm(self.m_step1Label, 'top', 22)
        self.m_topLayout.attachForm(self.m_step1Text,'top', 22)
        
        self.m_topLayout.attachControl(self.m_step1Text,'left', 20, self.m_step1Label)
        
        #-------------step 1 controls attach-------------#
        
        self.m_topLayout.attachForm(self.m_jointToolButton, 'top', 20)
        self.m_topLayout.attachForm(self.m_jointToolButton, 'right', 20)
        
        self.m_topLayout.attachControl(self.m_jointToolButton, 'left', 20, self.m_step1Text)
        
        #-------------step 2 text attach-------------#
        
        self.m_topLayout.attachForm(self.m_step2Label, 'left', 20)       
        self.m_topLayout.attachControl(self.m_step2Label, 'top', 20, self.m_jointToolButton)
      
        self.m_topLayout.attachControl(self.m_step2Text, 'top', 23, self.m_jointToolButton)
        self.m_topLayout.attachControl(self.m_step2Text, 'left', 20, self.m_step2Label)
        
        #-------------step 2 control attach-------------#
        
        self.m_topLayout.attachControl(self.m_nameOverrideCheck,'left', 20, self.m_step2Text)
        self.m_topLayout.attachControl(self.m_nameOverrideCheck,'top',23,self.m_jointToolButton)

        self.m_topLayout.attachControl(self.m_nameOverrideText,'left', 20, self.m_nameOverrideCheck)
        self.m_topLayout.attachControl(self.m_nameOverrideText,'top',20,self.m_jointToolButton)
        
        self.m_topLayout.attachForm(self.m_nameOverrideText, 'right', 20)
        
        #-------------step 3 text attach-------------#
        
        self.m_topLayout.attachForm(self.m_step3Label, 'left', 20)       
        self.m_topLayout.attachControl(self.m_step3Label, 'top', 20, self.m_nameOverrideText)

        self.m_topLayout.attachPosition(self.m_step3Text, 'right', 20, 50)       
        self.m_topLayout.attachControl(self.m_step3Text, 'top', 20, self.m_nameOverrideText)
        self.m_topLayout.attachControl(self.m_step3Text, 'left', 20, self.m_step3Label)
        
        
        #-------------step 3 control attach-------------#
        
        self.m_topLayout.attachForm(self.m_jointTable, 'left', 30)
        self.m_topLayout.attachPosition(self.m_jointTable, 'right', 20, 50)
        self.m_topLayout.attachForm(self.m_jointTable,'bottom', 20)
        self.m_topLayout.attachControl(self.m_jointTable,'top', 20, self.m_step4Text)
                
        self.m_topLayout.attachForm(self.m_loadJointsButton, 'left', 20)
        self.m_topLayout.attachControl(self.m_loadJointsButton, 'right', 20, self.m_genRigButton)
        self.m_topLayout.attachControl(self.m_loadJointsButton, 'top', 20,self.m_step3Text)
        
        
        #-------------step 4 text attach-------------#
        
        self.m_topLayout.attachForm(self.m_step4Label, 'left', 20)
        self.m_topLayout.attachControl(self.m_step4Label, 'top', 20, self.m_loadJointsButton)
        
        self.m_topLayout.attachControl(self.m_step4Text, 'top', 20, self.m_loadJointsButton)
        self.m_topLayout.attachControl(self.m_step4Text, 'left', 20, self.m_step4Label)
        self.m_topLayout.attachControl(self.m_step4Text, 'right', 20, self.m_closeButton)
        
        #-------------step 5 text attach-------------#
        
        self.m_topLayout.attachPosition(self.m_step5Label, "left", 20,50)
        self.m_topLayout.attachControl(self.m_step5Label, "top", 20, self.m_nameOverrideText) 
        
        self.m_topLayout.attachControl(self.m_step5Text, "left", 20,self.m_step5Label)
        self.m_topLayout.attachControl(self.m_step5Text, "top", 20, self.m_nameOverrideText)
        self.m_topLayout.attachForm(self.m_step5Text, 'right', 20)  
        
        #-------------step 5 control attach-------------#
        
        self.m_topLayout.attachForm(self.m_ikCheck, 'right',20)
        self.m_topLayout.attachForm(self.m_fkCheck, 'right',20)
                
        self.m_topLayout.attachPosition(self.m_ikCheck, 'left' , 40 , 50)
        self.m_topLayout.attachPosition(self.m_fkCheck, 'left' , 40 , 50)
        
        self.m_topLayout.attachControl(self.m_ikCheck, 'top', 10, self.m_step5Text)
        self.m_topLayout.attachControl(self.m_fkCheck, 'top', 10, self.m_ikCheck)
        
        self.m_topLayout.attachPosition(self.m_numTwistText, 'left', 40, 50)
        self.m_topLayout.attachControl(self.m_numTwistText, 'top', 20, self.m_fkCheck)
        
        self.m_topLayout.attachControl(self.m_numTwistText, 'right', 20 ,self.m_numTwistJntsVal)
        
        self.m_topLayout.attachForm(self.m_numTwistJntsVal, 'right', 20)
        self.m_topLayout.attachControl(self.m_numTwistJntsVal, 'top', 20, self.m_fkCheck)
        
        self.m_topLayout.attachForm(self.m_genRigButton, 'right', 20)
        self.m_topLayout.attachPosition(self.m_genRigButton, 'left', 20, 50)
        self.m_topLayout.attachControl(self.m_genRigButton, 'bottom', 20,self.m_reGenRigButton)
        
        self.m_topLayout.attachForm(self.m_reGenRigButton, 'right', 20)
        self.m_topLayout.attachPosition(self.m_reGenRigButton, 'left', 20, 50)
        self.m_topLayout.attachControl(self.m_reGenRigButton, 'bottom', 20, self.m_closeButton)
                
        #-------------misc control attach-------------#
                
        self.m_topLayout.attachForm(self.m_closeButton, 'right', 20)
        self.m_topLayout.attachPosition(self.m_closeButton, 'left', 20, 50)
        self.m_topLayout.attachForm(self.m_closeButton, 'bottom', 20)
        
        
    def clearTab(self):
        
        """
            Method: clearTab
                A method to clear out the tab, returns a TabSettings object
                
            On Exit:                The tab has been removed, and the uiElements
                                    deleted, and a settins object returned to 
                                    allow for continuity of choices across user
                                    skill levels
        """
        
        #generate a TabSettings object
                                    
        settings = pts.TabSettings()
        
        #store the appropriate values in the TabSettings Object
        
        settings.m_tabName = self.m_topLayout.shortName()
        settings.m_limbName = self.m_nameOverrideText.getText()
        settings.m_doSideSpecify = self.m_doSideSpecify
        settings.m_sideSpecifier = self.m_sideSpecifier
        settings.m_jntList = self.m_jointTable.getAllItems()
        settings.m_numTwistJnts = self.m_numTwistJntsVal.getValue()
        settings.m_doIK = self.m_ikCheck.getValue()
        settings.m_ikExt = self.m_ikExt
        settings.m_doFK = self.m_fkCheck.getValue()
        settings.m_fkExt = self.m_fkExt
        settings.m_jntExt = self.m_jntExt
        settings.m_ctrlExt = self.m_ctrlExt
        settings.m_rigElement = self.m_rigElement
        
        #delete the ui
        
        pm.deleteUI(self.m_topLayout)
        
        #and return the  settings object
        
        return settings
        

                                     

#----------END-ArmTabIntermediate-Class----------#       