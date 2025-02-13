"""
TODO LIST:

    - Get mirai python built with _ssl and bz2
    - Fix up patcher.
    - Graphical User Interface (inb4 python needs m0ar)
"""
from fsm.FSM import FSM
import urllib, json, sys, os, subprocess, threading, time, stat, getpass
import settings, localizer, messagetypes
from urllib.request import urlopen
from urllib.parse import urlencode
import os

import http.client as httplib
DEVMODE = settings.devmode
MACOS_PATH = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Toontown Rewritten")
class TTRLauncher(FSM):
    """
    This is the "main" class that powers the Toontown Rewritten launcher. It manages
    everything the launcher needs to do, including manage all the "sub-threads" that
    carry out tasks such as patching.
    
    As of right now, the launcher consists of 3 threads:
    
        - "main-thread": This is the thread which holds this class, and keeps everything
        running properly. This also manages state transitions as well as submitting
        data to and from the web server.
    
        - "graphical": This thread will hold the GUI side of the launcher, such as abs
        wyPython interface. Usually, this is what the end user will see when running the
        launcher.
    
        - "patcher": Since the majority of the patching process is locking, it has to be
        run on a separate thread to keep the main thread alive. This thread will deal with
        all the files it needs to download, as well as update/patch. During the download
        process, the patcher will also report back the current download percentage of the
        current file it is downloading.
    
    ERR001: This occurs when the website returns broken JSON.
    ERR002: This occurs when the website returns a Non-OK response when authenticating.
    ERR003: We got a response, but the data received was invalid.
    ERR004: The response said our login was invalid (failed).
    ERR005: User tried to submit TFA code without entering anything.
    ERR006: Account server is temporarily unavailable (HTTP 503).
    """

    def __init__(self, input, output):
        FSM.__init__(self)
        self.input = input
        self.output = output
        self.transitions = {'Off': [
                 'CheckForUpdates', 'Off', 'LaunchGame'], 
           'CheckForUpdates': [
                             'Patch', 'Off'], 
           'GetCredentials': [
                            'SubmitCredentials', 'Off'], 
           'SubmitCredentials': [
                               'LoginResponse', 'Off'], 
           'LoginResponse': [
                           'GetCredentials', 'GetTFACode', 'Delayed', 'LaunchGame', 'Off'], 
           'GetTFACode': [
                        'SubmitTFACode', 'GetCredentials', 'Off'], 
           'SubmitTFACode': [
                           'LoginResponse', 'Off'], 
           'Delayed': [
                     'CheckQueue', 'Off'], 
           'CheckQueue': [
                        'LoginResponse', 'Off'], 
           'Patch': [
                   'GetCredentials', 'Off'], 
           'LaunchGame': [
                        'GetCredentials', 'Off']}
        self.version = settings.Version
        self.connection = None
        self.gameserver = None
        self.cookie = None
        self.authToken = None
        self.authBanner = None
        self.appToken = None
        self.queueToken = None
        self.patcher = None
        self.interface = None
        self.credentials = None
        self.dontClearMessage = False
        return

    def sendOutput(self, data):
        self.output.put(data, block=True, timeout=0.5)

    def start(self):
        self.sendOutput((messagetypes.LAUNCHER_STATUS, ''))
        self.request('CheckForUpdates')

    def enterCheckForUpdates(self):
        self.request('Patch')
        return

    def enterGetCredentials(self):
        if self.dontClearMessage:
            self.dontClearMessage = False
        else:
            self.sendOutput((messagetypes.LAUNCHER_STATUS, ''))
        if self.credentials is None:
            username, password = self.input.get(block=True, timeout=None)
            self.credentials = (username, password)
        else:
            username, password = self.credentials
        self.request('SubmitCredentials', username, password)
        return

    def enterSubmitCredentials(self, username, password):
        self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.GUI_Authing))
        self.connection = httplib.HTTPSConnection(*settings.SSLConnection)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        params = urlencode({'username': username.encode('utf8'), 
           'password': password.encode('utf8')})
        self.connection.request('POST', settings.LoginPostLocation, params, headers)
        self.request('LoginResponse')

    def enterLoginResponse(self):
        try:
            response = self.connection.getresponse()
        except httplib.BadStatusLine:
            self.sendOutput((messagetypes.LAUNCHER_ERROR, 'ERR006: %s' % localizer.ERR_AccServerDown))
            self.credentials = None
            self.request('GetCredentials')
        else:
            if response.status == httplib.SERVICE_UNAVAILABLE:
                self.sendOutput((messagetypes.LAUNCHER_ERROR, 'ERR006: %s' % localizer.ERR_AccServerDown))
                self.credentials = None
                self.request('GetCredentials')
            if response.status != httplib.OK:
                self.sendOutput((messagetypes.LAUNCHER_ERROR, 'ERR002: %s' % localizer.ERR_Non200Resp % {'response': str(response.status)}))
                self.credentials = None
                self.request('GetCredentials')
            try:
                data = json.loads(response.read().decode('utf-8'))
            except:
                self.sendOutput((messagetypes.LAUNCHER_ERROR, 'ERR001: %s' % localizer.ERR_JSONParseError))
                print("json parse error in area 1")
                self.request('Off')

        success = data.get('success', 'false')
        self.connection.close()
        self.connection = None
        if success == 'true':
            self.cookie = data.get('cookie', 'NoCookieGiven')
            self.gameserver = data.get('gameserver', 'NoServerGiven')
            self.request('LaunchGame')
        else:
            if success == 'false':
                self.sendOutput((messagetypes.LAUNCHER_ERROR, data.get('banner', localizer.ERR_InvalidLogin)))
                self.credentials = None
                self.request('GetCredentials')
                self.sendOutput(messagetypes.LAUNCHER_CLEAR_PASSWORD)
            else:
                if success == 'partial':
                    self.authToken = data.get('responseToken', None)
                    self.authBanner = data.get('banner', '')
                    self.request('GetTFACode')
                else:
                    if success == 'delayed':
                        eta = int(data.get('eta', 5))
                        self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.GUI_Queue % eta))
                        self.queueToken = data.get('queueToken', None)
                        self.request('Delayed', eta)
        return

    def enterGetTFACode(self):
        if self.authToken is None:
            self.sendOutput((messagetypes.LAUNCHER_ERROR, 'ERR005: %s' % localizer.ERR_TFAWithoutToken))
            self.request('Off')
        self.sendOutput((messagetypes.LAUNCHER_STATUS, ''))
        self.sendOutput((messagetypes.LAUNCHER_REQUEST_TFA, self.authBanner))
        self.appToken = self.input.get(block=True, timeout=None)
        if self.appToken is None:
            self.credentials = None
            self.request('GetCredentials')
        self.request('SubmitTFACode')
        return

    def enterSubmitTFACode(self):
        self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.GUI_Authing))
        self.connection = httplib.HTTPSConnection(*settings.SSLConnection)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        params = urlencode({'appToken': self.appToken, 
           'authToken': self.authToken})
        self.connection.request('POST', settings.LoginPostLocation, params, headers)
        self.request('LoginResponse')

    def enterDelayed(self, timeDelay):
        if self.queueToken is None:
            self.sendOutput((messagetypes.LAUNCHER_ERROR, 'ERR007: %s' % localizer.ERR_DelayWithoutToken))
            self.request('Off')
        time.sleep(max(timeDelay, 1))
        self.request('CheckQueue')
        return

    def enterCheckQueue(self):
        self.connection = httplib.HTTPSConnection(*settings.SSLConnection)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        params = urlencode({'queueToken': self.queueToken})
        self.connection.request('POST', settings.LoginPostLocation, params, headers)
        self.request('LoginResponse')

    def enterPatch(self):
        from patcher import Patcher
        self.patcher = threading.Thread(target=Patcher.Patch, name='Patcher-Thread', args=(self.__updateProgress, self.__updateFile))
        self.patcher.daemon = True
        self.patcher.start()

        self.request('GetCredentials')

    def __updateProgress(self, percentage):
        if self.output.empty():
            self.sendOutput((messagetypes.LAUNCHER_PROGRESS, percentage))

    def __updateFile(self, fileCount):
        #if self.output.empty():
        self.sendOutput((messagetypes.LAUNCHER_STATUS, fileCount))

    def exitPatch(self):
        self.sendOutput((messagetypes.LAUNCHER_PROGRESS, -1))

    def enterLaunchGame(self):
        os.environ['TTR_PLAYCOOKIE'] = self.cookie
        os.environ['TTR_GAMESERVER'] = self.gameserver
        if sys.platform == 'win32':
            game = subprocess.Popen('TTREngine', creationflags=134217728)
        elif sys.platform == 'darwin':
            # open "Toontown Rewritten"
            if not DEVMODE:
                # keep track of current path to get back to
                currentPath = os.getcwd()
                # change to the app support folder
                os.chdir(MACOS_PATH)
                # on mac if we aren't in dev mode, we need to use application support folder
                modes = os.stat('Toontown Rewritten.app/Contents/MacOS/TTREngine').st_mode
                if not modes & stat.S_IXUSR:
                    os.chmod('./Toontown Rewritten.app/Contents/MacOS/TTREngine', modes | stat.S_IXUSR)
            
            
                game = subprocess.Popen(['/Toontown Rewritten.app/Contents/MacOS/TTREngine'])
            else:
                # use the current directory
                modes = os.stat('Toontown Rewritten').st_mode
                game = subprocess.Popen(['./Toontown Rewritten'])
        elif sys.platform in ['linux2', 'linux']:
            modes = os.stat('TTREngine').st_mode
            if not modes & stat.S_IXUSR:
                os.chmod('TTREngine', modes | stat.S_IXUSR)
            game = subprocess.Popen('./TTREngine')
        self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.GUI_PlayGameFarewell))
        time.sleep(1)
        self.sendOutput(messagetypes.LAUNCHER_HIDE)
        while game.poll() is None:
            time.sleep(1.5)
            # this is a hack to get the icon to show up on linux
            if sys.platform in ['linux2', 'linux']:
                os.system("/app/bin/wmclass") #Sets the WM_CLASS of Toontown Rewritten so that DE can show icon

        if game.returncode == 0:
            # return back to the original path
            os.chdir(currentPath)
            self.sendOutput(messagetypes.LAUNCHER_SHOW)
            self.sendOutput(messagetypes.LAUNCHER_ENABLE_CONTROLS)
            self.credentials = None
            self.dontClearMessage = True
            self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.GUI_PlayAgain))
            time.sleep(1.5)
            self.request('GetCredentials')
            return
        self.sendOutput(messagetypes.LAUNCHER_SHOW)
        self.sendOutput(messagetypes.LAUNCHER_PLAY_RETRY)
        if self.input.get(block=True, timeout=None):
            self.request('GetCredentials')
        else:
            self.request('Off')
        return

    def enterOff(self):
        if self.connection is not None:
            self.connection.close()
        self.sendOutput(messagetypes.LAUNCHER_EXIT)
        return
