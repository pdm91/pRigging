#----------Imports----------#

import pymel.core as pm
import pRigging.src.jointchain as pjc
import pRigging.src.twistchain as ptc
import pRigging.src.riggingbase as prb
import pRigging.src.jointchaincontainer as pjcc

#----------BindChain-Class----------#

class BindChain(pjcc.JointChainContainer):    
    
    """
        Class: BindChain
            A class to generate and contain a bind joint chain, optionally a twist joint set, and
            list of the constraints driving the bind joint chain
        
        File: pRigging/src/bindchain.py
        
        Contains:
            self.m_constraints:     a List of controls that drive the joints in the joint chain                 
            self.m_twistChains:      a list of TwistChains, typically 1 for the for arm area
        
        Imports:
            pymel.core as pm
            pRigging.src.jointchain as pjc
            import pRigging.src.twistchain as ptc
            pRigging.src.riggingbase as prb
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
        #initialise the object's attributes
        
        self.m_constraints = []                 
        self.m_twistChains = []
        
        """--------------------"""
    
    def genChain(self, _templateJoints, _names, _twistJointStartIDs = [], _tjsIDs = [], _numTwistJoints = 3):
        
        """
            Method: genChain
                a method which generates a BindChain as a duplicate of the input chain,
                _templateJoints, assigning the names, _names to them  
            
            Inputs:
                self:                   A pointer to the instance of the BindChain class of which
                                        this method is being called
                _templateJoints:          A list of the joints in the chain that is used to 
                                        as the basis for the new joint chain
                _jointNames:              A list of names for the joints to be called,
                                        used as a basis for the control names as well,
                                        names are uncompleted, and will be added to as
                                        they get passed down through the object structure
                _twistJointStartIDs:    A list of the joint Id's on which to generate twist chains,
                                        the twist chain starts from the joint stored in the ID passed
                                        in to the next joint in the hierarchy.
                _tjsIDs:                Short name for _twistJointStartIDs
                _numTwistJoints:          The number of twist joints to add into each twist chain,
                                        ignored if there are no indices set. 
            
            On Exit:                    The Bind chain has been generated                        
        """
        
        #generate the names for the joints
        
        newNames = self.addExtToNames( _names, "Bind")
        
        #generate the joint chain        

        self.m_jointChain = pjc.JointChain()        
        self.m_jointChain.genJoints(_templateJoints, newNames)
        
        #generate the appropriate twistChains
        
        jointList = self.m_jointChain.getJointList()
        
        ids = list(set(_twistJointStartIDs+_tjsIDs))
        
        if ids != []:
            
            initialTwistCount = len(self.m_twistChains)
            
            #cycle through each id passed in
            
            for i in range(0,len(ids)):
                
                #make a new twist chain
                
                self.m_twistChains.append(ptc.TwistChain())
                
                #generate the joints and and the constraints between the bind joints
                
                self.m_twistChains[i+initialTwistCount].genTwistChain(jointList[ids[i]],jointList[(ids[i])+1],
                        _numTwistJoints, 
                        _name = self.addExtToNames(self.removeExtFromNames([jointList[ids[i]]]),"Twist")[0]
                        )     
        
        """--------------------"""
        
    def connectJointsToChains(self, _jointChains, _constraintList):
        
        """
            Method: connectJointsToChains
                a method which connects the bind chain to the input chains
            
            Inputs:
                self:                   A pointer to the instance of the BindChain class of which
                                        this method is being called
                _jointChains:           A list of the joint chains that are to be used to drive the
                                        bind joint chain
                _constraintList:        The constraints to put on the bind chain from the jointChains 
            
            On Exit:                    The bind joint chain has been connected to the input joint chains                    
        """
        
        
        if _jointChains != 0 and _constraintList != 0:
            print _jointChains, _constraintList
            #first enforce equal numbers of joints, users should access the individual method,
            #connectJointToJoints, to define behaviours of chains that are not the same length
            
            #cycle through each joint chain passed in and check if it's length is the same as the
            #number of joints in the bind chain
            
            numBindJoints = self.m_jointChain.getNumJoints()
            
            numCheck = True
            
            print "number of bind joints: ", numBindJoints
            
            for jointChain in _jointChains:
                
                print "number in input joint chain: ", jointChain.getNumJoints()
                if jointChain.getNumJoints() != numBindJoints:
                    
                    numCheck = False
                    
                    break
            print "numCheck: ", numCheck
                    
            #only if the numbers are correct
            
            if numCheck:
                
                #cycle for each joint in the bind chain
                
                for i in range (0,numBindJoints):
                    
                    #make a list of the corresponding joints from each chain
                    
                    driverList = []
                    
                    for jointChain in _jointChains:
                        
                        #add to the driver list
                        
                        driverList.append(jointChain.getJoint(i))
                        
                    #call add const to joint method
                    
                    self.connectJointToJoints(i, driverList, _constraintList)

        """--------------------"""
        
    def connectJointToJoints(self, _id, _jointList, _constraintList):
        
        """
            Method: connectJointToJoints
                a method which connects a specified bind joint to the input joints 
            
            Inputs:
                self:                   A pointer to the instance of the BindChain class of which
                                        this method is being called
                _id:                    The id of the joint to constrain
                _jointList:               A list of the joints that are to be used to drive the
                                        bind joint
                _constraintList:        The constraints to put on the joint 
            
            On Exit:                    The bind joint specified by the _id has been connected to the
                                        specified joints
                                                                
        """
        
        #check if any constraints or joints have been passed into the method and that the id refers to
        #a joint in the joint chain
        
        if _jointList != 0 and _constraintList != 0 and _id >= 0 and _id < self.m_jointChain.getNumJoints():
            
            #cycle through the constraints
            
            for constraint in _constraintList:

                self.m_constraints.append(self.addConstraint(constraint, self.m_jointChain.getJoint(_id), _jointList))
                
        
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
    
    def getConstraints(self):
    
        """
            Method: getConstraints
                a method to return the list of constraints on the bind joints
                
            On Exit:        The Constraint List is returned
            
        """
        
        return self.m_constraints                 
        
        
        """--------------------"""
        
#----------END-BindChain-Class----------#  
