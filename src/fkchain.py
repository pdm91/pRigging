#----------Imports----------#

import pymel.core as pm
import pRigging.src.jointchain as pjc

#----------FKChain-Class----------#

class FKChain:    
    
    """
        Class: FKChain
            A class to generate and contain an fk joint chain which includes a joint chain
            and a set of fk control objects which drive the orientation of the joints through orient 
            constraints
        
        File: pRigging/src/fkchain.py
        
        Contains:
            self.m_jointChain:      A list of the joints contained int he joint chain
                                    ordered from parent to child.
        
        Imports:
            pymel.core as pm
            pRigging.src.jointchain as pjc
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
        
        self.m_jointChain = pjc.JointChain()
        
        """--------------------"""
    
    def genChain(self, _templateJnts, _Names):
        
        """
            Method: genChain
                a method which generates a joint chain as a duplicate of the input chain,
                _templateJnts, assigning the names, _jntNames to them  
            
            Inputs:
                self:                   A pointer to the instance of the FKChain class of which
                                        this method is being called
                _templateJnts:          A list of the joints in the chain that is used to 
                                        as the basis for the new joint chain
                _jntNames:              A list of names for the joints to be called,
                                        used as a basis for the control names as well,
                                        names are uncompleted, and will be added to as
                                        they get passed down through the object structure
            
            On Exit:                    The fk chain has been generated, as have the controls,
                                        and they have both been connected together                        
        """
        
        #generate the joint chain based on the selected joints, and the names passed in as inputs
        
        pass
        
        """--------------------"""
        
    def genFromMirror(self, _mirrorChain):
        
        """
            Method: genFromMirror
                a method which generates a joint chain as a duplicate of the input jointChain
                object, _mirror chain, and renames them correctly 
            
            Inputs:
                self:                   A pointer to the instance of the FKChain class of which
                                        this method is being called
                _mirrorChain:           A jointChain object that will be mirrored to generate the
                                        new jointChain object
               
            On Exit:                    The fk chain has been generated, as have the controls,
                                        and they have both been connected together                           
        """
        
        #takes in a joint chain object and mirrors the chain to generate the chain
        
        pass
        
        """--------------------"""
        

            
#----------END-FKChain-Class----------#  

