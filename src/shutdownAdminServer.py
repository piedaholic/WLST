import ntpath

#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport

print 'starting the script ....'

nmUsername = sys.argv[1]
nmPassword = sys.argv[2]
nmListenPort = sys.argv[3]
nmListenAddress = sys.argv[4] 
domainHome = sys.argv[5]
adminServerName = sys.argv[6]

def getFilenameFromPath(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

domainName = getFilenameFromPath(domainHome)

try:
    nmConnect (nmUsername, nmPassword, nmListenAddress, nmListenPort, domainName, domainHome, 'SSL')
    if nmServerStatus(adminServerName) == 'SHUTDOWN':
        print 'Server Already Shutdown...Exiting'
        sys.exit(3)
    else:      
        nmKill(adminServerName)
    print "script returns SUCCESS"   
    exit()
except Exception, e:
    print e 
    print "Error while trying to shutdown Admin Server!!!"
    sys.exit(3)
    
