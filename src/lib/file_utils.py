'''
Created on Oct 28, 2018

@author: hpsingh
'''

#Import Python Modules
import ntpath
import os
import re
import sys
from os import walk

class File_Utils():
    """docstring for ."""

    def __init__(self):
        super().__init__()

    def find_sub_dir(self, path, regex):
        f = list()
        for entry in os.listdir(path):
            if os.path.isdir(os.path.join(path, entry)):
                if re.match(regex, entry):
                   f.append(entry)
        return f

    def getFileFromPath(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def getDirectoryFromPath(path):
        head = os.path.split(path)
        return head

    def getAppName(application):
        appArr = application.split('.')
        return appArr[0]

    def normalize_path(self, path):
        # path=re.sub(r'/|\\', re.escape(os.sep), path)
        # if re.compile('^(.*)'+re.escape(os.sep)+'$').match(path):
        #         path = re.compile('^(.*)'+re.escape(os.sep)+'$').match(path).group(1)
        # return path
        return re.sub(r'/|\\', re.escape(os.sep), path)

    def find_dir(self, path, regex, displayFullPath, recursionLevel):
        f = set()
        #print_f()
        path = self.normalize_path(path)
        count1 = len(re.findall(re.escape(os.sep),path))
        if re.compile('^(.*)'+re.escape(os.sep)+'$').match(path):
            count1 = count1 - 1

        # print('displayOnlyFiles:'+str(displayOnlyFiles))
        # print('displayFullPath:'+str(displayFullPath))
        # print('recursionLevel:'+str(recursionLevel))
        # print('path:'+ path)
        # print('count1:'+ str(count1))

        if recursionLevel is None:
            recursionLevel = sys.maxsize
        for (dirpath, dirnames, filenames) in walk(path):
            count2 = len(re.findall(re.escape(os.sep),dirpath))
            #count2 = dirpath.count(re.escape(os.sep))
            if re.compile('^(.*)'+re.escape(os.sep)+'$').match(dirpath):
                count2 = count2 - 1
            level = count2 - count1
            if ( level <= recursionLevel):
                for dirname in dirnames:
                    if re.search(regex, dirname):
                            if (displayFullPath):
                                f.add(os.path.join(dirpath,dirname))
                                # print('count2:' + str(count2))
                                # print('level:' + str(level))
                                # print('dirpath:' + dirpath)
                            else:
                                f.add(dirname)
        return f
