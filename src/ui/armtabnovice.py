#----------Imports----------#

import pymel.core as pm
import pRigging.src.ui.tabbase as ptb
import pRigging.src.ui.tabsettings as pts

#----------ArmTabNovice-Class----------#

class ArmTabNovice(ptb.TabBase):
    
    """
        Class: ArmTabNovice
            A class containing all of the code for generating an arm tab 
            for the novice dificulty rating 
        
        File: pRigging/src/ui/armtabnovice.py
        
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
        
        #initialise variable to stor settings that are not stored in ui elements
        
        self.m_limbName = _settings.m_limbName
        self.m_doSideSpecify = _settings.m_doSideSpecify
        self.m_sideSpecifier = _settings.m_sideSpecifier
        self.m_numTwistJnts = _settings.m_numTwistJnts 
        self.m_ikExt = _settings.m_ikExt
        self.m_fkExt = _settings.m_fkExt 
        self.m_jntExt = _settings.m_jntExt 
        self.m_ctrlExt = _settings.m_ctrlExt 
                
        #-------------step 1 text generate-------------#
        
        self.m_step1Label = pm.text(label="Step 1:", fn = "boldLabelFont")
        self.m_step1Text = pm.text(label = "Build the template joint chain for your arm", 
                                    ann = "At this point, I can't really help, you need to at least know where you want the joints",
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    ww = True)
                                    
        self.m_note1Text = pm.text(label = "Note: There is no need to build twist joints, these will be generated by the tool if you set that option", 
                                    al = "left",
                                    h = 20,
                                    fn = "smallPlainLabelFont",
                                    ww = True)
        
        #-------------step 1 control generate-------------#
        
        self.m_jointToolButton = pm.button(l = "Joint Tool", c = 'pm.runtime.JointTool()')
        
        #-------------step 2 text generate-------------#
        
        self.m_step2Label = pm.text(label="Step 2:", fn = "boldLabelFont")
        self.m_step2Text = pm.text(label = "Select the joints and load them into the box below", 
                                    ann = "The joints must be in an unbroken and single hirerarchy\n there must not be more than one child of any selected\n joint also selected",
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    h = 20,
                                    ww = True)
        
        #-------------step 3 text generate-------------#
                
        self.m_step3Label = pm.text(label="Step 3:", fn = "boldLabelFont")
        self.m_step3Text = pm.text(label = "Select the options and Generate", 
                                    al = "left",
                                    fn = "smallBoldLabelFont",
                                    h = 20,
                                    ww = True)
                                    
        #-------------step 2 control generate-------------#
        
        self.m_jointTable = pm.textScrollList(en = False)
        
        for tempJnt in _settings.m_jntList:
            self.m_jointTable.append(tempJnt)
            
        self.m_loadJointsButton = pm.button(l = "Load Joints", c = pm.Callback(self.loadJoints))
        
        #-------------step 3 control generate-------------#
        
        self.m_ikCheck = pm.checkBox(l = "IK", ann = "Generate an IK chain?", v = _settings.m_doIK)
        self.m_fkCheck = pm.checkBox(l = "FK", ann = "Generate an FK chain?", v = _settings.m_doFK)
        self.m_twistCheck = pm.checkBox(l = "Forearm Twist", ann = "Add a forearm twist chain?", v = True)        
        
        self.m_genRigButton = pm.button(l = "Generate Rig", c = pm.Callback(self.genChain))
        
        #-------------misc control generate-------------#
        
        self.m_closeButton = pm.button(l = "Close Tab")
        

        #-------------step 1 text attach-------------#
        
        self.m_topLayout.attachForm(self.m_step1Label, 'left', 20)
        self.m_topLayout.attachForm(self.m_step1Text, 'right', 20)
        self.m_topLayout.attachForm(self.m_step1Label, 'top', 20)
        self.m_topLayout.attachForm(self.m_step1Text,'top', 20)
        
        self.m_topLayout.attachControl(self.m_step1Text,'left', 20, self.m_step1Label)
        
        self.m_topLayout.attachForm(self.m_note1Text, 'left', 30)
        self.m_topLayout.attachForm(self.m_note1Text, 'right', 20)
        
        self.m_topLayout.attachControl(self.m_note1Text, 'top', 10, self.m_step1Text)
        
        self.m_topLayout.attachPosition(self.m_note1Text, 'bottom', 5, 20)
        
        #-------------step 1 controls attach-------------#
        
        self.m_topLayout.attachForm(self.m_jointToolButton, 'left', 30)
        self.m_topLayout.attachForm(self.m_jointToolButton, 'right', 20)
        
        self.m_topLayout.attachControl(self.m_jointToolButton, 'top', 20, self.m_note1Text)
        
        #-------------step 2 text attach-------------#
        
        self.m_topLayout.attachForm(self.m_step2Label, 'left', 20)       
        self.m_topLayout.attachControl(self.m_step2Label, 'top', 20, self.m_jointToolButton)

        self.m_topLayout.attachPosition(self.m_step2Text, 'right', 5, 50)       
        self.m_topLayout.attachControl(self.m_step2Text, 'top', 17, self.m_jointToolButton)
        self.m_topLayout.attachControl(self.m_step2Text, 'left', 20, self.m_step2Label)
        
        #-------------step 3 text attach-------------#
        
        self.m_topLayout.attachPosition(self.m_step3Label, 'left', 20,50)       
        self.m_topLayout.attachControl(self.m_step3Label, 'top', 20, self.m_jointToolButton)

        self.m_topLayout.attachForm(self.m_step3Text, 'right', 20)       
        self.m_topLayout.attachControl(self.m_step3Text, 'top', 17, self.m_jointToolButton)
        self.m_topLayout.attachControl(self.m_step3Text, 'left', 20, self.m_step3Label)
        
        
        #-------------step 2 control attach-------------#
        
        self.m_topLayout.attachForm(self.m_jointTable, 'left', 30)
        self.m_topLayout.attachPosition(self.m_jointTable, 'right', 20, 50)
        self.m_topLayout.attachControl(self.m_jointTable,'top', 20, self.m_step2Text)
        self.m_topLayout.attachControl(self.m_jointTable,'bottom', 20, self.m_loadJointsButton)
                
        self.m_topLayout.attachForm(self.m_loadJointsButton, 'left', 20)
        self.m_topLayout.attachControl(self.m_loadJointsButton, 'right', 20, self.m_genRigButton)
        self.m_topLayout.attachControl(self.m_loadJointsButton, 'bottom', 20,self.m_closeButton)
        
        #-------------step 3 control attach-------------#
        
        self.m_topLayout.attachForm(self.m_ikCheck, 'right',20)
        self.m_topLayout.attachForm(self.m_fkCheck, 'right',20)
        self.m_topLayout.attachForm(self.m_twistCheck, 'right',20)
        
        self.m_topLayout.attachPosition(self.m_ikCheck, 'left' , 40 , 50)
        self.m_topLayout.attachPosition(self.m_fkCheck, 'left' , 40 , 50)
        self.m_topLayout.attachPosition(self.m_twistCheck, 'left' , 40 , 50)
        
        self.m_topLayout.attachControl(self.m_ikCheck, 'top', 10, self.m_step3Text)
        self.m_topLayout.attachControl(self.m_fkCheck, 'top', 10, self.m_ikCheck)
        self.m_topLayout.attachControl(self.m_twistCheck, 'top', 10, self.m_fkCheck)
        
        self.m_topLayout.attachForm(self.m_genRigButton, 'right', 20)
        self.m_topLayout.attachPosition(self.m_genRigButton, 'left', 20, 50)
        self.m_topLayout.attachControl(self.m_genRigButton, 'bottom', 20,self.m_closeButton)
                
        #-------------misc control attach-------------#
                
        self.m_topLayout.attachForm(self.m_closeButton, 'left', 20)
        self.m_topLayout.attachForm(self.m_closeButton, 'right', 20)
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
        
        settings.m_baseName = self.m_rigName
        settings.m_tabName = self.m_topLayout.shortName()
        settings.m_limbName = self.m_limbName
        settings.m_doSideSpecify = self.m_doSideSpecify
        settings.m_sideSpecifier = self.m_sideSpecifier
        settings.m_jntList = self.m_jointTable.getAllItems()
        settings.m_numTwistJnts = self.m_numTwistJnts 
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
            
    def genChain(self):
        
        """
            Method: genChain
                A method to generate the joint chain
        """
        
        #check if there is an existing joint chain
        
        isChainExist  = self.m_rigElement.getIsGenerated()
        force = "False"
        
        if isChainExist:
            
            #generate a dialog window to define the force variable
            
            force = pm.layoutDialog(t = "Replace Chain?", ui = forcePrompt)
            
        if force == "True":
            
            #clear the rigElement
            
            self.m_rigElement.clear()
            
            #and set isChainExist to false
            
            isChainExist = False
            
        #if a chain doesn't exist at this point
        
        if not isChainExist:        
            
            print "INGENERATION", isChainExist, force
            #create a list of the unicode strings representing
            #the selected joints and an empty list for their
            #pynode counterparts
            
            strList = self.m_jointTable.getAllItems()
            pyNodeList = []
            
            #cycle through and convert to pyNode
            
            for jnt in strList:
                
                pyNodeList.append(pm.PyNode(jnt))
                
            #set the m_template joints equal to those passed in with hierarchy enforced
            
            pyNodeList = self.enforceHierarchy(pyNodeList)
                
            #and set the root name for the arm
            
            self.m_rigElement.setRootName(self.addExtToNames(self.addExtToNames([self.m_rigName],self.m_sideSpecifier),self.m_limbName)[0])
            
            result = self.m_rigElement.genArmRig(pyNodeList,
                        _doIK = self.m_ikCheck.getValue(),
                        _ikExt = self.m_ikExt,
                        _doFK = self.m_fkCheck.getValue(),
                        _fkExt = self.m_fkExt,
                        _jntExt = self.m_jntExt,
                        _ctrlExt = self.m_ctrlExt,
                        _doTwist = self.m_twistCheck.getValue(), 
                        _twistStartIds = [-2],
                        _numTwistJnts = self.m_numTwistJnts
                        )
                        
        #############DEAL WITH RESULT##################
        
def forcePrompt():
    """
        Method: forcePrompt
            A procedure defining a layout prompt, global because it
            breaks if it's in a class
            
        On Exit:            Returns a string defining the choice
                            of the force or not
    """
    # Get the dialog's formLayout.
    
    form = pm.setParent(q=True)

    #set size
    
    pm.formLayout(form, e=True, width=300, height = 50)

    #set the text for the window

    t = pm.text(l='A chain already exists, replace it?')
    
    #buttons 

    b1 = pm.button(l='Yes', c='pm.layoutDialog( dismiss="True" )' )
    b2 = pm.button(l='No', c='pm.layoutDialog( dismiss="False" )' )

    #set up the positioning of the elements

    form.attachForm(t, 'top', 5)
    form.attachForm(t, 'left', 5)
    form.attachForm(t, 'right', 5)
    form.attachForm(b1, 'left', 5)
    form.attachForm(b2, 'right', 5)
    form.attachForm(b1, 'bottom', 5)
    form.attachForm(b2, 'bottom', 5)
    
    form.attachControl(b1, 'top', 5, t)
    form.attachControl(b2, 'top', 5, t)

    form.attachPosition(b1, 'right', 5, 50)
    form.attachPosition(b2, 'left', 5, 50)


                                     

#----------END-ArmTabNovice-Class----------#       

