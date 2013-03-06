#----------Imports----------#

import pymel.core as pm

#----------HelpBox-Class----------#

class HelpBox():
    
    """
        Class: HelpBox
            A class to control the contents of the help text box
             
        File: pRigging/src/ui/helpbox.py
        
        Imports:
            pymel.core as pm
    """
    
    def __init__(self,_parent):
                       
        """
            Method: __init__
                The method to set up the help box
                
            Inputs:
                _parent:                The parent ui element
                
            On Exit:
                The help box has been set up properly
        """
        
        #set the parent
        
        pm.setParent(_parent)
        
        #create the top form layout
        
        self.m_topLayout = pm.formLayout(numberOfDivisions = 100)
        
        #then create the update button
        
        self.m_helpButton = pm.button(l = "Help!")
        
        #create the text Label
        
        self.m_helpLabel = pm.text(l = "Tip:", al = 'left', fn = "boldLabelFont")
                
        #and the help Text
        
        self.m_helpText = pm.text (l = "", al = 'left')
        
        #finally arange them all on the layout
        
        self.m_topLayout.attachForm(self.m_helpLabel, 'top', 10)
        self.m_topLayout.attachForm(self.m_helpLabel, 'left', 10)
        self.m_topLayout.attachForm(self.m_helpLabel, 'right', 10)
        
        self.m_topLayout.attachForm(self.m_helpButton, 'right', 10)
        self.m_topLayout.attachForm(self.m_helpButton, 'bottom', 10)
        self.m_topLayout.attachForm(self.m_helpButton, 'left', 10)
        
        self.m_topLayout.attachForm(self.m_helpText, 'right', 10)
        self.m_topLayout.attachForm(self.m_helpText, 'left', 10)
        self.m_topLayout.attachControl(self.m_helpText, 'bottom', 10, self.m_helpButton)        
        self.m_topLayout.attachControl(self.m_helpText, 'top', 10, self.m_helpLabel)
        
        #then call update
        
        self.update()
        
        
    def update(self):
        
        """
            Method: update
                Updates the help Box
                 
            On Exit:
                The help box has been updated
        """
        
        pass
        
    def getTopUI (self):
        
        """
            Method: getTopUi
                method to return the top level ui element within the class
        """
        
        return self.m_topLayout
                                     
#----------END-HelpBox-Class----------#       