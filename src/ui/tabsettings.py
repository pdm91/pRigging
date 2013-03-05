#----------TabSettings-Class----------#

class TabSettings:
    
    """
        Class: TabSettings
            A data storage class for transferring settings between correspnding tabs of differing
        
        File: pRigging/src/ui/tabsettings.py
        
        Contains:
            

        Imports:
            pymel.core as pm
            pRigging.src.riggingbase as prb     
    """
    
    def __init__(self):
        
        """
            Method: __init__
                A method called when the class is instanciated, sets up the attributes
            
            Inputs:
        """
        
        self.m_tabName = ""
        self.m_limbName = ""
        self.m_doSideSpecify = True
        self.m_sideSpecifier = ""
        self.m_jntList = []
        self.m_numTwistJnts = 3
        self.m_doIK = True
        self.m_ikExt = "IK"
        self.m_doFK = True
        self.m_fkExt = "FK"
        self.m_jntExt = "JNT"
        self.m_ctrlExt = "CTRL"
        self.m_rigElement = 0
        
                                            

#----------END-TabSettings-Class----------#       
