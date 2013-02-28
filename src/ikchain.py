#----------Imports----------#

import pymel.core as pm
import pRigging.src.jointchain as pjc
import pRigging.src.riggingbase as prb
import pRigging.src.control as pctrl
import pRigging.src.jointchaincontainer as pjcc


#----------IKChain-Class----------#

class IKChain(pjcc.JointChainContainer):    
    
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
            pRigging.src.jointchaincontainer as pjcc
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
        
        #initialise the super class
        
        pjcc.JointChainContainer.__init__(self)
        
        #initialise the object's attributes
        
        self.m_ikHandle = ""
        self.m_ikControl = pctrl.Control()
        self.m_ikPVControl = pctrl.Control()
        
        """--------------------"""
    
    def genChain(self, _templateJoints, _names, _solver = "", _extOverride = ""):
        
        """
            Method: genChain
                a method which generates an FKChain as a duplicate of the input chain,
                _templateJoints, assigning the names, _names to them  
            
            Inputs:
                self:                   A pointer to the instance of the FKChain class of which
                                        this method is being called
                _templateJoints:        A list of the joints in the chain that is used to 
                                        as the basis for the new joint chain
                _names:                 A list of names for the joints to be called,
                                        used as a basis for the control names as well,
                                        names are uncompleted, and will be added to as
                                        they get passed down through the object structure
                _solver:                the solver to use
                _extOverride:           An override for the name extension to be added at 
                                        this stage 
            
            On Exit:                    The fk chain has been generated, as have the controls,
                                        and they have both been connected together                        
        """
        #initialise variables
        
        newNames = _names[:]
        groupName = _names[0]
        
        if _extOverride == "":

            #add IK extension to the names
            
            newNames = self.addExtToNames( newNames, "IK")
            print _names, "LOOKATME"
            groupName = self.addExtToNames(self.removeExtFromNames([groupName]),"IK")[0]
        
        else:
            
            #add the override extension to the names
            
            newNames = self.addExtToNames(newNames, _extOverride)
            groupName = self.addExtToNames(self.removeExtFromNames([groupName]),_extOverride)[0]
                
        #generate the joint chain based on the selected joints, and the names passed in as inputs
        
        self.m_jointChain = pjc.JointChain()
        self.m_jointChain.genJoints(_templateJoints, newNames)
        
        #if the solver is not set default to rp
        
        solver = ""
        
        if _solver == "":
            
            solver = "ikRPsolver"
            
        else:
            solver = _solver
            
        #generate a name based on the root joint name
        
        handleName = self.addExtToNames(self.addExtToNames(self.removeExtFromNames(self.removeExtFromNames([newNames[0]])), "IK"), "HNDL")[0]
           
        #then generate an IK handle
                
        self.m_ikHandle = pm.ikHandle(
                                name = handleName,
                                startJoint = self.m_jointChain.getJoint(0), 
                                endEffector = self.m_jointChain.getJoint(-1),
                                sol = solver)[0] #0 so that just the handle is stored
        
        #and the control for it

        self.m_ikControl.genCtrl(self.m_ikHandle)
        
        #and set it as the parent of the IK handle
        
        self.m_ikHandle.setParent(self.m_ikControl.getCtrl())
        
        if solver == "ikRPsolver":
            
            #make a pole vector control
            #set the name for the control
            
            pvName = self.addExtToNames(self.addExtToNames(self.removeExtFromNames(self.removeExtFromNames([newNames[0]])), "IK"), "PV")[0]
            
            #add the control
            
            self.m_ikPVControl.genCtrl(self.m_jointChain.getJoint(1), _name= pvName)
    
            #offset offsets the group
            
            self.m_ikPVControl.offsetTopGroup (-5, 0, 0, _os = True, _r = True)
            
            #set the consraint
            
            self.m_ikPVControl.addConstraint("poleVector", self.m_ikHandle, self.m_ikPVControl.getCtrl())
            
            self.m_ikPVControl.setCtrlParent(self.m_ikControl.getCtrl())
            
            self.m_ikPVControl.getTopGrp().setRotation((0,0,0), space = "world")    
            
        #add the top group to the chain and controls
        
        self.addGroupOverChain( groupName)
            
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
        
    def addGroupOverChain(self, _name, _gExtOverride = "", _gExt = "", _addExt = True):
        
        """
            Method: addGroupOverChain
                a method to add a group over the chain
                
            Inputs:
                _name:                  The name of the group
                _gExtOverride:          An override of the extension for the group name,
                                        defaults to an empty string
                _gExt:                  Short name for _gExtOverride
                _addExt:                A boolean defining whether or not to add an extension
                                        to the group name, defaults to False
                                        
            On Exit:                    The group has been made and all of the objects in the
                                        chain have been parented under it
        """        
        
        #set up the name value
        
        name = _name
        
        #if the addExt boolean is set
        
        if (_addExt):
            
            #set the extension string to be the default
            
            ext = "GRP"
            
            #if either of the name inputs are set, make the extension the input,
            #_gExtOverride takes precidence over _gExt
            
            if _gExtOverride != "":
                
                ext = _gExtOverride
                
            elif _gExt != "":
                
                ext = _gExt
                
            #add the extension to the name
            
            name = self.addExtToNames([name],ext)[0]
            
        #check if there is currently a top group
        
        if len(self.m_chainGroups) != 0:
            
            #ensure clear selection
            
            pm.select(cl = True)
            
            #greate a group over that one and insert it into the top of the list
            #after setting the parent
            
            newGroup = pm.group(n = name)
            self.m_chainGroups[0].setParent(newGroup)
            self.m_chainGroups.insert(0,newgroup)
            
        #if there arent any groups
        
        else:
            
            #generate the group and set it as the parent of all of the hierarchies 
            #represented within the chain container
            
            pm.select(cl = True)
            
            #greate a group over that one and insert it into the top of the list
            #after setting the parent
            
            newGroup = pm.group(n = name)
            self.m_jointChain.getJoint(0).setParent(newGroup)
            self.m_ikControl.getTopGrp().setParent(newGroup)
            self.m_chainGroups.append(newGroup)   
                    
#----------END-IKChain-Class----------#  
