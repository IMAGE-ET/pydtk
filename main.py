#!/usr/bin/python

import sys, os, dicom, wx, resources, logic

res = resources.Resources()
logic = logic.Logic()

class BaseFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="pyDTK : DICOM Toolkit", size=(800,715))
        
        # Panels
        self.panel  = wx.Panel(self)
        self.file   = FileSelection(self.panel)
        self.edit   = EditTags(self.panel)
        self.add    = AddTags(self.panel)
        
        # Sizers
        self.container  = wx.BoxSizer(wx.VERTICAL)
        
        # Layout
        self.container.Add(self.file)
        self.container.Add(self.edit)
        self.container.Add(self.add)
        
        self.panel.SetSizer(self.container)
        
        self.Centre()
        
class FileSelection(wx.Panel):
    
    sPath = "/Users/jxu1/Documents/DICOM/dump/1/109-004/"
    tPath = "/Users/jxu1/Documents/DICOM/dump2/"
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(800,200))
        
        baseFrame = parent
        
        # Sizers
        self.container = wx.BoxSizer(wx.VERTICAL)
        self.hboxA = wx.BoxSizer(wx.HORIZONTAL)
        self.vboxA1 = wx.BoxSizer(wx.VERTICAL)
        self.vboxA2 = wx.BoxSizer(wx.VERTICAL)
        self.hboxB = wx.BoxSizer(wx.HORIZONTAL)
        
        # Static Text
        self.sourceTxt = wx.StaticText(self, 0, "Source Directory :")
        self.targetTxt = wx.StaticText(self, 0, "Target Directory :")
        
        # Text Control
        self.sourceTxtCtrl = wx.TextCtrl(self, 0, "", size=(600,25))
        self.targetTxtCtrl = wx.TextCtrl(self, 0, "", size=(600,25))
        
        # Buttons
        self.sourceBtn = wx.Button(self, 0, "Select Source", size=(150,25))
        self.targetBtn = wx.Button(self, 0, "Select Target", size=(150,25))
        self.helpBtn = wx.Button(self, 0, "User's Guide", size=(150,25))
        self.mapBtn = wx.Button(self, 0, "Map", size=(200,25))
        self.loadBtn = wx.Button(self, 0, "Load Map", size=(200,25))
        self.saveBtn = wx.Button(self, 0, "Save Map", size=(200,25))
        
        # Line
        self.line1 = wx.StaticLine(self, 0, size=(800,1))
        self.line2 = wx.StaticLine(self, 0, size=(800,1))
        
        # Dialog
        self.missingName = wx.MessageDialog(self, 'There were files without a Patient\'s Name, please check the runlog.txt for more information', 'Notice!', wx.OK | wx.ICON_INFORMATION)
        
        # Layout
        self.container.Add(self.hboxA)
        self.hboxA.Add(self.vboxA1, 0, wx.LEFT, 5)
        self.hboxA.Add(self.vboxA2, 0, wx.LEFT, 25)
        self.container.Add(self.line1, 0, wx.TOP, 5)
        self.container.Add(self.hboxB)
        self.container.Add(self.line2)
        
        self.vboxA1.Add(self.sourceTxt)
        self.vboxA1.Add(self.sourceTxtCtrl)
        self.vboxA1.Add(self.targetTxt)
        self.vboxA1.Add(self.targetTxtCtrl)
        
        self.vboxA2.AddSpacer((1,15))
        self.vboxA2.Add(self.sourceBtn)
        self.vboxA2.AddSpacer((1,15))
        self.vboxA2.Add(self.targetBtn)
        
        self.hboxB.AddSpacer((5,1))
        self.hboxB.Add(self.mapBtn, 0, wx.TOP, 5)
        self.hboxB.Add(self.loadBtn, 0, wx.TOP, 5)
        self.hboxB.Add(self.saveBtn, 0, wx.TOP, 5)
        self.hboxB.AddSpacer((25,1))
        self.hboxB.Add(self.helpBtn, 0, wx.TOP, 5)
        
        # Bindings
        self.sourceBtn.Bind(wx.EVT_BUTTON, self.setSource)
        self.targetBtn.Bind(wx.EVT_BUTTON, self.setTarget)
        self.helpBtn.Bind(wx.EVT_BUTTON, self.help)
        self.mapBtn.Bind(wx.EVT_BUTTON, self.mapper)
        self.loadBtn.Bind(wx.EVT_BUTTON, self.loadMap)
        self.saveBtn.Bind(wx.EVT_BUTTON, self.saveMap)
        
        # Initialization
        self.SetSizer(self.container)
        
        self.Centre()
        
    # Handlers    
    def setSource(self, event):
        self.filePrompt = wx.DirDialog(self, "Choose the Source Directory:", style=wx.DD_DEFAULT_STYLE)
        
        if self.filePrompt.ShowModal() == wx.ID_OK:
            FileSelection.sPath = self.filePrompt.GetPath() + '/'
            self.sourceTxtCtrl.SetValue(FileSelection.sPath)
            
        self.filePrompt.Destroy()
        
    def setTarget(self, event):
        self.filePrompt = wx.DirDialog(self, "Choose the Target Directory:", style=wx.DD_DEFAULT_STYLE)
        
        if self.filePrompt.ShowModal() == wx.ID_OK:
            FileSelection.tPath = self.filePrompt.GetPath() + '/'
            self.targetTxtCtrl.SetValue(FileSelection.tPath)
        
        self.filePrompt.Destroy()
        
    def help(self, event):
        for e in res.DicomDictionary.items():
            print e
        
    def mapper(self, event):
        self.flaggedFiles = []
        self.missingName = False
        
        for dirname, dirs, files, in os.walk(FileSelection.sPath):
            for filename in files:
                fPath = dirname + '/' + filename
                path = dirname.split("/")
                if isDicom(fPath):
                    ds = dicom.read_file(fPath)
                    if ds.PatientsName == "":
                        self.flaggedFiles.append(fPath)
                        self.missingName = True
                    else:
                        logic.getPatients(self, ds)
                        
        if self.missingName:
            timeStamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            logName = "logs/log_" + timeStamp + ".txt"
            errorFile = open(logName, 'wb')
            errorFile.write("The following files are flagged for not having a Patient\'s Name:\n")
                
            for filename in self.flaggedFiles:
                errorFile.write(filename + "\n")
                
            self.missingName.ShowModal()
            self.missingName.Destroy()
                        
        logic.genMap(self)
        
    
    def loadMap(self, event):
        print "Load Button"
        
    def saveMap(self, event):
        print "Save Button"
        
class EditTags(wx.Panel):
    
    patients    = {}
    changedTags = {}
    tagList     = []
    currentTags = []
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        global baseTags
        
        baseFrame = parent
        
        # Sizers
        self.container = wx.BoxSizer(wx.VERTICAL)
        self.vboxA = wx.BoxSizer(wx.VERTICAL)
        self.hboxA1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxB = wx.BoxSizer(wx.HORIZONTAL)
        self.vboxB1 = wx.BoxSizer(wx.VERTICAL)
        self.vboxC = wx.BoxSizer(wx.VERTICAL)
        self.hboxC1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxC2 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Buttons
        self.editBtn = wx.Button(self, 0, "Edit Tag", size=(185,25))
        self.removeBtn = wx.Button(self, 0, "Remove Tag", size=(185,25))
        
        # Checkbox
        self.privateCheck = wx.CheckBox(self, 0, "Remove Private Tags")
        
        # Combo
        self.tagDrop = wx.ComboBox(self, 0, size=(790, 25), choices=res.tagGroups, style=wx.CB_READONLY)
        self.patientDrop = wx.ComboBox(self, 0, size=(600, 25), choices=['Patients List'], style=wx.CB_READONLY)
    
        # Text Ctrl
        self.editTc = wx.TextCtrl(self, 0, 'Input field for new Tag value', size=(600,25))
        self.tagTc = wx.TextCtrl(self, 0, 'Select a Tag to edit it', size=(600,25), style=wx.TE_READONLY)
        
        # List Box
        self.changesLBox = wx.ListBox(self, 0, size=(395,255), style=wx.TE_MULTILINE)
        self.tagLBox = wx.ListBox(self, 0, size=(395,255), choices=sorted(EditTags.tagList), style=wx.TE_MULTILINE)
        
        # Line
        self.line1 = wx.StaticLine(self, 0, size=(800,1))
        
        # Layout
        self.container.AddSpacer((1,5))
        self.container.Add(self.vboxA)
        self.container.Add(self.hboxB, 0, wx.LEFT, 5)
        self.container.AddSpacer((1,5))
        self.container.Add(self.vboxC, 0, wx.LEFT, 5)
        self.container.Add(self.line1, 0, wx.TOP, 5)
        
        self.vboxA.Add(self.hboxA1, 0, wx.LEFT, 5)
        self.hboxA1.Add(self.patientDrop)
        self.hboxA1.Add(self.privateCheck, 0, wx.LEFT, 25)
        self.vboxA.Add(self.tagDrop, 0, wx.LEFT, 5)
        
        self.hboxB.Add(self.tagLBox)
        self.hboxB.Add(self.vboxB1)
        self.vboxB1.Add(self.changesLBox)
        
        self.vboxC.Add(self.hboxC1)
        self.hboxC1.Add(self.tagTc)
        self.hboxC1.Add(self.removeBtn, 0, wx.LEFT, 5)
        self.vboxC.AddSpacer((1,5))
        self.vboxC.Add(self.hboxC2)
        self.hboxC2.Add(self.editTc)
        self.hboxC2.Add(self.editBtn, 0, wx.LEFT, 5)
        
        # Bindings
        self.editBtn.Bind(wx.EVT_BUTTON, self.editTag)
        self.tagDrop.Bind(wx.EVT_COMBOBOX, self.setTagGroup)
        self.patientDrop.Bind(wx.EVT_COMBOBOX, self.setPatient)
        self.tagLBox.Bind(wx.EVT_LISTBOX, self.tagSelected)
        self.changesLBox.Bind(wx.EVT_LISTBOX, self.changeSelected)
        self.removeBtn.Bind(wx.EVT_BUTTON, self.removeEdit)
        
        # Initialization
        self.SetSizer(self.container)
        self.Centre()
        self.tagDrop.SetValue('0010 : Patient Information')
        self.patientDrop.SetValue('Patients List')
        
        
    # Handlers
    def setTagGroup(self, event):
        self.group = self.tagDrop.GetValue()[:4]
        EditTags.tagList = []
        
        self.tagLBox.Clear()
        
        for tag in res.DicomDictionary.items():
            groupID = tag[0][2:6]
            if groupID == self.group:
                EditTags.tagList.append(tag[1][2])
        
        self.tagLBox.InsertItems(items=sorted(EditTags.tagList), pos=0)
    
    def editTag(self, event):
        self.newValue = self.editTc.GetValue()
        self.tagName = self.tagTc.GetValue()
        
        self.changesLBox.Clear()
        
        EditTags.changedTags[self.tagName] = self.newValue
        
        for pair in EditTags.changedTags.items():
            self.insertValue = pair[0] + " => " + pair[1]
            self.changesLBox.Insert(item=self.insertValue, pos=0)
            
    def removeEdit(self, event):
        self.id = event.GetSelection()
        self.tagName = self.tagTc.GetValue()
        
        del EditTags.changedTags[self.tagName]
        
        self.changesLBox.Clear()
        
        for pair in EditTags.changedTags.items():
            self.insertValue = pair[0] + " => " + pair[1]
            self.changesLBox.Insert(item=self.insertValue, pos=0)
        
        
    def tagSelected(self, event):
        self.id = event.GetSelection()
        self.selectedTag = self.tagLBox.GetString(self.id)
        
        self.tagTc.SetValue(self.selectedTag)
        
        if self.selectedTag not in self.changedTags.keys():
            self.editTc.SetValue("")
        else:
            self.editTc.SetValue(EditTags.changedTags[self.selectedTag])
            
    def changeSelected(self, event):
        self.id = event.GetSelection()
        self.selectedTag = self.changesLBox.GetString(self.id)
        self.tagName = self.selectedTag.split(" => ")[0]
        self.tagValue = self.selectedTag.split(" => ")[1]
        
        self.tagTc.SetValue(self.tagName)
        self.editTc.SetValue(self.tagValue)
        
    def setPatient(self, event):
        pass
        
class AddTags(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        baseFrame = parent

        # Sizers
        self.container  = wx.BoxSizer(wx.HORIZONTAL)
        self.vboxA      = wx.BoxSizer(wx.VERTICAL)
        self.hboxA1     = wx.BoxSizer(wx.HORIZONTAL)
        self.vboxB      = wx.BoxSizer(wx.VERTICAL)
        
        # Buttons
        self.addBtn     = wx.Button(self, 0, "Add", size=(300,25))
        self.removeBtn  = wx.Button(self, 0, "Remove", size=(300,25))
        self.processBtn = wx.Button(self, 0, "Process", size=(150,25))
        self.batchBtn   = wx.Button(self, 0, "Batch Process", size=(150,25))
        
        # Text Ctrl
        self.addTc      = wx.TextCtrl(self, 0, 'Input field for adding Comments', size=(596,25))

        # List Box
        self.commentLBox    = wx.ListBox(self, 0, size=(600,135), style=wx.TE_MULTILINE)
        
        # Layout
        self.container.AddSpacer((1,50))
        self.container.Add(self.vboxA, 0, wx.TOP | wx.LEFT, 5)
        self.container.Add(self.vboxB, 0, wx.LEFT, 25)
        
        self.vboxA.Add(self.commentLBox)
        self.vboxA.AddSpacer((1,2))
        self.vboxA.Add(self.addTc, 0, wx.LEFT, 2)
        self.vboxA.AddSpacer((1,5))
        self.vboxA.Add(self.hboxA1)
        self.hboxA1.Add(self.addBtn)
        self.hboxA1.Add(self.removeBtn)
        
        self.vboxB.AddSpacer((1,148))
        self.vboxB.Add(self.processBtn)
        self.vboxB.Add(self.batchBtn)
        
        # Bindings
        self.addBtn.Bind(wx.EVT_BUTTON, self.addComment)
        self.removeBtn.Bind(wx.EVT_BUTTON, self.removeComment)
        self.processBtn.Bind(wx.EVT_BUTTON, self.process)
        self.batchBtn.Bind(wx.EVT_BUTTON, self.batchProcess)
        
        # Initialization
        self.SetSizer(self.container)
        
        self.Centre()
        
    # Handlers
    def addComment(self, event):
        print "Add Button"
        
    def removeComment(self, event):
        print "Remove Button"
        
    def process(self, event):
        print "Process Button"
        
    def batchProcess(self, event):
        redir = RedirectText(self.addTc)
        for i in res.DicomDictionary.keys():
            sys.stdout = redir
            Printer(i)
        
def Error(message, title='Error', parent=None):
    dlg = wx.MessageDialog(parent, message, title, wx.OK | wx.ICON_ERROR)
    dlg.CenterOnParent()
    dlg.ShowModal()
    dlg.Destroy()
    

class RedirectText:
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)
    
class Printer(object):
    def __init__(self, data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        #sys.stdout.flush()
    
def isDicom(filename):
    try:
        return dicom.read_file(filename) 
    except dicom.filereader.InvalidDicomError:
        return False
    
if __name__ == "__main__":
    
    for tag in res.DicomDictionary.items():
        groupID = tag[0][2:6]
        if groupID == "0010":
            EditTags.tagList.append(tag[1][2])
    
    app = wx.App(0)
    main = BaseFrame()
    main.Show()
    app.MainLoop()
    