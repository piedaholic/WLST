
# Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *  # @UnusedWildImport
import ntpath    

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

def getFilenameFromPath(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def getDirectoryFromPath(path):
    head,tail = os.path.split(path)
    return head

def isAppDeployed(app) :
    appFound =False
    serverConfig()
    try:
        cd('/AppDeployments')
        appList=cmo.getAppDeployments()
        for appName in appList:
            if (appName.getName() == app):
                appFound = True 
    except WLSTException:  
        return False            
    return appFound

def getAppName(application):
    appArr = application.split('.')
    return appArr[0]

print 'starting the script ....'
username = sys.argv[1]
password = sys.argv[2]
url = sys.argv[3]
targetList = sys.argv[4].split(',')
applicationList = sys.argv[5].split(',')
connect(username, password, url)

if allTargetsFunctioning(targetList) == True :
    for application in applicationList :
        try :
            print application
            appPath = getDirectoryFromPath(application)
            application = getFilenameFromPath(application)
            appName = getAppName(application)
            if isAppDeployed(appName) is True:
                try:
                    print 'Stopping ' + appName
                    stopApplication(appName)
                except Exception, e:
                    print 'Exception occured while stopping ' + application
                    #print e
                    #dumpStack()
                    sys.exit(3)
                    
                try:
                    print 'Undeploying ' + appName    
                    undeploy(appName)
                except Exception, e:
                    print 'Exception occured while undeploying ' + application
                    #print e
                    try :
                        undo('true', 'y')
                    except Exception:
                        print 'Failed to revert after undeploying '+application+'...Skipping' 
                    #dumpStack()
                    sys.exit(3)
                
            try:
                print 'Deploying ' + appName     
                deploy(appName, appPath, sys.argv[4])
            except Exception, e:
                    print 'Exception occured while deploying ' + application
                    #print e
                    try :
                        undo('true', 'y')
                    except Exception:
                        print 'Failed to revert after deploying '+application+'...Skipping'    
                    #dumpStack()
                    sys.exit(3)
                
            try:
                print 'Starting ' + appName
                startApplication(appName)
            except Exception, e:
                print 'Exception occured while starting ' + application
                #print e
                #dumpStack()
                sys.exit(3)
                           
        except Exception, e:
                print e 
                print "Unhandled Exception occurred while deploying " + application   
                dumpStack()
                sys.exit(3)
else :
    print 'One of the targets is not functioning...Please Check'
    sys.exit(3)

try:

    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to save and/or activate!!!"
    dumpStack()
    raise 
    
