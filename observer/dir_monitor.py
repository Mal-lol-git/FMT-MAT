# -*- coding:utf-8 -*-

import re
import os
import sys
import shutil


from observer.file_monitor import Target


#tmp = os.path.join(path)


class CreateObserverDir(Target):
    def __init__(self, watchDir):
        super().__init__(watchDir)

    def on_created(self, event):
        try:
            fp = re.search(r"src_path='(.*)'",str(event))
            print('CREATE '+fp.group(1))
            #filename = fp.group(1).split('/')[-1]
        except Exception as e:
            print(e)
    def on_deleted(self, event):
        try:
            fp = re.search(r"src_path='(.*)'",str(event))
            print('DELETE '+fp.group(1))

        except Exception as e:
            print(e)
    def on_modified(self, event):
        try:
            fp = re.search(r"src_path='(.*)'",str(event))
            print('MODIFIED '+fp.group(1))
        except Exception as e:
            print(e)
    def on_moved(self, event):
        try:
            sp = re.search(r"src_path='(.*),",str(event))
            dp = re.search(r".*.dest_path='(.*)'",str(event))
            print('MOVED ' + sp.group(1) + ' -> ' + dp.group(1))
        except Exception as e:
            print(e)            
            

