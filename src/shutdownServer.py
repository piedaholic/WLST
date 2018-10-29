#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport

username = sys.argv[1]
password = sys.argv[2]
url = sys.argv[3]
serverName = sys.argv[4]

connect(username,password,url)
try:
    try :
        domainRuntime()
        cd('/ServerRuntimes/'+serverName)
        shutdown(serverName,'Server', ignoreSessions='true')
    except Exception, e:  
        print 'Server not Running...Exiting'
        sys.exit(3)  
    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to shutdown " + serverName
    dumpStack()
    raise 
    
