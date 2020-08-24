# -*- coding:utf-8 -*-

import re

from observer.file_monitor import Target


log_path = r'D:\pool\FMT-MAT\WEB\log.txt'


class CreateObserverDir(Target):
    def __init__(self, watchDir):
        super().__init__(watchDir)

    def on_created(self, event):
        try:
            with open(log_path, 'a', -1, 'utf-8') as f:
                fp = re.search(r"src_path='(.*)'",str(event))
                f.write('NEW '+fp.group(1)+'\n')

        except Exception as e:
            print(e)

            
    def on_deleted(self, event):
        try:
            with open(log_path, 'a', -1, 'utf-8') as f:
                fp = re.search(r"src_path='(.*)'",str(event))
                f.write('DELETE '+fp.group(1)+'\n')
                
        except Exception as e:
            print(e)

            
    def on_modified(self, event):
        try:
            with open(log_path, 'a', -1, 'utf-8') as f:
                fp = re.search(r"src_path='(.*)'",str(event))
                f.write('MODIFIED '+fp.group(1)+'\n')
                
        except Exception as e:
            print(e)

            
    def on_moved(self, event):
        try:
            with open(log_path, 'a', -1, 'utf-8') as f:
                sp = re.search(r"src_path='(.*),",str(event))
                dp = re.search(r".*.dest_path='(.*)'",str(event))
                f.write('MOVED ' + sp.group(1) + ' -> ' + dp.group(1)+'\n')
                
        except Exception as e:
            print(e)            
            

