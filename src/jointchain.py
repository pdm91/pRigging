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
    
    def genJoints(self, _templateJoints, _jointNames):
        
        """
            Method: genJoints
                a method which generates a joint chain as a duplicate of the input chain,
                _templateJoints, assigning the names, _jointNames to them  
            
            Inputs:
                self:                   A pointer to the instance of the JointChain class of which
                                        this method is being called
                _templateJoints:          A list of the joints in the chain that is used to 
                                        as the basis for the new joint chain
                _jointNames:              A list of names for the joints to be called
            
            On Exit:                    The joints have been generated and parented together
                                        and named correctly                          
        """
        
        #generate the joint chain based on the selected joints, and the names passed in as inputs
        
        #check that the number of template joints match the number of names provided
        
        numTemplateJoints = len(_templateJoints)
        numNames =  len(_jointNames)
        
        newNames = _jointNames
        
        #if not return error string
        
        if numTemplateJoints != numNames:
            
            return "Error: number of names provided does not equal the number of template joints"
       
        #otherwise create the joints
        
        else:

            #add the extension to the names
            
            newNames = self.addExtToNames(newNames, self.m_ext)
            
            #make sure the selection is clear
            
            pm.select(clear = True)
        
            #cycle through the joints
            
            i = 0;
            
            while i < numTemplateJoints:
                
                #add a joint to the list of joints in the joint chain
                #NOTE: if inputted name is just a number the joint creation method
                #removes that number from the start of the name
                
                self.m_joints.append(pm.joint(name = newNames[i]))
                
                #set the translation and rotation of the joint
                
                self.transAndOrientObj (self.m_joints[i], _templateJoints[i])
                
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

    def genFromTopAndBottom(
                            self,
                            _topJoint,
                            _bottomJoint,
                            _numJoints,
                            _nameList = [], 
                            _name = "", 
                            _posOnTop = False,
                            _pot = False, 
                            _posOnBottom = False,
                            _pob = False,
                            _parentToTop = True,
                            _ptt = True
                            ):
                            
        """
            Method: genFromTopAndBottom
                a method which generates a joint chain  positioned between the bottom and top
                joint specified
            
            Inputs:
                self:                   A pointer to the instance of the JointChain class of which
                                        this method is being called
                _topJoint:                The top joint used to define the joint chain, this is the top
                                        in hierarchy, not the top in position.
                _bottomJoint:             The bottom joint used to define the joint chain.
                _numJoints:               The number of joints to generate
                _nameList:              A list of names to use as the base for the names of the joints,
                                        must all be unique, defaults to an empty list.
                _name:                  A single base name for the joints, will have numbering added to it
                                        before it being assigned. If neither the name list nor the name 
                                        parameter is set the name will be generated from the top joint 
                                        passed in
                _posOnTop:              Defaults to False, specifies whether or not one of the joints
                                        should be placed on the top joint.
                _pot:                   Short name for _posOnTop
                _posOnBottom:           Defaults to False, specifies whether or not to position one of
                                        the joints should be placed on the bottom joint.
                _pob:                   Short name for _posOnBottom
                _parentToTop:           Defaults to True, specifies whether or not to parent the top
                                        of the joint chain to the top joint passed in
                _ptt:                   Sort name for _parentToTop
               
            On Exit:                    The joints have been generated and parented together
                                        and named correctly                          
        """
        
        #get the position in world space of the two joints passed in
        
        topPos = _topJoint.getTranslation(space='world')
        bottomPos = _bottomJoint.getTranslation(space='world')
        
        #and the vector between them
        
        vector = bottomPos-topPos
        
        #set up the names
        
        newNames = []
        
        #if no names were passed in,
        
        if (_nameList == [] or len(_nameList) != _numJoints) and _name == "":
            
            #set the base name
            
            nameBase = self.removeExtFromNames([_topJoint.name()])[0]
            
            #for each name that's being created
            
            for i in range (0, _numJoints):
                
                #add a number as an extension and put the name into the list
                
                newNames.append(self.addExtToNames([nameBase], str(i+1))[0])
                
        #if the single name was passed in
        
        elif (_nameList == [] or len(_nameList) != _numJoints) and _name != "":
            
            for i in range (0, _numJoints):
                
                newNames.append(self.addExtToNames([_name],str(i+1))[0])
               
       #if the list was passed in it takes precidence
                
        else:
            
            for name in _nameList:
                
                newNames.append(name)
                
        #add the joint extension
        
        newNames = self.addExtToNames(newNames,self.m_ext)
                
        #generate the joints:
            
        for jointName in newNames:
            
            #clear the selection
            
            pm.select( cl = True )
            
            #and make the joints
            
            self.m_joints.append(pm.joint(name = jointName))
            
        pm.select(cl = True)

        #make a list of the propotions along the vector for each joint to be positioned
        
        vecMultiplier = []
        
        #first calculate the divisor
        
        divisor = _numJoints+1
        
        if _posOnTop or _pot:
            
            divisor = divisor - 1
            
        if _posOnBottom or _pob:
            
            divisor = divisor - 1
            
        #then claculate the proportions
        
        proportions = 1.0/divisor
        
        #finally, loop through for each joint that is not co positioned 
        #with one of the input joints
        
        for i in range(0,(divisor - 1)):
            
            #append the multiplier
            
            vecMultiplier.append(proportions*(i+1))
            
        #then if either the top of or the bottom joints are meant to be in
        #place as the inputted joints, add those multipliers 
        
        if _posOnTop or _pot:
            
            vecMultiplier.insert(0,0)
            
        if _posOnBottom or _pob:
            
            vecMultiplier.append(1)
            
        #finally loop through each joint and set the position and orientation and freeze transformations
        #and do the parenting
        
        for i in range (0,len(self.m_joints)):
            
            self.m_joints[i].setTranslation(topPos+(vector*vecMultiplier[i]))
            
            #add a clause for if it's the last joint and it is in the same position as
            #the bottom joint
            
            if i == len(self.m_joints)-1 and (_pob or _posOnBottom):
                
                self.m_joints[i].setParent(self.m_joints[i-1])
                self.m_joints[i].jointOrientX.set(0)
                self.m_joints[i].jointOrientY.set(0)
                self.m_joints[i].jointOrientZ.set(0)
                
            else:    
            
                self.orientByAim(self.m_joints[i],_bottomJoint, _upObj = _topJoint)              
                pm.makeIdentity(self.m_joints[i], r=True, a=True)
                
                #if it's not the root, parent it under the one higher up the hierarchy
                
                if i != 0:
                    
                    self.m_joints[i].setParent(self.m_joints[i-1])
                    
        #parent the top joint to the top joint passed in if chosen and clear selection
        
        if _ptt and _parentToTop:
            
            self.m_joints[0].setParent(_topJoint)
                    
        pm.select (cl = True)
                        
        """--------------------"""    
            
    def genFromMirror(self, _mirrorChain):
        
        """
            Method: genFromMirror
                a method which generates a joint chain as a mirrored duplicate of the input jointChain
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
        
    def getJointList(self):
        
        """
            Method: getJointList
                a method which returns the list of the joints incorporated in the joint chain
                
            On Exit:                    returns a list of the joints in the chain
        """
        
        return self.m_joints
        
        """--------------------"""
        
    def getNumJoints(self):
        
        """
            Method: getNumJoints
                a method which returns the list number of joints in the joint chain
                
            On Exit:                    returns the number of joints
        """
        
        return len(self.m_joints)
        
        """--------------------"""
        
    def getJoint(self, _id):
        
        """
            Method: getJoint
                a method which returns the specified joint in the joint chain hierarchy.
                
            On Exit:                    returns the top joint in the joint chain hierarchy
        """
        
        return self.m_joints[_id]
        
        """--------------------"""
    

            
#----------END-JointChain-Class----------# 
