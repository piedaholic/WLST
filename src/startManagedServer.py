# Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *  # @UnusedWildImport
 
print 'starting the script ....'

username = sys.argv[1]
password = sys.argv[2]
url = sys.argv[3]
serverName = sys.argv[4]

try:
    connect(username, password, url)
except Exception, e:
    print e 
    print 'Failed to connect to weblogic server '
    print "script returns FAILURE"
    sys.exit(3)
    
try:
    try :
        domainRuntime()
        cd('/ServerRuntimes/'+serverName)
        print 'Server Already Running...Exiting'
        print "script returns FAILURE"
        sys.exit(3)
    except Exception, e:
        try:
            start(serverName, 'Server')
        except Exception, e:
            print e    
            print 'Failed to start '+ serverName
            print "script returns FAILURE"
            sys.exit(3)
        
    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to start " + serverName
    sys.exit(3) 
