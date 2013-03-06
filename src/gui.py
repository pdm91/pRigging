#----------Imports----------#

import pymel.core as pm
import os
import pRigging.src.riggingbase as prb
import pRigging.src.ui.starttabnovice as pstn
import pRigging.src.ui.armtabnovice as patn
import pRigging.src.ui.armtabintermediate as pati
import pRigging.src.ui.armtabexperienced as pate
import pRigging.src.armrig as par
import pRigging.src.ui.tabsettings as pts
import pRigging.src.ui.helpbox as phb

#----------GUI-Class----------#

class Gui (prb.RiggingBase):
    
    """
        Class: Gui
            A class to contain all of the user interface code for the rigging tools
        
        File: pRigging/src/gui.py
        
        Contains:
            self.m_skillLevel:      A variable to store the skill level that the 
                                    user picks for the UI
            self.m_toolRoot:       A string that stores the path to the root of
                                    the tool directory.
            self.m_firstStartup:    A boolean value that states whether or not
                                    tool has been started off before
            self.m_window:          The GUI window, contains all of the other UI
                                    elements
            self.m_windowName:      The name of the window ui object being created
        
        Imports:
            pymel.core as pm
            os
            pRigging.src.riggingbase as prb
            pRigging.src.ui.starttabnovice as pstn
            pRigging.src.ui.armtabnovice as patn
            pRigging.src.ui.armtabintermediate as pati
            pRigging.src.ui.armtabexperienced as pate
            pRigging.src.armrig as par
            pRigging.src.ui.tabsettings as pts
            pRigging.src.ui.helpbox as phb
    """
    
    def __init__(self):
        
        """
            Method: __init__
                A method called when the class is instanciated, sets up the attributes
                and calls the genGui method
            
            Inputs:
                self:                   A pointer to the instance of the object being
                                        created.
        """
        
        #set the location of the root folder of the tool files
        
        self.m_toolRoot = "$MAYA_APP_DIR/scripts/pRigging/"
        
        #place holder value for window variable
        
        self.m_window = 0
        
        #name for the window
        
        self.m_windowName = "pRiggingWindow"
        
        #tabList
        
        self.m_tabList = []
        
        #rig components
        
        self.m_rigComponents = []
                
        #if the prefs file isn't empty
        
        if os.path.isfile(os.path.expandvars(self.m_toolRoot+".prefs/helpLevel.txt")) == True:
        
            #get the m_skill LevelVariable from the file
        
            f = open(os.path.expandvars(self.m_toolRoot+".prefs/helpLevel.txt"), "r")
            
            #read the contents of the file and close
                        
            self.m_skillLevel = f.readline()            
            f.close
        
        else:
            
            #make sure the folder is there
            
            if not os.path.exists(os.path.expandvars(self.m_toolRoot+".prefs")):
                
                #if not make it
                
                os.mkdir(os.path.expandvars(self.m_toolRoot+".prefs"))
            
            #set a default value for the skill level
        
            self.m_skillLevel = 'Novice'
        
        #generate the gu   
        #check the existance of the window currently
        
        if pm.window(self.m_windowName, exists=True):
            pm.deleteUI(self.m_windowName)
                    
        #create the window
        
        self.m_window = pm.window(self.m_windowName, title = "pRigging")
                   
        #create the form layout that contains the overall window
        
        self.m_outerForm = pm.formLayout(numberOfDivisions = 100)
        
        #map from help skill level string to int - may be replaced with an actual map object
        
        i = 1
        
        if self.m_skillLevel == "Novice":
            i = 1
        elif self.m_skillLevel == "Intermediate":
            i = 2
        elif self.m_skillLevel == "Experienced":
            i = 3
        
        #create the user skill radio buttons
        
        self.m_userSkillRB = pm.radioButtonGrp(
                    label='User Skill: ', 
                    labelArray3=['Novice', 'Intermediate', 'Experienced'], 
                    numberOfRadioButtons=3, 
                    on1 = pm.Callback(self.updateSkillLevel, "Novice"),  
                    on2 = pm.Callback(self.updateSkillLevel,"Intermediate"),  
                    on3 = pm.Callback(self.updateSkillLevel,"Experienced"),
                    sl = i)
        
        #create the show/hide buttons
        
        self.m_hideRigButton = pm.button(l = "Hide Rig")        
        self.m_hideChainButton = pm.button(l = "Hide Current Chain")
        self.m_showRigButton = pm.button(l = "Show Rig")        
        self.m_showChainButton = pm.button(l = "Show Current Chain")
        
        self.m_helpBox = phb.HelpBox(self.m_outerForm)
        helpBoxUI = self.m_helpBox.getTopUI()   
        
        pm.setParent(self.m_outerForm)   
        
        #create the tab layout
               
        self.m_tabs = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        
        #create the initial tab
        
        self.m_tabList.append(pstn.StartTabNovice(self.m_tabs,self,"General"))
        
        #attach the tabs and the radio buttons to the form layout
        
        self.m_outerForm.attachForm(self.m_tabs, 'left', 0), 
        self.m_outerForm.attachForm(self.m_tabs, 'bottom', 0)
        self.m_outerForm.attachForm(self.m_userSkillRB, 'top', 5)
        self.m_outerForm.attachForm(self.m_userSkillRB,'left', 5)
                                  
        self.m_outerForm.attachControl(self.m_tabs, 'top', 5, self.m_userSkillRB)
                                     
        self.m_outerForm.attachPosition(self.m_tabs, 'right', 0,70)
          
        #attach the buttons
                                       
        self.m_outerForm.attachForm(self.m_hideRigButton, 'right', 20)
        self.m_outerForm.attachForm(self.m_hideChainButton, 'right', 20)
        self.m_outerForm.attachForm(self.m_showRigButton, 'right', 20)
        self.m_outerForm.attachForm(self.m_showChainButton, 'right', 20)
        

        self.m_outerForm.attachPosition(self.m_hideRigButton, 'left', 10, 70)
        self.m_outerForm.attachPosition(self.m_hideChainButton, 'left', 10, 70)
        self.m_outerForm.attachPosition(self.m_showRigButton, 'left', 10, 70)
        self.m_outerForm.attachPosition(self.m_showChainButton, 'left', 10, 70)
        
        self.m_outerForm.attachControl(self.m_hideRigButton, 'top', 10, self.m_userSkillRB)
        self.m_outerForm.attachControl(self.m_hideChainButton, 'top', 10, self.m_hideRigButton)
        self.m_outerForm.attachControl(self.m_showRigButton, 'top', 10, self.m_hideChainButton)
        self.m_outerForm.attachControl(self.m_showChainButton, 'top', 10, self.m_showRigButton)
        
        #attach the helpbox
        
        self.m_outerForm.attachForm(helpBoxUI, 'right', 10)
        self.m_outerForm.attachForm(helpBoxUI, 'bottom', 10)
        self.m_outerForm.attachPosition(helpBoxUI, 'left', 10, 70)
        self.m_outerForm.attachControl(helpBoxUI, 'top', 10,self.m_showChainButton) 
                            
        #show window 
        
        pm.showWindow(self.m_window)
        
        """--------------------"""
        
    def updateSkillLevel(self,_newLevel):
        
        """
            Method: updateSkillLevel
                A method called by the user skill radioButton to change the user skill
                variable and to regenerate the UI based on the new valuer
            
            Inputs:
                self:                   A pointer to the instance of the GUI class of which
                                        this method is being called
                _newLevel:              A string reperesenting the chosen skill level of the
                                        user, used to define the regeneration of the UI
            
            On Exit:                    The UI has been regenerated and shown based on the
                                        radio Button input 
        """
         
        #check that the skill level has changed
        
        if self.m_skillLevel != _newLevel:
        
            #set the skill level
        
            self.m_skillLevel = _newLevel
            
            #set the id for selection after the transfer
            
            id = self.m_tabs.getSelectTabIndex()
            
            for i in range(1, len(self.m_tabList)):
                
                #get the type
                
                type = self.m_tabList[i].getTabType()
                
                if type == "arm":
                    
                    #clear the current tab storing the settings
                    
                    settings = self.m_tabList[i].clearTab()
                    
                    #replace the existing tab with a new one,
                    #this will take the reference count of the tab to
                    #0 and python will remove it
                    
                    if self.m_skillLevel == "Novice":
                        
                        self.m_tabList[i] = patn.ArmTabNovice(self.m_tabs,self, settings)
                                                
                    elif self.m_skillLevel == "Intermediate":
                        
                        self.m_tabList[i] = pati.ArmTabIntermediate(self.m_tabs,self, settings)
                        
                    elif self.m_skillLevel == "Experienced":
                    
                        self.m_tabList[i] = pate.ArmTabExperienced(self.m_tabs,self, settings)            
                
            #re-select the chosen tab
            
            self.m_tabs.setSelectTabIndex(id)
            
            #save the file to the maya prefs folder
            
            f = open(os.path.expandvars(self.m_toolRoot+".prefs/helpLevel.txt"), "w")
            f.write(self.m_skillLevel)
            f.close()
        
        """--------------------"""
        
    def addTab(self, _type):
        
        """
            Method: addTab
                a method to add a tab
                
            Inputs:
                _type:                A string identifyinfg the type of tab to add
                
            On Exit:                  A tab has been added
            
        """
        
        #switch throught the different options
        
        if _type == "arm":
            
            #create a button prompt
            
            side = pm.layoutDialog(t = "Pick Sides", ui = lrPrompt)
            
            #generate the root name from the name stored in the start tab 
            
            name = self.addExtToNames([self.m_tabList[0].getRigName()],side)[0]
            
            #make an arm rig and add it to the rig components
            
            arm = par.ArmRig(name)
            self.m_rigComponents.append(arm)
            
            #set up a settings object for the tab settings
            settings = pts.TabSettings()
            
            settings.m_tabName = "Arm Tab"
            settings.m_limbName = "Arm"
            settings.m_sideSpecifier = side
            settings.m_rigElement = arm
            
            #switch through the dificulty levels
            
            if self.m_skillLevel == "Novice":
                
                self.m_tabList.append(patn.ArmTabNovice(self.m_tabs,self, settings))
                
            elif self.m_skillLevel == "Intermediate":
                
                self.m_tabList.append(pati.ArmTabIntermediate(self.m_tabs,self, settings))
                
            elif self.m_skillLevel == "Experienced":
            
                self.m_tabList.append(pate.ArmTabExperienced(self.m_tabs,self, settings))
            
            self.m_tabs.setSelectTabIndex(len(self.m_tabList))
            
            


            
            
            
def lrPrompt():
    """
        Method: lrPrompt
            A procedure defining a layout prompt, global because it
            breaks if it's in a class
            
        On Exit:            Returns a string defining the choice
                            of the user, left right or centre
    """
    # Get the dialog's formLayout.
    
    form = pm.setParent(q=True)

    #set size
    
    pm.formLayout(form, e=True, width=300, height = 50)

    #set the text for the window

    t = pm.text(l='What side do you want to start working on?')
    
    #buttons 

    b1 = pm.button(l='Left', c='pm.layoutDialog( dismiss="L" )' )
    b2 = pm.button(l='Centre', c='pm.layoutDialog( dismiss="C" )' )
    b3 = pm.button(l='Right', c='pm.layoutDialog( dismiss="R" )' )

    #set up the positioning of the elements

    form.attachForm(t, 'top', 5)
    form.attachForm(t, 'left', 5)
    form.attachForm(t, 'right', 5)
    form.attachForm(b1, 'left', 5)
    form.attachForm(b3, 'right', 5)
    form.attachControl(b1, 'top', 5, t)
    form.attachControl(b2, 'top', 5, t)
    form.attachControl(b3, 'top', 5, t)
    form.attachPosition(b1, 'right', 5, 33)
    form.attachPosition(b2, 'left', 5, 33)
    form.attachPosition(b2, 'right', 5, 66)
    form.attachPosition(b3, 'left', 5, 66)


    

#----------END-GUI-Class----------#       
reload(par)
reload (patn)
gui = Gui()
