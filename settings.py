# -*- coding:utf-8 -*-

import os, sys
import getpass
import re
import tempfile 

#===========================USER NAME===========================

USERNAME = getpass.getuser()

#===========================BAKUP_PATH===========================

EXE_PATH  = os.path.dirname(sys.executable)
BACKUP_PATH = os.path.join(EXE_PATH, 'backup')



