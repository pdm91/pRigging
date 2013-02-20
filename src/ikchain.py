#----------Imports----------#

import pymel.core as pm
import pRigging.src.jointchain as pjc
import pRigging.src.riggingbase as prb
import pRigging.src.control as pctrl

#----------IKChain-Class----------#

class IKChain(prb.RiggingBase):    
    
    """
        Class: IKChain
            A class to generate and contain an ik joint chain which includes a joint chain
            and an IK control object and a pole vector
        
        File: pRigging/src/ikchain.py
        
        Contains:
            self.m_jointChain:      A joint chain
            self.m_ikHandle:        The Ik handle
            self.m_ikControl:       The Ik control
            self.m_ikPVControl:     The pole vector control
        
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
        self.m_ikHandle = ""
        self.m_ikControl = pctrl.Control()
        self.m_ikPVControl = pctrl.Control()
        
        """--------------------"""
    
    def genChain(self, _templateJnts, _names, _solver = ""):
        
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
                _solver:                the solver to use
            
            On Exit:                    The fk chain has been generated, as have the controls,
                                        and they have both been connected together                        
        """
        
        #add IK extension to the names
        
        newNames = self.addExtToNames( _names, "IK")
        
        #generate the joint chain based on the selected joints, and the names passed in as inputs
        
        self.m_jointChain.genJoints(_templateJnts, newNames)
        
        #if the solver is not set default to rp
        
        solver = ""
        
        if _solver == "":
            
            solver = "ikRPsolver"
            
        else:
            solver = _solver
            
        #generate a name based on the root joint name
        
        handleName = self.addExtToNames(self.addExtToNames(self.removeExtFromNames(self.removeExtFromNames([_names[0]])), "IK"), "HNDL")[0]
           
        #then generate an IK handle
                
        self.m_ikHandle = pm.ikHandle(
                                name = handleName,
                                startJoint = self.m_jointChain.getTopJoint(), 
                                endEffector = self.m_jointChain.getBottomJoint(),
                                sol = solver)[0] #0 so that just the handle is stored
        
        #and the control for it
        
        self.m_ikControl.genCTRL(self.m_ikHandle)
        
        #and set it as the parent of the IK handle
        
        self.m_ikHandle.setParent(self.m_ikControl.getCtrl())
            
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
        

            
#----------END-IKChain-Class----------#  

reload(pjc)

test = IKChain()
test.genChain(pm.ls(sl = True), ["test_1","test_2","test_3"])