# -*- coding:utf-8 -*-

import os 
import getpass
import re

#===========================USER NAME===========================

USERNAME = getpass.getuser()

#===========================USER NAME===========================

NOW_PATH = os.path.dirname(os.path.abspath(__file__))
BACKUP_PATH = os.path.join(NOW_PATH, 'backup')

