#!/usr/bin/python

import sys, os, dicom, wx, resources

class Logic():
    
    finalPatients   = []
    
    def getPatients(self, parent, dataset):
        ui              = parent
        name            = dataset.PatientsName
        
        if name not in Logic.finalPatients:
            Logic.finalPatients.append(name)
            
    def genMap(self, parent):
        ui = parent
        
        pass