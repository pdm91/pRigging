#----------Imports----------#

import pymel.core as pm

#----------HelpBox-Class----------#

class HelpBox():
    
    """
        Class: HelpBox
            A class to control the contents of the help text box
             
        File: pRigging/src/ui/helpbox.py
        
        Imports:
            pymel.core as pm
    """
    
    def __init__(self,_parent, _guiInstance):
                       
        """
            Method: __init__
                The method to set up the help box
                
            Inputs:
                _parent:                The parent ui element
                
            On Exit:
                The help box has been set up properly
        """
        
        #set the parent
        
        pm.setParent(_parent)
        
        #set the gui
        
        self.m_gui = _guiInstance
        
        #create the top form layout
        
        self.m_topLayout = pm.formLayout(numberOfDivisions = 100)
        
        #then create the update button
        
        self.m_helpButton = pm.button(l = "Help!", c = pm.Callback(self.update))
        
        #create the text Label
        
        self.m_helpLabel = pm.text(l = "Tip:", al = 'left', fn = "boldLabelFont")
                
        #and the help Text
        
        self.m_helpText = pm.text (l = "", al = 'left', ww = True)
        
        #finally arange them all on the layout
        
        self.m_topLayout.attachForm(self.m_helpLabel, 'top', 10)
        self.m_topLayout.attachForm(self.m_helpLabel, 'left', 10)
        self.m_topLayout.attachForm(self.m_helpLabel, 'right', 10)
        
        self.m_topLayout.attachForm(self.m_helpButton, 'right', 10)
        self.m_topLayout.attachForm(self.m_helpButton, 'bottom', 10)
        self.m_topLayout.attachForm(self.m_helpButton, 'left', 10)
        
        self.m_topLayout.attachForm(self.m_helpText, 'right', 10)
        self.m_topLayout.attachForm(self.m_helpText, 'left', 10)
        self.m_topLayout.attachControl(self.m_helpText, 'bottom', 10, self.m_helpButton)        
        self.m_topLayout.attachControl(self.m_helpText, 'top', 10, self.m_helpLabel)
        
        
        
    def update(self, _errorList = []):
        
        """
            Method: update
                Updates the help Box
                 
            On Exit:
                The help box has been updated
        """
        
        if _errorList != []:
            
            #display the error List
            
            #set the label text
            
            self.m_helpLabel.setLabel(_errorList[0])
            
            #and the help text
            
            self.m_helpText.setLabel(_errorList[2])
            
            
        else:
            
            #make a list of the selection
            
            sel = pm.ls(sl = True)
            print sel
            
            #if there are elements in the selection
            
            if sel != []:
                
                #display information based on the last selected Item
                #use the last selected object
                
                obj = sel[-1]
                
                #set that as the title
                
                self.m_helpLabel.setLabel( obj+":")
                
                #then switch through the top level extensions, firstly groups
                
                text = ""
                
                if "GRP" in obj.name():
                    
                    text = text+ "This Is a Group. Groups with the extension _GRP are used for organisational purposes, to gather together related objects. "
                    
                    #then switch through the next level of possible extensions
                    
                    if "IK" in obj.name():
                        
                        text = text + "This one groups together the IK nodes in the rig element.\n\n"
                    
                    elif "FK" in obj.name():
                        
                        text = text + "This one groups together the FK nodes in the the rig element.\n\n"
                        
                    elif "Bind" in obj.name():
                        
                        text = text + "This one groups together the Bind nodes in the rig element, including the bind chain that will need to be skinned to the model, and any relating nodes.\n\n"
                    else:
                        
                        text = text + "\n\n"  
                        
                #if it's a constraint
                
                elif "Constraint" in obj.name():
                    
                    if "orient" in obj.name():
                        
                        text = text + "This is an orient constraint. It drives the rotation of its parent (in the hierarchy) by the rotation of the object named in the constraint name.\n\n"

                    elif "poleVector" in obj.name():
                        
                        text = text + "This is a pole vector constraint. It drives the pole vector of its parent (in the hierarchy) based on the position of the object named in the constraint name.\n\n"

                    elif "parent" in obj.name():
                        
                        text = text + "This is a parent constraint. It drives the rotation and translation of its parent (in the hierarchy) by the transformation of the object named in the constraint name.\n\n"
                        
                    elif "point" in obj.name():
                        
                        text = text + "This is a point constraint. It drives the translation of its parent (in the hierarchy) by the translation of the object named in the constraint name.\n\n"
                        
                        
                #otherWise, if it's a joint
                
                elif "JNT" in obj.name():
                    
                    text = text+ "This Is a Joint "
                    
                    #then switch through the next level of possible extensions
                    
                    if "IK" in obj.name():
                        
                        text = text + "which is part of an IK ckain. It is driven by an IK handle and is connected to the bind joint chain."
                    
                    elif "FK" in obj.name():
                        
                        text = text + "which is part of an FK ckain. It is (usually) driven by an FK control and connected to the bind joint chain."
                        
                    elif "Bind" in obj.name():
                        
                        text = text + "which is part of a bind chain, meaning that it needs to be skinned to the mesh during the binding process."
                        
                        if "Twist" in obj.name():
                            
                            text = text + "This is also a twist joint, which means that it is driven by other bind joints, rather than an FK or IK chain, and user to spread twist down limb sections"

                    text = text + "\n\n"
                   
                #if it's related to a control
                
                elif "CTRL" in  obj.name():
                    
                    if "_0" in obj.name():
                        
                        text = text + "This is a 0 group above a control. This is used to \"0\" out the control by having it's transformations in this group. Move with caution, it can be difficult to get it back to it's original position\n\n"
                    
                    elif "_CONST" in obj.name():
                        
                        text = text + "This is a contraint group, used for when you want a control to be driven by another object. Can be used as the place where rig elements are connected together\n\n"
                    
                    elif "_SDK" in obj.name():
                        
                        text = text + "This is an SDK (Set Driven Key) group, used for addind driven keys (where another object drived the control, similar to a constraint but animatable)\n\n"
                        
                    else:
                        
                        text = text + "This is a Control, used for animation."
                        
                        if ("IK" in obj.name()) and not("PV" in obj.name()):
                            
                            text = text + " The position of this control drives the IK joint chain\n\n"
                            
                        elif ("IK" in obj.name()) and ("PV" in obj.name()):
                            
                            text = text + " The position of this control drives the IK knee's pole vector (aim)\n\n"
                            
                        elif "_FK_" in obj.name():
                            
                            text = text + " The rotation of this control drives the rotation of th corresponding FK joint\n\n"
                            
                        elif "FKIK" in obj.name():
                            
                            text = text + " The switch value defines how much the bind chain follows the FK or IK chains\n\n"
                            
                        else:
                            
                            text = text + "\n\n";
                            
                #if it is an ik handle
                
                elif "HNDL" in obj.name():
                    
                    text = text + "This is an IK handle object, which drives the IK chain. This is driven by the position of an IK control\n\n"
                

                #search for side specifier
                
                sideText = ""
                
                if "_L_" in obj.name():
                    
                    sideText  = "on the left-hand side"
                    
                elif "_R_" in obj.name():
                    
                    sideText  = "on the right-hand side"
                    
                elif "_C_" in obj.name():

                    sideText = "in the centre"
                    
                #and then limb name
                
                if "Arm" in obj.name():
                    
                    text = text + "This is part of an Arm element " +sideText + " of the rig.\n\n"
                
                elif "Leg" in obj.name():
                    
                    text = text + "This is part of an Leg element " +sideText + " of the rig.\n\n"
                    
                elif "Spine" in obj.name():
                    
                    text = text + "This is part of a spine element " +sideText + " of the rig.\n\n"
                    
                #and if there is still no text
                
                if text == "":
                    
                    text = "Unknown object"
                    
                self.m_helpText.setLabel(text)
            else:
                
                #display information based on the current tab
            
                #get the info List
                
                inf = self.m_gui.getTabInfo()
                
                #set the label
                
                self.m_helpLabel.setLabel("Tab Type: "+inf[0])
                
                #generate the text
                
                text = ""
                if inf[0] == "Start Tab":
                    
                    text = "This is the start tab, choose a rig element to work on"
                    
                else:
                    if inf[1] and inf[2]:
                        
                        text = "You have generated joint chain. If you are done, close the tab and move on to the next rig element, otherwise change the options or template joints and regenerate the element\n\n"
                        
                    elif not inf[1] and inf [2]:
                        
                        text = "You have generated a joint chain, but no template joints are loaded. If you are done, close the tab and move on to the next rig element. If you want to regenerate the rig element you will need to load in a set of template joints"
                        
                    elif inf [1] and not inf[2]:
                        
                        text = "You have selected the template joints, just set the options you want and generate the rig element"
                        
                    else:
                        
                        text = "Load in a template joint chain and set up your desired options before generating the rig element"
                        
                
                self.m_helpText.setLabel(text)
        
 
        
    def getTopUI (self):
        
        """
            Method: getTopUi
                method to return the top level ui element within the class
        """
        
        return self.m_topLayout
                                     
#----------END-HelpBox-Class----------#       
