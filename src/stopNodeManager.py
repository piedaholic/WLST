#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport
import ntpath    

print 'starting the script ....'

nmUsername = sys.argv[1]
nmPassword = sys.argv[2]
nmListenPort = sys.argv[3]
nmListenAddress = sys.argv[4] 
domainHome = sys.argv[5]

def getFilenameFromPath(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

domainName = getFilenameFromPath(domainHome)

try:
    nmConnect (nmUsername, nmPassword, nmListenAddress, nmListenPort, domainName, domainHome, 'SSL')
    stopNodeManager()
    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to stop Node Manager!!!"
    sys.exit(3)
    
