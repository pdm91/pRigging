#----------Imports----------#

import pymel.core as pm
import pRigging.src.jointchain as pjc
import pRigging.src.riggingbase as prb

#----------JointChainContainer-Class----------#

class JointChainContainer(prb.RiggingBase):
    """
        Class: JointChainContainer
            A base class for all joint chain container classes
        
        File: pRigging/src/ikchain.py
        
        Contains:
            self.m_jointChain:      A joint chain
        
        Imports:
            pymel.core as pm
            pRigging.src.jointchain as pjc
            pRigging.src.riggingbase as prb
    """
    
    def __init__(self):
        
        """
            Method: __init__
                A method called when the class is instanciated, sets up the attributes
                for the object
            
            Inputs:
                self:                   A pointer to the instance of the object being
                                        created.
        """
        #initialise the object's attributes
        
        self.m_jointChain = 0

        """--------------------"""

    def getJointChain (self):
    
        """
            Method: getJointChain
                a method to return the joint chain object
                
        """
        
        return self.m_jointChain

        """--------------------"""
            
    def getJoint (self, _id):
    
        """
            Method: getJointChain
                a method to return the joint chain object
                
        """
        
        return self.m_jointChain.getJoint(_id)

        """--------------------"""
            
#----------END-JointChainContainer-Class----------#  
