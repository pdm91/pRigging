#----------Imports----------#

import pymel.core as pm
import os
import pRigging.src.riggingbase as prb
import pRigging.src.ui.starttabnovice as pstt

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
        
        #tabList
        
        self.m_tabList = []
        
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
            
            #create the initial tab
            
            self.m_tabList.append(pstt.StartTabNovice(self.m_tabs,self,"General"))
        
        #attach the tabs and the radio buttons to the form layout
        
        self.m_outerForm.attachForm(self.m_tabs, 'left', 0), 
        self.m_outerForm.attachForm(self.m_tabs, 'bottom', 0)
        self.m_outerForm.attachForm(self.m_userSkillRB, 'top', 5)
        self.m_outerForm.attachForm(self.m_userSkillRB,'left', 5)
                                  
        self.m_outerForm.attachControl(self.m_tabs, 'top', 5, self.m_userSkillRB)
                                     
        self.m_outerForm.attachPosition(self.m_tabs, 'right', 0, 50)
        self.m_outerForm.attachPosition(self.m_userSkillRB, 'right',0,50)
                                       
        self.m_outerForm.attachNone(self.m_userSkillRB, 'bottom')
                    
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
            #pm.deleteUI(self.m_tabs)
            self.genGui(self.m_skillLevel)
            
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
            
            print side
            
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
    
    pm.formLayout(form, e=True, width=300)

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

gui = Gui()
