#!/usr/bin/python

import sys, os, dicom, wx

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
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(800,200))
        
        baseFrame = parent
        
        # Sizers
        self.container  = wx.BoxSizer(wx.VERTICAL)
        self.hboxA      = wx.BoxSizer(wx.HORIZONTAL)
        self.vboxA1     = wx.BoxSizer(wx.VERTICAL)
        self.vboxA2     = wx.BoxSizer(wx.VERTICAL)
        self.hboxB      = wx.BoxSizer(wx.HORIZONTAL)
        
        # Static Text
        self.sourceTxt  = wx.StaticText(self, 0, "Source Directory :")
        self.targetTxt  = wx.StaticText(self, 0, "Target Directory :")
        
        # Text Control
        self.sourceTxtCtrl  = wx.TextCtrl(self, 0, "", size=(600,25))
        self.targetTxtCtrl  = wx.TextCtrl(self, 0, "", size=(600,25))
        
        # Buttons
        self.sourceBtn  = wx.Button(self, 0, "Select Source", size=(150,25))
        self.targetBtn  = wx.Button(self, 0, "Select Target", size=(150,25))
        self.helpBtn    = wx.Button(self, 0, "User's Guide", size=(150,25))
        self.mapBtn     = wx.Button(self, 0, "Map", size=(200,25))
        self.loadBtn    = wx.Button(self, 0, "Load Map", size=(200,25))
        self.saveBtn    = wx.Button(self, 0, "Save Map", size=(200,25))
        
        # Line
        self.line1  = wx.StaticLine(self, 0, size=(800,1))
        self.line2  = wx.StaticLine(self, 0, size=(800,1))
        
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
        
        # Initialization
        self.SetSizer(self.container)
        
        self.Centre()
        
        
class EditTags(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        baseFrame       = parent
        self.tagGroups  = ["One", "Two", "Three"]
        
        # Sizers
        self.container  = wx.BoxSizer(wx.VERTICAL)
        self.vboxA      = wx.BoxSizer(wx.VERTICAL)
        self.hboxA1     = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxB      = wx.BoxSizer(wx.HORIZONTAL)
        self.vboxB1     = wx.BoxSizer(wx.VERTICAL)
        self.vboxC      = wx.BoxSizer(wx.VERTICAL)
        self.hboxC1     = wx.BoxSizer(wx.HORIZONTAL)
        
        # Buttons
        self.removeBtn  = wx.Button(self, 0, "Remove Edit", size=(395,25))
        self.editBtn    = wx.Button(self, 0, "Edit Tag", size=(185,25))
        
        # Checkbox
        self.privateCheck   = wx.CheckBox(self, 0, "Remove Private Tags")
        
        # Combo
        self.tagDrop        = wx.ComboBox(self, 0, size=(790, 25), choices=self.tagGroups, style=wx.CB_READONLY)
        self.patientDrop    = wx.ComboBox(self, 0, size=(600, 25), choices=['Patients List'], style=wx.CB_READONLY)
        
        # Check List Box
        self.tagCLBox   = wx.CheckListBox(self, 0, size=(395,255), choices=[], style=0)
        
        # Text Ctrl
        self.editTc = wx.TextCtrl(self, 0, 'Input field for new Tag value', size=(600,25))
        self.tagTc  = wx.TextCtrl(self, 0, 'Select a Tag to edit it', size=(790,25), style=wx.TE_READONLY)
        
        # List Box
        self.changesLBox    = wx.ListBox(self, 0, size=(395,230), style=wx.TE_MULTILINE)
        
        # Line
        self.line1  = wx.StaticLine(self, 0, size=(800,1))
        
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
        
        self.hboxB.Add(self.tagCLBox)
        self.hboxB.Add(self.vboxB1)
        self.vboxB1.Add(self.changesLBox)
        self.vboxB1.Add(self.removeBtn)
        
        self.vboxC.Add(self.tagTc)
        self.vboxC.AddSpacer((1,5))
        self.vboxC.Add(self.hboxC1)
        self.hboxC1.Add(self.editTc)
        self.hboxC1.Add(self.editBtn, 0, wx.LEFT, 5)
        
        # Initialization
        self.SetSizer(self.container)
        
        self.Centre()
        
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
        self.addTc  = wx.TextCtrl(self, 0, 'Input field for adding Comments', size=(600,25))

        # List Box
        self.commentLBox    = wx.ListBox(self, 0, size=(600,135), style=wx.TE_MULTILINE)
        
        # Layout
        self.container.AddSpacer((1,50))
        self.container.Add(self.vboxA, 0, wx.TOP | wx.LEFT, 5)
        self.container.Add(self.vboxB, 0, wx.LEFT, 25)
        
        self.vboxA.Add(self.commentLBox)
        self.vboxA.AddSpacer((1,2))
        self.vboxA.Add(self.addTc)
        self.vboxA.AddSpacer((1,5))
        self.vboxA.Add(self.hboxA1)
        self.hboxA1.Add(self.addBtn)
        self.hboxA1.Add(self.removeBtn)
        
        self.vboxB.AddSpacer((1,147))
        self.vboxB.Add(self.processBtn)
        self.vboxB.Add(self.batchBtn)
        
        # Initialization
        self.SetSizer(self.container)
        
        self.Centre()
        

if __name__ == "__main__":
    app = wx.App(0)
    main = BaseFrame()
    
    main.Show()
    app.MainLoop()