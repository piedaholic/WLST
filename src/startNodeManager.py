#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport

print 'starting the script ....'

domainHome = sys.argv[1]
nmListenPort = sys.argv[2]
nmListenAddress = sys.argv[3]

try:
    startNodeManager(verbose='true', NodeManagerHome=domainHome+os.sep+'nodemanager', ListenPort=nmListenPort, ListenAddress=nmListenAddress)
    print "script returns SUCCESS"   
except Exception, e:
    print e 
    print "Error while trying to start Node Manager!!!"
    sys.exit(3)