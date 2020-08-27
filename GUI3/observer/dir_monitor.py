# -*- coding:utf-8 -*-

import re
import shutil
import queue

from observer.file_monitor import Target
from settings import *
from pathlib import Path


q = queue.Queue()   #Tread control

USERNAME='mjhnytgrf'    #Username ..settings

#regex path filter
regex = [
r'C:\\Users\\'+USERNAME+r'\\ntuser.dat.LOG1',
r'C:\\Users\\'+USERNAME+r'\\NTUSER.DAT',
r'C:\\Users\\'+USERNAME+r'\\AppData\\Local\\Temp\\wireshark_*.pcapng',
r'C:\\Program Files\\Notepad[+][+]\\*',
r'C:\\Program Files\\Wireshark\\*',
r'C:\\Program Files\\VMware\\*',
r'C:\\Users\\'+USERNAME+r'\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat.LOG1',
r'C:\\Users\\'+USERNAME+r'\\AppData\\Local\\Microsoft\\Windows\\UsrClass.dat',
r'C:\\ProgramData\\DirectoryMonitor\\*',
r'C:\\Users\\'+USERNAME+r'\\AppData\\Local\\Microsoft\\Windows\\WebCache\\*.log',
r'C:\\Users\\'+USERNAME+r'\\AppData\\Local\\Temp\\vmware-*',
r'C:\\Windows\\Prefetch\\*.pf',
r'C:\\Windows\\System32\\LogFiles\\*'
]


class CreateObserverDir(Target):

    def __init__(self, watchDir):
        super().__init__(watchDir)

    def on_created(self, event):
        try:
            fp = re.search(r"src_path='(.*)'",str(event))   # event filter
            #print('CREATE '+fp.group(1))
            new_log = str(Path(fp.group(1)))                # use Path method 
            if self.filter(new_log):                    # path fileter
                q.put('New '+ new_log)                      # Queue send
        except Exception as e:
            print(e)

            
    def on_deleted(self, event):
        try:
            fp = re.search(r"src_path='(.*)'",str(event))
            #print('DELETE '+fp.group(1))
            deleted_log = str(Path(fp.group(1)))
            if self.filter(deleted_log):
                q.put('Deleted '+ deleted_log) 
        except Exception as e:
            print(e)

            
    def on_modified(self, event):
        try:
            fp = re.search(r"src_path='(.*)'",str(event))
            #print('MODIFIED '+fp.group(1))
            modified_log = str(Path(fp.group(1)))
            if self.filter(modified_log):
                q.put('Modified '+ modified_log)
        except Exception as e:
            print(e)

            
    def on_moved(self, event):
        try:
            sp = re.search(r"src_path='(.*),",str(event))
            dp = re.search(r".*.dest_path='(.*)'",str(event))
            #print('MOVED ' + sp.group(1) + ' -> ' + dp.group(1))
            modified_sp_log = str(Path(sp.group(1)))
            modified_dp_log = str(Path(dp.group(1)))
            if self.filter(modified_sp_log) and self.filter(modified_dp_log):
                q.put('Moved ' + modified_sp_log + ' -> ' + modified_dp_log)
        except Exception as e:
            print(e) 

    def filter(self, value):
        for row in iter(regex):                     # load filter list
            result = re.match(row,value)           # use filter
            if result != None:                      # fileter matching
                print(result)
                return False                        # matched return 'False'
        return True                                 # not fileter matching


