#----------Imports----------#

import pymel.core as pm
import pRigging.src.ui.tabbase as ptb
import pRigging.src.ui.tabsettings as pts

#----------ArmTabExperienced-Class----------#

class ArmTabExperienced(ptb.TabBase):
    
    """
        Class: ArmTabExperienced
            A class containing all of the code for generating an arm tab 
            for the Experienced dificulty rating 
        
        File: pRigging/src/ui/armtabexperienced.py
        
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
        
        ptb.TabBase.__init__(self,_parent,_guiInstance,_settings.m_tabName, _settings.m_rigElement, 'arm', _settings.m_baseName)
        
        #-------------name elements generate-------------#
        
        self.m_nameLabel = pm.text(label="Limb Name:", fn = "boldLabelFont")                                    
        self.m_nameOverrideText = pm.textField(tx = _settings.m_limbName, ann = "Enter the name of the rig section here")
        
        #-------------side elements generate-------------#
        
        self.m_sideLabel = pm.text(label="Add side specifier?", fn = "boldLabelFont", al = 'left')
        self.m_sideCheck = pm.checkBox(l = "", v = _settings.m_doSideSpecify, onc = pm.Callback(self.setSideTextEnable, True), ofc = pm.Callback(self.setSideTextEnable, False))
        self.m_sideTextField = pm.textField(tx = _settings.m_sideSpecifier, ann = "Enter the desired side specifier here", en = self.m_sideCheck.getValue())

        #-------------joint loading generate-------------#
        
        self.m_jointToolButton = pm.button(l = "Joint Tool", c = 'pm.runtime.JointTool()')
        self.m_loadJointsButton = pm.button(l = "Load Joints", c = pm.Callback(self.loadJoints))
        self.m_step4Label = pm.text(label="Select twist roots:", fn = "boldLabelFont", al = 'left')
        self.m_jointTable = pm.textScrollList(ams = True)
        
        for tempJnt in _settings.m_jntList:
            self.m_jointTable.append(tempJnt)
            
        self.m_numTwistText = pm.text(label = "Twist joints per chain:")
        self.m_numTwistJntsVal = pm.intField(v = _settings.m_numTwistJnts, ann = "Enter the number of twist joints to\n generate in each twist chain\n ignored if no joints selected to be\n the roots of twist chains")       
        
               
        #-------------Options generate-------------#
                
        self.m_optionsText = pm.text(label="Options:", fn = "boldLabelFont", al= 'left')                          
        
        #-------------initial options generate-------------#
        
        self.m_ikCheck = pm.checkBox(l = "IK", ann = "Generate an IK chain?", v = _settings.m_doIK, onc = pm.Callback(self.setIKTextEnable, True), ofc = pm.Callback(self.setIKTextEnable, False))
        self.m_ikExtText = pm.text(l = "Extension: ") 
        self.m_ikExt = pm.textField(ann = "The extension for the IK chain", tx = _settings.m_ikExt,  en  = self.m_ikCheck.getValue())
        self.m_fkCheck = pm.checkBox(l = "FK", ann = "Generate an FK chain?", v = _settings.m_doFK, onc = pm.Callback(self.setFKTextEnable, True), ofc = pm.Callback(self.setFKTextEnable, False))
        self.m_fkExtText = pm.text(l = "Extension: ")
        self.m_fkExt = pm.textField(ann = "The extension for the FK chain", tx = _settings.m_fkExt,  en  = self.m_fkCheck.getValue())
        
        #-------------additional options generate-------------#
         
        self.m_frame = pm.frameLayout(cll = True, cl = True, l = "Additional options")
        self.m_frameRow = pm.rowColumnLayout(nc = 2)
        pm.text(l = 'Joint Extension:' )
        self.m_jointExt = pm.textField(tx = _settings.m_jntExt)
        pm.text(l = 'Control Extension:')
        self.m_controlExt = pm.textField(tx = _settings.m_ctrlExt)
        pm.setParent(self.m_topLayout)
         
        #-------------final buttons generate-------------# 
                
        self.m_genRigButton = pm.button(l = "Generate Rig", c = pm.Callback(self.genChain))
        self.m_reGenRigButton = pm.button(l = "Regenerate rig", c = pm.Callback(self.reGenChain))
        
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
        
        self.m_topLayout.attachForm(self.m_jointToolButton, 'left', 20)
        self.m_topLayout.attachControl(self.m_jointToolButton, 'top', 20, self.m_sideTextField)
        self.m_topLayout.attachPosition(self.m_jointToolButton, 'right',20,50)
        
        self.m_topLayout.attachForm(self.m_loadJointsButton, 'left', 20)
        self.m_topLayout.attachControl(self.m_loadJointsButton, 'top', 20, self.m_jointToolButton)
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
        
        settings.m_baseName = self.m_rigName
        settings.m_tabName = self.m_topLayout.shortName()
        settings.m_limbName = self.m_nameOverrideText.getText()
        settings.m_doSideSpecify = self.m_sideCheck.getValue()
        settings.m_sideSpecifier = self.m_sideTextField.getText()
        settings.m_jntList = self.m_jointTable.getAllItems()
        settings.m_numTwistJnts = self.m_numTwistJntsVal.getValue()
        settings.m_doIK = self.m_ikCheck.getValue()
        settings.m_ikExt = self.m_ikExt.getText()
        settings.m_doFK = self.m_fkCheck.getValue()
        settings.m_fkExt = self.m_fkExt.getText()
        settings.m_jntExt = self.m_jointExt.getText()
        settings.m_ctrlExt = self.m_controlExt.getText()
        settings.m_rigElement = self.m_rigElement
        
        #delete the ui
        
        pm.deleteUI(self.m_topLayout)
        
        #and return the  settings object
        
        return settings
        
    def setRigRootName(self):
        
        """
            Method: setRigRootName
                A method to set the root name of the rig element
        """
        name = self.m_rigName
        
        if self.m_sideCheck.getValue() == True:
            
            name = self.addExtToNames([name], self.m_sideTextField.getText())[0]
            
        name = self.addExtToNames([name], self.m_nameOverrideText.getText())[0]
        
        self.m_rigElement.setRootName(name)
        
    def setSideTextEnable(self, _val):
        
        """
            Method: setSideTextEnable
                a method to set the enable value on the side text field
                
            Inputs:
                _val:                   The boolean to set the variable to
        """
        
        self.m_sideTextField.setEnable(_val)
        
    def loadJoints(self):
        
        """
            Method: loadJoints
                A method to load the selected joints into the list
                
            On Exit:                The template joints are loaded into the list.
        """
        
        #empty the items loaded into the joint box
        
        self.m_jointTable.removeAll()
        
        selection = pm.ls(sl = True, type = "joint")
        
        for jnt in  selection:
            
            self.m_jointTable.append(jnt)

    def setIKTextEnable(self, _val):
        
        """
            Method: setSideTextEnable
                a method to set the enable value on the side text field
                
            Inputs:
                _val:                   The boolean to set the variable to
        """
        
        self.m_ikExt.setEnable(_val)
        
    def setFKTextEnable(self, _val):
        
        """
            Method: setSideTextEnable
                a method to set the enable value on the side text field
                
            Inputs:
                _val:                   The boolean to set the variable to
        """
        
        self.m_fkExt.setEnable(_val)

    def genChain(self):
        
        """
            Method: genChain
                A method to generate the joint chain
        """
        
        #create a list of the unicode strings representing
        #the selected joints and an empty list for their
        #pynode counterparts
        
        strList = self.m_jointTable.getAllItems()
        pyNodeList = []
        
        #cycle through and convert to pyNode
        
        for jnt in strList:
            
            pyNodeList.append(pm.PyNode(jnt))
            
        #check that there are some joints
        
        if pyNodeList == []:
            
            #currently print, will be refactored to use the help box
            
            print ["ERROR","NO JOINTS","ERROR: No joints were passed in to generate the rig from"]
            
        #otherwise continue with the generation
        
        else:
        
            #enfoce the hierarchy
            
            pyNodeList = self.enforceHierarchy(pyNodeList)
            
            #now check if there is any nodes in the joint list
            
            if pyNodeList == []:
                
                #temp print, will use the help box eventually
                
                print ["ERROR","INCORRECT HIERARCHY","ERROR: The joints selected were not in a single hierarchy, either a joint was missing or one of them had two immediate children in the selection with it"]
            
            else:

            
                #get a list of the selected items
                
                twistRootList = self.m_jointTable.getSelectItem()
                
                #variable defining whether or not to generate a twist chain
                
                doTwist = True
                
                if twistRootList == []:
                
                    doTwist = False
                
                #generate a list for the twist root indices
                
                indexList = []
                
                #then cycle through the ordered pynode list
                
                for i in range (0, len(pyNodeList)-1):
                                
                    #cycle through all of the selected joints
                    
                    for jnt in twistRootList:
                        
                        #if they are the same, add the id into the list
                        
                        if jnt == pyNodeList[i]:
                            
                            indexList.append(i)
                            
                #and set the root name for the arm
                
                self.m_rigElement.setRootName(self.addExtToNames(self.addExtToNames([self.m_rigName],self.m_sideTextField.getText()),self.m_nameOverrideText.getText())[0])
                
                result = self.m_rigElement.genArmRig(pyNodeList,
                            _doIK = self.m_ikCheck.getValue(),
                            _ikExt = self.m_ikExt.getText(),
                            _doFK = self.m_fkCheck.getValue(),
                            _fkExt = self.m_fkExt.getText(),
                            _jntExt = self.m_jointExt.getText(),
                            _ctrlExt = self.m_controlExt.getText(),
                            _doTwist = doTwist, 
                            _twistStartIds = indexList,
                            _numTwistJnts =  self.m_numTwistJntsVal.getValue()
                            )
                    
        #############DEAL WITH RESULT##################
        
        
    def reGenChain(self):
        
        """
            Method: reGenChain
                A method to regenerate the chain based on a new set of parameters
        """
        
        self.m_rigElement.clear()
        self.genChain()
#----------END-ArmTabExperienced-Class----------#       
