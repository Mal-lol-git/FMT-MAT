# -*- coding:utf-8 -*-

import re
import queue

from observer.file_monitor import Target
from filter.log_filter import regex
from pathlib import Path
from settings import *

#========================================================================================

q = queue.Queue()                                                   #Tread control


class CreateObserverDir(Target):

    def __init__(self, watchDir):
        super().__init__(watchDir)

    #created event 
    def on_created(self, event):
        try:
            #print(bool(event)) --
            fp = re.search(r"src_path='(.*)'",str(event))           # created event regex filter
            #print('CREATE '+fp.group(1))
            new_log = str(Path(fp.group(1)))                        # use Path method 
            if self.filter(new_log, regex):                         # apply regex filter list <- log_filter.py
                q.put('New '+ new_log)                              # send new_log to Queue
        except Exception as e:
            print(e)

    #deleted event
    def on_deleted(self, event):                                 
        try:
            fp = re.search(r"src_path='(.*)'",str(event))           # deleted event regex filter
            #print('DELETE '+fp.group(1))
            deleted_log = str(Path(fp.group(1)))                    # use Path method
            if self.filter(deleted_log, regex):                     # apply regex filter list <- log_filter.py
                q.put('Deleted '+ deleted_log)                      # send deleted_log to Queue
        except Exception as e:
            print(e)

    #modified event
    def on_modified(self, event):
        try:
            fp = re.search(r"src_path='(.*)'",str(event))           # modified event regex filter
            #print('MODIFIED '+fp.group(1))
            modified_log = str(Path(fp.group(1)))                   # use Path method
            if self.filter(modified_log, regex):                    # apply regex filter list <- log_filter.py
                q.put('Modified '+ modified_log)                    # send modified_log to Queue
        except Exception as e:
            print(e)

    #moved event        
    def on_moved(self, event):
        try:
            sp = re.search(r"src_path='(.*),",str(event))                                               # moved(src) event regex filter 
            dp = re.search(r".*.dest_path='(.*)'",str(event))                                           # moved(dest) event regex filter
            #print('MOVED ' + sp.group(1) + ' -> ' + dp.group(1))
            modified_sp_log = str(Path(sp.group(1)))                                                    # use Path method
            modified_dp_log = str(Path(dp.group(1)))                                                    # use Path method
            if self.filter(modified_sp_log, regex) and self.filter(modified_dp_log, regex):             # apply regex filter list <- log_filter.py 
                q.put('Moved ' + modified_dp_log)                            # send moved(sp,dp)_log to Queue
                #q.put('Moved ' + modified_sp_log + ' -> ' + modified_dp_log)                            # send moved(sp,dp)_log to Queue
        except Exception as e:
            print(e) 

    #event filter
    def filter(self, Event, filter_list):
        event = Event.split(os.sep)                                 # event split and delete '\' to path

        for row in iter(filter_list):                               # filter_list value -> row
            fv = row.split(os.sep)                                  # row split and delete '\' to path
            
            if event == fv or event[:-1] == fv:                     # compare event and filter_list 
                return False                                        # detect filter -> return False

            if '*' == fv[-1]:
                if fv[:-1] == event or fv[:-1] == event[:-1]:
                    return False
        
            if '*.' == fv[-1][:2]:
                if event[:-1] == fv[:-1]:
                    f1 = os.path.splitext(row)[-1]
                    e1 = os.path.splitext(Event)[-1]
                    if f1 == e1:
                        return False
                        
        if '*' != fv[-1]:
            if '*.' != fv[-1][:2]:
                a = re.search(fv[-1], event[-1])
                if a != None:
                    return False             

        return True


