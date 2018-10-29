
#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport

#Import utility WLST Python Modules
from lib import commonUtils
from lib import fileUtils

print 'starting the script ....'
username = sys.argv[1]
password = sys.argv[2]
url = sys.argv[3]
targetList=sys.argv[4].split(',')
libraryList = sys.argv[5].split(',')

connect(username,password,url)
edit()
startEdit()
if commonUtils.allTargetsFunctioning(targetList) is True :
    for library in libraryList :
        try :
            deploy(fileUtils.getFilenameFromPath(library), fileUtils.getDirectoryFromPath(library), sys.argv[4], libraryModule = 'true')
        except Exception, e:
                print e 
                print "Error while deploying library"+library
                dumpStack()
                undo('true', 'y')
                raise
                sys.exit(3)
else :
    print 'One of the targets is not functioning...Please Check'
    undo('true', 'y')
    raise
    sys.exit(3)

try:
    save()
    activate(block="true")
    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to save and/or activate!!!"
    undo('true', 'y')
    dumpStack()
    raise 
    
