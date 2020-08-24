import sys

from observer.dir_monitor import CreateObserverDir


arg = sys.argv[1]

ob = CreateObserverDir(arg)
ob.run()
