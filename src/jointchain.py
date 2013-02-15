#----------Imports----------#

import pymel.core as pm

#----------JointChain-Class----------#

class JointChain:    
    
    """
        Class: JointChain
            A class to generate and contain the joints that form a joint chain,
            defined as an unbroken hierarch of joints where between 0 and 1 child 
            joints of each joint are included in the chain
        
        File: pRigging/src/jointchain.py
        
        Contains:
            self.m_joints:          A list of the joints contained int he joint chain
                                    ordered from parent to child.
        
        Imports:
            pymel.core
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
        
        pass   
    
    def genJoints(self, _templateJnts, _jntNames):
        
        """
            Method: genJoints
                a method which generates a joint chain as a duplicate of the input chain,
                _templateJnts, assigning the names, _jntNames to them  
            
            Inputs:
                self:                   A pointer to the instance of the GUI class of which
                                        this method is being called
                _templateJnts:          A list of the joints in the chain that is used to 
                                        as the basis for the new joint chain
                _jntNames:              A list of names for the joints to be called
            
            On Exit:                    The joints have been generated and parented together
                                        and named correctly                          
        """
        
        #generate the joint chain based on the selected joints, and the names passed in as inputs
        
        pass
        
    def genFromMirror(self, _mirrorChain):
        
        """
            Method: genFromMirror
                a method which generates a joint chain as a duplicate of the input jointChain
                object, _mirror chain, and renames them correctly 
            
            Inputs:
                self:                   A pointer to the instance of the GUI class of which
                                        this method is being called
                _mirrorChain:           A jointChain object that will be mirrored to generate the
                                        new jointChain object
               
            On Exit:                    The joints have been generated and parented together
                                        and named correctly                          
        """
        
        #takes in a joint chain object and mirrors the chain to generate the chain
        
        pass
        

            
#----------END-JointChain-Class----------#  

###TEST_CODE###

jnts = pm.ls(type = 'joint', selection = True)
print jnts

pm.select(clear = True)

joint1 = pm.joint(name = "niceJNTNAME")
joint1.setTranslation(jnts[0].getTranslation(space = 'world'))
joint1.setRotation(jnts[0].getRotation(space = 'world'))
pm.makeIdentity(joint1, r=True, a=True)


joint2 = pm.joint(name = "niceJNTNAME2")
joint2.setTranslation(jnts[1].getTranslation(space = 'object'))
joint2.setRotation(jnts[1].getRotation(space = 'object'))
pm.makeIdentity(joint2, r=True, a=True)


