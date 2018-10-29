
#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport

def getRunningServerNames():
    domainConfig()
    return cmo.getServers()

def monitorRunningServers():
    print 'starting the script ....'
    
    username = sys.argv[1]
    password = sys.argv[2]
    url = sys.argv[3]
    
    try:
        connect(username, password, url)
        print 'Connected to Weblogic Server'
    except Exception, e:
        print e 
        print 'Failed to connect to weblogic server '
        print "script returns FAILURE"
        sys.exit(3)
    
    serverNames = getRunningServerNames()
    domainRuntime()
    for name in serverNames:
        print 'Now checking '+name.getName()
        try:
            cd("/ServerRuntimes/"+name.getName())
        except WLSTException,e:
            # this typically means the server is not active, just ignore
            print e
            pass
        print cmo.getName()
        print cmo.getSocketsOpenedTotalCount()

if __name__== "main":
    monitorRunningServers()
    
