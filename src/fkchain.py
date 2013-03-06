#----------Imports----------#

import pymel.core as pm
import pRigging.src.jointchain as pjc
import pRigging.src.riggingbase as prb
import pRigging.src.control as pctrl
import pRigging.src.jointchaincontainer as pjcc


#----------FKChain-Class----------#

class FKChain(pjcc.JointChainContainer):    
    
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
        
        self.m_controls = []
        
        self.m_isGenerated = False
        
        """--------------------"""
    
    def genChain(self, _templateJoints, _names, _extOverride = "", _jointExt = "", _controlExt = ""):
        
        """
            Method: genChain
                a method which generates an FKChain as a duplicate of the input chain,
                _templateJnts, assigning the names, _names to them  
            
            Inputs:
                self:                   A pointer to the instance of the FKChain class of which
                                        this method is being called
                _templateJoints:          A list of the joints in the chain that is used to 
                                        as the basis for the new joint chain
                _names:                 A list of names for the joints to be called,
                                        used as a basis for the control names as well,
                                        names are uncompleted, and will be added to as
                                        they get passed down through the object structure
                _extOverride:           An override for the name extension to be added at 
                                        this stage 
            
            On Exit:                    The fk chain has been generated, as have the controls,
                                        and they have both been connected together                        
        """
        
        newNames = _names[:]
        groupName = _names[0]
        
        if _extOverride == "":
                
            #add FK extension to the names
            
            newNames = self.addExtToNames( newNames, "FK")
            
            groupName = self.addExtToNames(self.removeExtFromNames([groupName]),"FK")[0]
        
        else:
            
            #add the override extension to the names
            
            newNames = self.addExtToNames(newNames, _extOverride)
            groupName = self.addExtToNames(self.removeExtFromNames([groupName]),_extOverride)[0]
            
        #generate the joint chain based on the selected joints, and the names passed in as inputs
        
        self.m_jointChain = pjc.JointChain()
        self.m_jointChain.genJoints(_templateJoints, newNames, _ext = _jointExt)
        
        #for each joint in the list
        
        jointList = self.m_jointChain.getJointList()
        
        i = 0
        
        for joint in jointList:
            
            #make a control based on the list, connect it with an orient constraint
            
            self.m_controls.append(pctrl.Control())
            self.m_controls[i].genCtrl(joint, _name = self.removeExtFromNames([newNames[i]])[0], _addConstraintToObj = ["orient"], _cExt = _controlExt)
            
            i = i + 1
            
        #then set them in their hierarchical structure
        
        for i in range(len(self.m_controls)-1, 0, -1):
            
            #set the parent of the selected control to the control before it in the list
            
            self.m_controls[i].setCtrlParent(self.m_controls[i-1].getCtrl())
            
        self.addGroupOverChain(groupName)   
            
        pm.select(cl = True)
        
        self.m_isGenerated = True
        
        
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
            self.m_controls[0].getTopGrp().setParent(newGroup)
            self.m_chainGroups.append(newGroup)    

        
        """--------------------"""    
        
    def clear(self):
        
        """
            Method: clear
                A method to delete all of the maya objects generated by the joint chain
        """
        
        if self.m_isGenerated == True:
                
            #call clear on pRigging objects
            
            self.m_jointChain.clear()
            
            for ctrl in self.m_controls:
                
                ctrl.clear()
            
            #delete maya objects
            
            for grp in self.m_chainGroups:
                
                try:
                    
                    pm.delete(grp)
                    
                except:
                
                    pass
            
                
            #then reset the lists
            
            self.m_jointChain = 0
            self.m_chainGroups = []
            self.m_controls = []
            
            #and set the is generated boolean
            
            self.m_isGenerated = False
        
        """--------------------"""
        
    def getIsGenreated(self):
        
        """
            Method: getIsGenerated
                A method to return whether or not the chain has been generated
        """
        
        return self.m_isGenerated
            
        """--------------------"""

#----------END-FKChain-Class----------#  
