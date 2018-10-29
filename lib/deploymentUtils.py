'''
Created on Oct 28, 2018

@author: hpsingh
'''

# Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *  # @UnusedWildImport

def isAppDeployed(app) :
    appFound =False
    domainRuntime()
    try:
        cd('/AppDeployments')
        appList=cmo.getAppDeployments()
        for appName in appList:
            if (appName.getName() == app):
                appFound = True 
    except WLSTException:  
        return False            
    return appFound      

def isLibDeployed(lib) :
    libFound =False
    domainRuntime()
    try:
        cd('/Libraries')
        libList = ls(returnMap='true')
        for libraryArray in libList:
            libName = libraryArray.split('#')
            if (libName[1] == lib):
                    libFound = True 
    except WLSTException:  
        return False            
    return libFound

def isAppTargeted(app, server):
    currDir = pwd()
    serverConfig()
    cd('/AppDeployments/'+app+'/Targets')
    serverNames = ls(returnMap='true',returnType='c')
    cd('../../')
    for serverName in serverNames :
        if (serverName == server):
            cd (currDir)
            return True
    cd (currDir)    
    return False

def isLibTargeted(lib, server):
    currDir = pwd()
    serverConfig()
    cd('/Libraries/'+lib+'/Targets')
    serverNames = ls(returnMap='true',returnType='c')
    for serverName in serverNames :
        if (serverName == server):
            cd (currDir)
            return True
    cd (currDir)    
    return False

def getAppTargets(app):
    currDir = pwd()
    serverConfig()
    cd('/AppDeployments/'+app+'/Targets')
    serverNames = ls(returnMap='true',returnType='c')
    cd (currDir)
    return serverNames

def getLibTargets(lib):
    currDir = pwd()
    serverConfig()
    cd('/AppDeployments/'+lib+'/Targets')
    serverNames = ls(returnMap='true',returnType='c')
    cd (currDir)
    return serverNames
    
def removeAppExistingTargets(app, targetList):
    for target in targetList:
        if isAppTargeted(app, target) is True:
            targetList.remove(target)
    return targetList        
        
def removeLibExistingTargets(lib, targetList):
    for target in targetList:
        if isLibTargeted(lib, target) is True:
            targetList.remove(target)
    return targetList  
            