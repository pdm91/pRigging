import maya.cmds as cmds

class JointChain:
    
    def __init__(self):
        
        #initialise the object's attributes
        
        pass   
    
    def genJoints(self, _templateNames, _jointNames):

        #generate the joint chain based on the names of the selected joints, and the names passed in as inputs
        
        pass
        
    def genFromMirror(self, _mirrorChain):
        
        #takes in a joint chain object and mirrors the chain to generate the chain
        
        pass
        
    def checkHierarchy (self, _names):
        
        #checks the list of names to make sure they are in hierarchical order and that at most 1 child of each joint is selected
        #returns either an error if too many of a joint's children are selected
        
        #cycle through each object
        
        for i in range (len(_names)):
            #create a list of child objects
            
            children = 
