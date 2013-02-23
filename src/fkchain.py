#----------Imports----------#

import pymel.core as pm
import pRigging.src.jointchain as pjc
import pRigging.src.riggingbase as prb
import pRigging.src.control as pctrl

#----------FKChain-Class----------#

class FKChain(prb.RiggingBase):    
    
    """
        Class: FKChain
            A class to generate and contain an fk joint chain which includes a joint chain
            and a set of fk control objects which drive the orientation of the joints through orient 
            constraints
        
        File: pRigging/src/fkchain.py
        
        Contains:
            self.m_jointChain:      a joint chain
            self.m_controls:        a List of controls that drive the joints in the joint chain                 
        
        Imports:
            pymel.core as pm
            pRigging.src.jointchain as pjc
            pRigging.src.riggingbase as prb
            pRigging.src.control as pctrl

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
        self.m_controls = []
        
        """--------------------"""
    
    def genChain(self, _templateJnts, _names):
        
        """
            Method: genChain
                a method which generates an FKChain as a duplicate of the input chain,
                _templateJnts, assigning the names, _names to them  
            
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
        
        #add FK extension to the names
        
        newNames = self.addExtToNames( _names, "FK")
        
        #generate the joint chain based on the selected joints, and the names passed in as inputs
        
        self.m_jointChain.genJoints(_templateJnts, newNames)
        
        #for each joint in the list
        
        jntList = self.m_jointChain.getJntList()
        
        i = 0
        
        for jnt in jntList:
            
            #make a control based on the list, connect it with an orient constraint
            
            self.m_controls.append(pctrl.Control())
            self.m_controls[i].genCTRL(jnt, _name = self.removeExtFromNames([newNames[i]])[0], _addConstToObj = ["orient"])
            
            i = i + 1
            
        #then set them in their hierarchical structure
        
        for i in range(len(self.m_controls)-1, 0, -1):
            
            #set the parent of the selected control to the control before it in the list
            
            self.m_controls[i].setCtrlParent(self.m_controls[i-1].getCtrl())
            
        pm.select(cl = True)
        
        
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