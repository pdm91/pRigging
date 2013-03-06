#----------Imports----------#

import pymel.core as pm
import pRigging.src.bindchain as pbc
import pRigging.src.ikchain as pic
import pRigging.src.fkchain as pfc
import pRigging.src.control as pctrl
import pRigging.src.riggingbase as prb

#----------ArmRig-Class----------#

class ArmRig(prb.RiggingBase):    
    
    """
        Class: ArmRig
            A class to generate and contain an arm rig with either an fk, Ik or 
            both and a bind chain. also contains the control to handle FK/IK
            switching if apropriate. Also stores the template joint chain for quick
            regeneration. 
        
        File: pRigging/src/armrig.py
        
        Contains:
            self.m_templateJoints:  A list of template joints
            self.m_fkChain:         An optional FKChain.
            self.m_ikChain:         An optional IkChain.
            self.m_bindChain:       An optional BindChain.
            self.m_FKIKControl:     The FKIK switching control, generated if both chain 
                                    sets are made with a bind chain.
            self.m_reverseNode:     The plus minus average node used to reverse the output 
                                    of the FK/IK switch value 
        
        Imports:
            pymel.core as pm
            pRigging.src.bindchain as pbc
            pRigging.src.ikchain as pic
            pRigging.src.fkchain as pfc
            pRigging.src.control as pctrl
            pRigging.src.riggingbase as prb

    """
    
    def __init__(self, _name):
        
        """
            Method: __init__
                A method called when the class is instanciated, sets up the attributes
                for the object
            
            Inputs:
                self:                   A pointer to the instance of the object being
                                        created.
        """
        
        #set the variables up
        
        self.m_templateJoints = []
        self.m_fkChain = 0
        self.m_ikChain = 0
        self.m_bindChain = 0
        self.m_FKIKControl = 0
        self.m_reverseNode = ""
        self.m_topGroup = ""
        
        #the root name of the rig
        
        self.m_rootName = _name
        
        """--------------------"""
        
    def genArmRig(self, 
                    _templateJoints,
                    _doIK = True,
                    _ikExt = "", 
                    _doFK = True,
                    _fkExt = "",
                    _jntExt = "",
                    _ctrlExt = "",
                    _doTwist = True, 
                    _twistStartIds = [-2],
                    _numTwistJnts = 3
                    ):

        
        """
            Method: genArmRig
                A method to generate the arm rig
            
            Inputs:
                self:                   A pointer to the instance of the object being
                                        created.
                _templateJoints:        The joints to use as the template for the arm rig 
                _name:                  The base name for the armRig
                _doIK:                  Whether or not to generate the IK chain, defaults to True
                _doFK:                  Whether or not to generate the FK chain, defaults to True
                _doTwist:               Whether or not to generate any twist chains with the rig,
                                        defaults to True
                _twistStartId:          Defaults to -2, the joint above the last, amounting to
                                        a default of forearm twist
                                        
            On Exit:                The arm has been generated.
        """
        
        #set the template joints
        
        self.m_templateJoints = _templateJoints[:]

        #get the number of joints inputted
        
        numJoints = len(self.m_templateJoints)
        
        #make a list of names based on the number of joints
        
        names = []
        
        groupName = self.addExtToNames([self.m_rootName],"GRP")[0]
        
        if numJoints >= 1:
            
            #if there is at least 1 joint
            
            names.append(self.addExtToNames([self.m_rootName], "Shoulder")[0])
            
        if numJoints >= 2:
            
            #if there are at least 2 joints
            
            names.append(self.addExtToNames([self.m_rootName], "Wrist")[0])
            
        if numJoints == 3:
            
            #if there are exactly three joints
            
            names.insert(-1, self.addExtToNames([self.m_rootName], "Elbow")[0])
            
        elif numJoints > 3:
            
            #if there are more than one joints
            
            for i in range(1, numJoints-1):
                
                #add the elbow as an extension and a number
                
                names.insert(-1, self.addExtToNames(self.addExtToNames([_name], "Elbow"),str(i))[0])
                
        #set a default extension override
        
        extOver = ""
        
        #set a value to it if only FK is being generated or only IK
        
        if (_doIK and not _doFK) or (_doFK and not _doIK):
            
            extOver = "Bind"
            
        #Then if _doIk is true
        
        if _doIK:
            
            #if the extOver is not set
            
            if extOver != "Bind":
                
                extOver = _ikExt
                
            #generate the IK chain
            
            self.m_ikChain = pic.IKChain()

            self.m_ikChain.genChain(self.m_templateJoints, names, _extOverride = extOver, _jointExt = _jntExt, _controlExt = _ctrlExt)
            
        if _doFK:
            
            #if the extOver is not set
            
            if extOver != "Bind":
                
                extOver = _fkExt
                
            #generate the FK Chain
            
            self.m_fkChain = pfc.FKChain()

            self.m_fkChain.genChain( self.m_templateJoints, names, _extOverride = extOver, _jointExt = _jntExt, _controlExt = _ctrlExt)
            
        if _doFK and _doIK:
            
            #generate the bind chain
            
            self.m_bindChain = pbc.BindChain()

            if not _doTwist:
                
                self.m_bindChain.genChain(self.m_templateJoints, names)
                
            else:
                
                 self.m_bindChain.genChain(self.m_templateJoints, names, _twistJointStartIDs = _twistStartIds, _numTwistJoints = _numTwistJnts, _jointExt = _jntExt)
                
            self.m_bindChain.connectJointsToChains([self.m_ikChain.getJointChain(),self.m_fkChain.getJointChain()], ["orient"])
            
            #now create a control to drive the FK/IK switching value
            
            self.m_FKIKControl = pctrl.Control()
            self.m_FKIKControl.genCtrl(self.m_bindChain.getJoint(-1),
                                        _name = self.addExtToNames([self.m_rootName],"FKIK")[0], 
                                        _groupExtsOverride = ["0"],
                                        _parent = self.m_bindChain.getJoint(-1)
                                      )
                                      
            #move the switch control
            
            self.m_FKIKControl.offsetTopGroup (0, 3, 0, _os = True, _r = True)
                                      
            #add an attribute to the control    
            
            ikAttr = self.m_FKIKControl.addAttribute("FKIK_Switch",
                                                        "float",
                                                        _dv = 0,
                                                        _max = 1,
                                                        _min = 0,
                                                        _setMax = True,
                                                        _setMin = True
                                                        ) 
                                                        
            multName = self.addExtToNames(self.addExtToNames([self.m_rootName],"FKIK"),"_MINUS")[0]
                                                        
            
            #generate a minus node and connect it up
                        
            self.m_reverseNode =  pm.shadingNode('plusMinusAverage', name = multName, au = True)
                       
            self.m_reverseNode.operation.set(2)
            
            self.m_reverseNode.input1D[0].set(1)
            
            self.m_FKIKControl.getCtrl().FKIK_Switch.connect(self.m_reverseNode.input1D[1])
            
            #get a list of the constraints on the bind chain
            
            constraintList = self.m_bindChain.getConstraints()
            
            #for each constraint
            
            for const in constraintList:
                
                #get the weight attribute names
                
                weights =  const.getWeightAliasList()
                
                #then connect the appropriate values
            
                self.m_FKIKControl.getCtrl().FKIK_Switch.connect(weights[0])
                self.m_reverseNode.output1D.connect(weights[1])
                    
        #make the group
        
        pm.select(cl = True)
        self.m_topGroup = pm.group(n = groupName)
        
        #if the various chains exist, parent their top group to the group
        
        if self.m_fkChain != 0:
            
            self.m_fkChain.getChainGroup().setParent(self.m_topGroup)
        
        if self.m_ikChain != 0:
            
            self.m_ikChain.getChainGroup().setParent(self.m_topGroup)
        
        if self.m_bindChain != 0:
            
            self.m_bindChain.getChainGroup().setParent(self.m_topGroup)
            
        #clear the selection
        
        pm.select(cl = True)
        
        #return success
        
        return ["SUCCESS","CHAIN GENERATED","SUCCESS: The chain has been successfully generated"]
        
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
        
        #takes in a Twist chain object and mirrors it to generate the chain
        
        pass
        
        """--------------------"""
        
    def setRootName(self, _name):
    
        """
            Method: setRootName
                Method to set the root name for the arm rig
                
            Inputs:
                _name:                  The text to set the name to
        """
        
        self.m_rootName = _name
        
        
        """--------------------"""
        
#----------END-ArmRig-Class----------#  
