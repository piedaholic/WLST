import ntpath

#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport

print 'starting the script ....'

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

username = sys.argv[1]
password = sys.argv[2]
url = sys.argv[3]
targetList=sys.argv[4].split(',')
libraryList = sys.argv[5].split(',')

connect(username,password,url)
edit()
startEdit()
if allTargetsFunctioning(targetList) is True :
    for library in libraryList :
        try :
            deploy(getFilenameFromPath(library), getDirectoryFromPath(library), sys.argv[4], libraryModule = 'true')
        except Exception, e:
                print e 
                print "Error while deploying library"+library
                sys.exit(3)
else :
    print 'One of the targets is not functioning...Please Check'
    sys.exit(3)

try:
    save()
    activate(block="true")
    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to save and/or activate!!!"
    undo('true', 'y')
    sys.exit(3)
    
print "script returns SUCCESS"   

disconnect()
exit() 