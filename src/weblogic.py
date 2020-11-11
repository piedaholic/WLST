# import os
# import sys
from xml.dom import minidom
# import socket
import ntpath;


# Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__':
    from wlstModule import *  # @UnusedWildImport

class Error(Exception):
    """Base class for other exceptions"""
    pass
class ValueTooSmallError(Error):
    """Raised when the input value is too small"""
    pass
class ValueTooLargeError(Error):
    """Raised when the input value is too large"""
    pass

class ServerNotRunningException(Error):
    """Raised when the server is not in Running state"""
    pass

class ServerAlreadyRunningException(Error):
    """Raised when the server is already in Running state"""
    pass

class NullArgumentException(Error):
    """Raised when the server is already in Running state"""
    pass
def getServerStatus(server):
    domainRuntime()
    try:
        cd('/ServerLifeCycleRuntimes/' + server)
        return cmo.getState()
    except:
        print 'Exception occurred while getting server state for ' + server
        dumpStack()

def getServerNames():
    domainConfig()
    return cmo.getServers()

def getRunningServerNames():
    running_servers = list()
    domainRuntime()
    for server in getServerNames():
        try:
            cd('/ServerLifeCycleRuntimes/' + server.getName())
            if cmo.getState() == 'RUNNING':
                running_servers.append(server.getName())
        except:
            print 'Exception occurred while getting server state for ' + server.getName()
            dumpStack()
    return running_servers

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
    head = os.path.split(path)[0]
    return head

def isAppDeployed(app) :
    appFound = False
    serverConfig()
    try:
        cd('/AppDeployments')
        appList = cmo.getAppDeployments()
        for appName in appList:
            if (appName.getName() == app):
                appFound = True
    except WLSTException:
        return False
    return appFound

def getAppTargets(app):
    currDir = pwd()
    serverConfig()
    cd('/AppDeployments/' + app + '/Targets')
    serverNames = ls(returnMap='true', returnType='c')
    cd (currDir)
    return serverNames

def getAppName(application):
    appArr = application.split('.')
    return appArr[0]


def read_properties_file(path):
    prop_file = open(path, "r")
    prop_dict = dict()
    for prop_line in prop_file:
        prop_def = prop_line.strip()
        if len(prop_def) == 0:
            continue
        if prop_def[0] in ('!', '#'):
            continue
        punctuation = [prop_def.find(c) for c in '='] + [len(prop_def)]
        found = min([pos for pos in punctuation if pos != -1])
        name = prop_def[:found].rstrip()
        # print(name)
        value = prop_def[found:].lstrip("=").rstrip()
        # print(value)
        prop_dict[name] = value
    prop_file.close()
    # print propDict
    return prop_dict

# if __name__ == '__main__':
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def multi_getattr(obj, attr, default=None):
    """
    Get a named attribute from an object; multi_getattr(x, 'a.b.c.d') is
    equivalent to x.a.b.c.d. When a default argument is given, it is
    returned when any attribute in the chain doesn't exist; without
    it, an exception is raised when a missing attribute is encountered.
    """
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj

class operation:
    def deploy(self):
        print 'starting the script ....'

        try:
            applications = sys.argv[2]
        except:
            print 'No source file provided for deployment'
            return
        try:
            targets = sys.argv[3]
        except Exception, e:
            print 'No target specified for deployment'
            return
        targetList = targets.split(',')

        applicationList = applications.split(',')
        connect(adminUsername, adminPassword, adminUrl)
        if allTargetsFunctioning(targetList) == True :
            for application in applicationList :
                try :
                    print application
                    appPath = getDirectoryFromPath(application)
                    application = getFilenameFromPath(application)
                    if application.endsWith('jar'):
                        try :
                            deploy(application, appPath, targets, libraryModule='true')
                        except Exception, e:
                            print e
                            print "Error while deploying library" + application
                            sys.exit(3)
                        continue
                    appName = getAppName(application)
                    if isAppDeployed(appName) is True:
                        try:
                            print 'Stopping ' + appName
                            stopApplication(appName)
                        except Exception, e:
                            print 'Exception occured while stopping ' + application
                            # print e
                            # dumpStack()
                            sys.exit(3)

                        try:
                            print 'Undeploying ' + appName
                            undeploy(appName)
                        except Exception, e:
                            print 'Exception occured while undeploying ' + application
                            # print e
                            try :
                                undo('true', 'y')
                            except Exception:
                                print 'Failed to revert after undeploying ' + application + '...Skipping'
                            # dumpStack()
                            sys.exit(3)

                    try:
                        print 'Deploying ' + appName
                        deploy(appName, appPath, targets)
                    except Exception, e:
                            print 'Exception occured while deploying ' + application
                            # print e
                            try :
                                undo('true', 'y')
                            except Exception:
                                print 'Failed to revert after deploying ' + application + '...Skipping'
                            # dumpStack()
                            sys.exit(3)

                    try:
                        print 'Starting ' + appName
                        startApplication(appName)
                    except Exception, e:
                        print 'Exception occured while starting ' + application
                        # print e
                        # dumpStack()
                        sys.exit(3)

                except Exception, e:
                        print e
                        print "Unhandled Exception occurred while deploying " + application
                        dumpStack()
                        sys.exit(3)
        else :
            print 'One of the targets is not functioning...Please Check'
            sys.exit(3)

        print "script returns SUCCESS"
        disconnect()

    def startAdmin(self):
        try:
            nmConnect (nmUsername, nmPassword, nmListenAddress, nmListenPort, domainName, domainHome, 'ssl', 'true')
            if  (nmServerStatus(adminServer) == 'RUNNING') :
                raise ServerAlreadyRunningException
            else:
                nmStart('AdminServer')
        except ServerAlreadyRunningException:
            print 'Admin Server is already Running'
            print "script returns FAILURE"

    def start(self):
        try :
            arg = sys.argv[2]
            if arg == None :
                raise NullArgumentException
        except IndexError:
            print 'ERROR : No/Less argument(s) provided'
            return
        except NullArgumentException:
            print 'ERROR : No/Less argument(s) provided'
            return
        if arg != '-app' :
            try :
                nmConnect (nmUsername, nmPassword, nmListenAddress, nmListenPort, domainName, domainHome, 'ssl', 'true')
                if  (nmServerStatus(server) == 'RUNNING') :
                    raise ServerAlreadyRunningException
                else:
                    nmStart(server)
            except ServerAlreadyRunningException:
                print 'ERROR:' + server + ' is already Running'
                # print "script returns FAILURE"
                return
        elif arg == '-app':
            try :
                sys.argv[3]
            except IndexError:
                print 'ERROR : No/Less argument(s) provided'
            if sys.argv[3] != '-name':
                print 'ERROR : Invalid syntax'
                return
            else :
                try :
                    sys.argv[4]
                except IndexError:
                    print 'ERROR : No/Less argument(s) provided'

                if sys.argv[4] == None :
                    print 'ERROR : Application/Library Name not provided'
                    return
                elif sys.argv[4].startswith('-'):
                    print 'ERROR : Invalid syntax'
                    return
                else :
                    self.startApp(sys.argv[4])


    def startApp(self, appNames):
            try:
                print adminUsername
                print adminPassword
                connect(adminUsername, adminPassword, adminUrl)
                print 'Connected to Weblogic Server'
            except Exception, e:
                print e
                print 'Failed to connect to weblogic server '
                print "script returns FAILURE"
                sys.exit(3)

            try:
                appFound = False
                cd ('AppDeployments')
                appList = cmo.getAppDeployments()
                print appList
                appNamesArr = appNames.split(',')
                for appName in appNamesArr :
                    for app in appList:
                        if app.getName() == appName :
                            appFound = True
                            try:
                                cd('/ApplicationRuntimes/' + appName)
                                print 'Application/Library Already Running'
                            except:
                                print 'Going to start ' + appName
                                startApplication(appName)
                    if appFound == False:
                        print 'ERROR : ' + appName + ' Application/Library Not Deployed in WL Console'
                        return
            except WLSTException:
                print 'ERROR : Unhandeled Exception Occurred'


    def stop(self):
        try :
            server = sys.argv[2]
        except :
            print 'No arguments given'
            print 'script returns FAILURE'
        try:
            shutdown(server, 'Server', 'true', 1000, force='true', block='true')
        except:
            print 'Exception Occurred while shutting down'

    def stopAdmin(self):
        try:
            shutdown(adminServer, 'Server', 'true', 1000, force='true', block='true')
        except:
            print 'Exception Occurred while shutting down'

    def startDomain(self):
        try:
            print 'Going to start Node Manager'
            if self.nm_status() == 'Reachable' :
                print 'Node Manager is Already Running'
            elif self.nm_status() == 'Inactive' :
                startNodeManager(verbose='true', NodeManagerHome=domainHome + os.sep + 'nodemanager', ListenPort=nmListenPort, ListenAddress=nmListenAddress)
            else :
                print 'ERROR : Node Manager Status is unknown'
            print 'Going to start Admin Server'
            try:
                self.startAdmin()
            except ServerAlreadyRunningException:
                print 'Admin Server is already Running'
            print "script returns SUCCESS"
        except Exception, e:
            print e
            print "Error while trying to save and/or activate!!!"
            dumpStack()
            # raise

    def shutdownServer(self, serverName):
        try:
            shutdown(serverName, 'Server', 'true', 1000, force='true', block='true')
        except:
            print 'Exception Occurred while shutting down'
            sys.exit(3)

    def connect(self):
        try:
            connect(adminUsername, adminPassword, adminUrl)
        except:
            print 'Failed to connect'
            return
        disconnect()

    def stopDomain(self):
        try:
            connect(adminUsername, adminPassword, adminUrl)
            servers = getServerNames()
            #disconnect()
        except:
            print 'Failed to get servers list'
            return

        try:
            #connect(adminUsername, adminPassword, adminUrl)
            nmConnect (nmUsername, nmPassword, nmListenAddress, nmListenPort, domainName, domainHome, 'ssl', 'true')
        except:
            print 'Failed to connect to Node Manager'
            return

        try:
            for server in servers:
                    serverStatus = nmServerStatus(server.getName())
                    if serverStatus != 'SHUTDOWN' and server.getName() != adminServer :
                        print 'Shutting down ' + server.getName()
                        #self.shutdownServer(server.getName())
                        nmKill(server.getName())
            try:
                if nmServerStatus(adminServer) == 'RUNNING' :
                        print 'Going to shutdown AdminServer'
                        #shutdown(adminServer, 'Server', 'true', 1000, force='true', block='true')
                        nmKill(adminServer)
                else :
                        print 'Admin Server is not running'
                        print 'Current Status is ' + serverStatus
            except :
                print 'Failed to stop ' + adminServer
            self.stopNM()
            print "script returns SUCCESS"
        except Exception, e:
            print e
            print "Error Occurred!!!"
            dumpStack()
            sys.exit(3)

    def startNM(self):
        try:
            startNodeManager(verbose='true', NodeManagerHome=domainHome + os.sep + 'nodemanager', ListenPort=nmListenPort, ListenAddress=nmListenAddress)
            print "script returns SUCCESS"
        except Exception, e:
            print e
            print "Error while trying to start Node Manager!!!"

    def stopNM(self):
        try:
            nmConnect (nmUsername, nmPassword, nmListenAddress, nmListenPort, domainName, domainHome, 'SSL')
            stopNodeManager()
            print "script returns SUCCESS"
        except Exception, e:
            print e
            print "Error while trying to stop Node Manager!!!"


    def monitor(self):
        print 'starting the script ....'

        try:
            connect(adminUsername, adminPassword, adminUrl)
            print 'Connected to Weblogic Server'
        except Exception, e:
            print e
            print 'Failed to connect to weblogic server '
            print "script returns FAILURE"
            sys.exit(3)
        serverNames = getServerNames()
        domainRuntime()
        print '**********************************************************************'
        for serverName in serverNames:
            # print 'Now checking ' + serverName.getName()
            try:
                cd("/ServerRuntimes/" + serverName.getName())
                print 'Server Name : ' + cmo.getName()
                print 'Server Status : ' + cmo.getState()
                print 'Total Number of open sockets ' + str(cmo.getSocketsOpenedTotalCount())
                cd('JVMRuntime/' + serverName.getName())
                ls()
                print '**********************************************************************'
            except WLSTException:
                # this typically means the server is not active, just ignore
                # print e
                pass

    def checkHealth(self, serverName):
        while 1:
            slBean = self.getSLCRT(serverName)
            status = slBean.getState()
            print 'Status of Managed Server is ' + status
            # if status != "RUNNING":
            #  print 'Starting server ' + serverName
            #  start(serverName, block="true")
            time.sleep(5)

    def nm_status(self):
        NMstatus = os.system('jps |grep -i nodemanager|grep -v grep')
        if NMstatus == 0:
                return 'Reachable'
        else:
                return 'Inactive'

    def getSLCRT(self, svrName):
        domainRuntime()
        slrBean = cmo.lookupServerLifecycleRuntime(svrName)
        return slrBean

    def monitorJVMHeapSize(self):
        # waitTime=300000
        THRESHOLD = 100000000
        # connect(adminUsername, adminPassword, adminUrl)
        while 1:
            serverNames = getRunningServerNames()
            domainRuntime()
            for name in serverNames:
                print 'Now checking ' + name.getName()
                try:
                    cd("/ServerRuntimes/" + name.getName() + "/JVMRuntime/" + name.getName())
                except WLSTException:
                    # this typically means the server is not active, just ignore
                    pass
                heapSize = cmo.getHeapSizeCurrent()
                if heapSize > THRESHOLD:
                # do whatever is neccessary, send alerts, send email etc
                    print 'WARNING: The HEAPSIZE is Greater than the Threshold'
                else:
                    print heapSize
            java.lang.Thread.sleep(1800000)


try:
    # os.environ['DOMAIN_HOME'] = 'C:\\Oracle\\Middleware_JDev12c\\Oracle_Home\\user_projects\\domains\\base_domain'
    domainHome = os.environ.get('DOMAIN_HOME')
    domainName = getFilenameFromPath(domainHome)
    # print ('domainHome:' + domainHome)
    configXml = domainHome + os.sep + 'config' + os.sep + 'config.xml'
    # print ('configXml:' + configXml)
    doc = minidom.parse(configXml)
    nmUsername = doc.getElementsByTagName('node-manager-username')[0].firstChild.data
    service = weblogic.security.internal.SerializedSystemIni.getEncryptionService(domainHome)
    encryption = weblogic.security.internal.encryption.ClearOrEncryptedService(service)
    nmPassword = encryption.decrypt(doc.getElementsByTagName('node-manager-password-encrypted')[0].firstChild.data)
    properties = read_properties_file(
            os.environ.get('DOMAIN_HOME') + os.sep + 'nodemanager' + os.sep + 'nodemanager.properties')
    nmListenPort = properties.get('ListenPort')
    nmListenAddress = properties.get('ListenAddress')
    properties = read_properties_file(
    os.environ.get(
                'DOMAIN_HOME') + os.sep + 'servers' + os.sep + 'AdminServer' + os.sep + 'security' + os.sep + 'boot.properties')
    adminServer = doc.getElementsByTagName('admin-server-name')[0].firstChild.data
    adminUsername = encryption.decrypt(properties.get('username'))  # properties.get('username')
    adminPassword = encryption.decrypt(properties.get('password'))
    servers = doc.getElementsByTagName('server')
    for server in servers:
        serverName = server.getElementsByTagName('name')[0].firstChild.data
        if serverName == adminServer:
            try:
                if server.getElementsByTagName('listen-address')[0].firstChild != None :
                    adminListenAddress = server.getElementsByTagName('listen-address')[0].firstChild.data
                else:
                    adminListenAddress = socket.gethostname()
            except Exception, e:
                adminListenAddress = socket.gethostname()
            try:
                ssl_enabled = server.getElementsByTagName('ssl')[0].getElementsByTagName('enabled')[0].firstChild.data
            except Exception, e:
                ssl_enabled = 'false'
            if ssl_enabled == 'true' :
                adminListenPort = server.getElementsByTagName('ssl')[0].getElementsByTagName('listen-port')[0].firstChild.data
                adminConnectProtocol = 't3s'
            else:
                for child in server.childNodes:
                    if child.nodeType == child.ELEMENT_NODE and (child.tagName == 'listen-port'):
                        if child.firstChild != None:
                            adminListenPort = child.firstChild.data
                        else:
                            adminListenPort = '7001'
                    adminConnectProtocol = 't3'
    adminUrl = adminConnectProtocol + "://" + adminListenAddress + ':' + adminListenPort
    # print 'Admin URL is ' + adminUrl
    method = sys.argv[1]
    # print method
    obj = operation()
    getattr(obj, "%s" % method, 'Not Found')()
except :
    print 'Phata mc'
