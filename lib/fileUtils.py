'''
Created on Oct 28, 2018

@author: hpsingh
'''

#Import Python Modules
import ntpath
import os

def getFileFromPath(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def getDirectoryFromPath(path):
    head = os.path.split(path)
    return head

def getAppName(application):
    appArr = application.split('.')
    return appArr[0]