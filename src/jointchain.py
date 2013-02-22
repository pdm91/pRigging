#----------Imports----------#

import pymel.core as pm
import pRigging.src.riggingbase as prb

#----------JointChain-Class----------#

class JointChain(prb.RiggingBase):    
    
    """
        Class: JointChain
            A class to generate and contain the joints that form a joint chain,
            defined as an unbroken hierarch of joints where between 0 and 1 child 
            joints of each joint are included in the chain
        
        File: pRigging/src/jointchain.py
        
        Contains:
            self.m_joints:          A list of the joints contained int he joint chain
                                    ordered from parent to child.
            self.m_ext:             A string containing the extension to be added to the
                                    names passed in to the generation method 
        
        Imports:
            pymel.core as pm
            pRigging.src.riggingbase as prb
            
        Inherits:
            prb.RiggingBase
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
        
        self.m_joints = []
        self.m_ext = "JNT"
        
        """--------------------"""
    
    def genJoints(self, _templateJnts, _jntNames):
        
        """
            Method: genJoints
                a method which generates a joint chain as a duplicate of the input chain,
                _templateJnts, assigning the names, _jntNames to them  
            
            Inputs:
                self:                   A pointer to the instance of the JointChain class of which
                                        this method is being called
                _templateJnts:          A list of the joints in the chain that is used to 
                                        as the basis for the new joint chain
                _jntNames:              A list of names for the joints to be called
            
            On Exit:                    The joints have been generated and parented together
                                        and named correctly                          
        """
        
        #generate the joint chain based on the selected joints, and the names passed in as inputs
        
        #check that the number of template joints match the number of names provided
        
        numTemplateJnts = len(_templateJnts)
        numNames =  len(_jntNames)
        

        
        #if not return error string
        
        if numTemplateJnts != numNames:
            
            return "Error: number of names provided does not equal the number of template joints"
       
        #otherwise create the joints
        
        else:

            #add the extension to the names
            
            newNames = self.addExtToNames(_jntNames, self.m_ext)

            #make sure the selection is clear
            
            pm.select(clear = True)
        
            #cycle through the joints
            
            i = 0;
            
            while i < numTemplateJnts:
                
                #add a joint to the list of joints in the joint chain
                
                self.m_joints.append(pm.joint(name = newNames[i]))
                
                #set the translation and rotation of the joint
                
                self.transAndOrientObj (self.m_joints[i], _templateJnts[i])
                
                #move all rotations to the joint orient
                
                pm.makeIdentity(self.m_joints[i], r=True, a=True)
                
                #if it isnt the first joint
                
                if i!= 0:
                
                    #make the joint created before the current one the parent of the joint
                
                    self.m_joints[i].setParent(self.m_joints[i-1])
                
                #clear selection and increment i
                
                pm.select(clear = True)
                i = i+1
                
        """--------------------"""
        
    def genFromMirror(self, _mirrorChain):
        
        """
            Method: genFromMirror
                a method which generates a joint chain as a duplicate of the input jointChain
                object, _mirror chain, and renames them correctly 
            
            Inputs:
                self:                   A pointer to the instance of the JointChain class of which
                                        this method is being called
                _mirrorChain:           A jointChain object that will be mirrored to generate the
                                        new jointChain object
               
            On Exit:                    The joints have been generated and parented together
                                        and named correctly                          
        """
        
        #takes in a joint chain object and mirrors the chain to generate the chain
        
        pass
        
        """--------------------"""
        
    def getJntList(self):
        
        """
            Method: getJntList
                a method which returns the list of the joints incorporated in the joint chain
                
            On Exit:                    returns a list of the joints in the chain
        """
        
        return self.m_joints
        
        """--------------------"""
        
    def getJoint(self, _id):
        
        """
            Method: getTopJoint
                a method which returns the specified joint in the joint chain hierarchy.
                
            On Exit:                    returns the top joint in the joint chain hierarchy
        """
        
        return self.m_joints[_id]
        
        """--------------------"""
        

            
#----------END-JointChain-Class----------#  
