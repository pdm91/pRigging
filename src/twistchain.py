#----------Imports----------#

import pymel.core as pm
import pRigging.src.jointchain as pjc
import pRigging.src.riggingbase as prb

#----------TwistChain-Class----------#

class TwistChain(prb.RiggingBase):    
    
    """
        Class: TwistChain
            A class to generate and contain a twist joint chain and the multiply node which
            drives them
        
        File: pRigging/src/twistchain.py
        
        Contains:
            self.m_jointChain:      a joint chain
            self.m_multNode:        the multiply node which the joints are driven by
        
        Imports:
            pymel.core as pm
            pRigging.src.jointchain as pjc
            pRigging.src.riggingbase as prb


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
        
        #set the variables up
        
        self.m_jointChain = pjc.JointChain()
        self.m_multNode = ""
        
        """--------------------"""
        
    def genTwistChain(self,
                        _topJnt,
                        _bottomJnt,
                        _numJnts,
                        _nameList = [], 
                        _name = "",
                        _addConnection = True,
                        _acon = True,
                        _attr = "rx"
                        ):
        
        """
            Method: __init__
                A method called when the class is instanciated, sets up the attributes
                for the object
            
            Inputs:
                self:                   A pointer to the instance of the object being
                                        created.
                _topJnt:                The top joint that the twist chain will be parented
                                        under
                _bottomJnt:             The joint that will drive the chain's x rotations
                _numJnts:               The number of joints to make
                _nameList:              A list of names, if not specified the name will be 
                                        generated from the top joint
                _name:                  A name, if not specified it will be generated from 
                                        the top joint
                _addConnection:         Defaults to True, defines whether or not to add
                                        the connection to the joints.
                _acon:                  Short Name for _addConnection
                                        
            On Exit:                The twist joint chain has been generated and connected
        """
        
        #generate the joint Chain
        
        self.m_jointChain.genFromTopAndBottom(_topJnt,
                                                _bottomJnt,
                                                _numJnts,
                                                _nameList = _nameList, 
                                                _name = _name
                                                )
                                                
        #then if the acon bool is set
        
        if _acon or _addConnection:
            
            #set a name for the multiply node
            
            multName = ""
            
            if _nameList != []: 
               
                multName = self.addExtToNames(self.removeExtFromNames([_namelist[i]]),"MULT")[0]
                
            elif _name != "":
                
                multName = self.addExtToNames([_name],"MULT")[0]
                
            else:
                
                multName = self.addExtToNames(self.removeExtFromNames([_topJnt]),"MULT")[0]
                
            #make a multiply node to set the influence scale
            
            self.m_multNode = pm.shadingNode('multiplyDivide', name = multName, au = True)
            
            self.m_multNode.input1X.set(1.0/(_numJnts+1))
            
            #switch through the _attr strings
            #at the moment there is a lot of repeated code, might finde a nicer way of doing this
            #in the future
            
            if _attr == "rx":
                
                #connect the value on the bottom joint to the mult node and the output of
                #that to drive the twist joints
                
                _bottomJnt.rx.connect(self.m_multNode.input2X)
                
                for jnt in self.m_jointChain.getJntList():
                    
                    self.m_multNode.outputX.connect(jnt.rx)
                    
            elif _attr == "ry":
                
                #connect the value on the bottom joint to the mult node and the output of
                #that to drive the twist joints
                
                _bottomJnt.ry.connect(self.m_multNode.input2X)
                
                for jnt in self.m_jointChain.getJntList():
                    
                    self.m_multNode.outputX.connect(jnt.ry)
                    
            elif _attr == "rz":
                
                #connect the value on the bottom joint to the mult node and the output of
                #that to drive the twist joints
                
                _bottomJnt.rz.connect(self.m_multNode.input2X)
                
                for jnt in self.m_jointChain.getJntList():
                    
                    self.m_multNode.outputX.connect(jnt.rz)
                    
            elif _attr == "tx":
                
                #connect the value on the bottom joint to the mult node and the output of
                #that to drive the twist joints
                
                _bottomJnt.tx.connect(self.m_multNode.input2X)
                
                for jnt in self.m_jointChain.getJntList():
                    
                    self.m_multNode.outputX.connect(jnt.tx)
                    
            elif _attr == "ty":
                
                #connect the value on the bottom joint to the mult node and the output of
                #that to drive the twist joints
                
                _bottomJnt.ty.connect(self.m_multNode.input2X)
                
                for jnt in self.m_jointChain.getJntList():
                    
                    self.m_multNode.outputy.connect(jnt.ty)
                    
            elif _attr == "tz":
                
                #connect the value on the bottom joint to the mult node and the output of
                #that to drive the twist joints
                
                _bottomJnt.tz.connect(self.m_multNode.input2X)
                
                for jnt in self.m_jointChain.getJntList():
                    
                    self.m_multNode.outputz.connect(jnt.tz)
                    
            elif _attr == "sx":
                
                #connect the value on the bottom joint to the mult node and the output of
                #that to drive the twist joints
                
                _bottomJnt.sx.connect(self.m_multNode.input2X)
                
                for jnt in self.m_jointChain.getJntList():
                    
                    self.m_multNode.outpusx.connect(jnt.sx)
                    
            elif _attr == "sy":
                
                #connect the value on the bottom joint to the mult node and the output of
                #that to drive the twist joints
                
                _bottomJnt.sy.connect(self.m_multNode.input2X)
                
                for jnt in self.m_jointChain.getJntList():
                    
                    self.m_multNode.outpusy.connect(jnt.sy)
                    
            elif _attr == "sz":
                
                #connect the value on the bottom joint to the mult node and the output of
                #that to drive the twist joints
                
                _bottomJnt.sz.connect(self.m_multNode.input2X)
                
                for jnt in self.m_jointChain.getJntList():
                    
                    self.m_multNode.outpusz.connect(jnt.sz)
                            
        
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
        
#----------END-TwistChain-Class----------#  

test = TwistChain()
test.genTwistChain(pm.ls(sl = True)[0],
                        pm.ls(sl = True)[1],
                        4,
                        _nameList = [], 
                        _name = "",
                        _addConnection = True,
                        _acon = True,
                        _attr = "rz")
                        