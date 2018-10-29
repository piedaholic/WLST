'''
Created on Oct 28, 2018

@author: hpsingh
'''

#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport
    
#Import Java Utilities
from java.io import FileInputStream    

def loadPropsFil(propsFil):
    inStream = FileInputStream(propsFil)
    propFil = Properties()
    propFil.load(inStream) 
    return propFil

def getRunningServerNames():
    domainConfig()
    return cmo.getServers()

def doesServerExist(serverName):
    serverFound = False
    serverNames = getRunningServerNames()
    for server in serverNames:
        if (server.getName() == serverName):
            serverFound = True
    return serverFound        

def isServerActive(serverName):
    domainRuntime()
    try:
        cd("/ServerRuntimes/" + serverName)
        serverActive = True
    except WLSTException:
        serverActive = False     
    return serverActive

def allTargetsFunctioning(targetList):
    for target in targetList:
        if isServerActive(target) is not True or doesServerExist(target) is not True :
            return False
    return True   
