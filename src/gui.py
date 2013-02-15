#----------Imports----------#

import pymel.core as pm
import os

#----------GUI-Class----------#

class Gui:
    
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
            pymel.core
            os
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
        
        #first startup boolean
        
        self.m_firstStartup = True
        
        #if the prefs file isn't empty
        
        if os.path.isfile(os.path.expandvars(self.m_toolRoot+".prefs/helpLevel.txt")) == True:
        
            #get the m_skill LevelVariable from the file
        
            f = open(os.path.expandvars(self.m_toolRoot+".prefs/helpLevel.txt"), "r")
            
            #read the contents of the file and close
                        
            self.m_skillLevel = f.readline()            
            f.close
        
        else:
            
            #set a default value for the skill level
        
            self.m_skillLevel = 'Novice'
        
        #generate the gui
        
        self.genGui(self.m_skillLevel)
        
        """--------------------"""
  
        
    def genGui (self, _skillLevel):
        
        """
            Method: genGui
                A method called by the init method and whenever the GUI has to be updated,
                does all of the GUI generation
            
            Inputs:
                self:                   A pointer to the instance of the GUI class of which
                                        this method is being called
                _skillLevel:            A string reperesenting the chosen skill level of the
                                        user, used to define the generation of the UI
            
            On Exit:                    The UI has been generated and shown
        """
        
        if (self.m_firstStartup):
        
            #check the existance of the window currently
            
            if pm.window(self.m_windowName, exists=True):
                pm.deleteUI(self.m_windowName)
                        
            #create the window
            
            self.m_window = pm.window(self.m_windowName, title = "Rigging Tools")
                       
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
           
            #set the first startup boolean
            
            self.m_firstStartup = False
            
        #create the tab layout
               
        self.m_tabs = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        
        #attach the tabs and the radio buttons to the form layout
        
        self.m_outerForm.attachForm(self.m_tabs, 'left', 0), 
        self.m_outerForm.attachForm(self.m_tabs, 'bottom', 0)
        self.m_outerForm.attachForm(self.m_userSkillRB, 'top', 5)
        self.m_outerForm.attachForm(self.m_userSkillRB,'left', 5)
                                  
        self.m_outerForm.attachControl(self.m_tabs, 'top', 5, self.m_userSkillRB)
                                     
        self.m_outerForm.attachPosition(self.m_tabs, 'right', 0, 50)
        self.m_outerForm.attachPosition(self.m_userSkillRB, 'right',0,50)
                                       
        self.m_outerForm.attachNone(self.m_userSkillRB, 'bottom')
        
        
        #set up the contents for the first tab
        #------------TEMPORARY CONTENT------------#
        
        self.child1 = pm.rowColumnLayout(numberOfColumns=1)
        pm.button()
        if _skillLevel == 'Novice':
            pm.button()
            pm.button()
        pm.setParent( '..' )
        
        #set up the contents for the second tab 
        
        self.child2 = pm.rowColumnLayout(numberOfColumns=1)
        pm.button()
        pm.button()
        pm.button()
        pm.setParent( '..' )
        
        #attach the tab contents to the tab
        
        pm.tabLayout(self.m_tabs, edit = True, tabLabel = ((self.child1, 'one'),(self.child2, 'Two')) )
        
        #self.m_tabs.setTabLabel(self.child1, 'one')
        #self.m_tabs.setTabLabel(self.child2, 'Two')
        
        #------------TEMPORARY CONTENT------------#
            
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
            pm.deleteUI(self.m_tabs)
            self.genGui(self.m_skillLevel)
            
            #save the file to the maya prefs folder
            
            f = open(os.path.expandvars(self.m_toolRoot+".prefs/helpLevel.txt"), "w")
            f.write(self.m_skillLevel)
            f.close()
        
        """--------------------"""

#----------END-GUI-Class----------#       
