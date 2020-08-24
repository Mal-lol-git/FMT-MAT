import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import threading
import time
from concurrent.futures import ThreadPoolExecutor

from observer.dir_monitor import CreateObserverDir
from observer.dir_monitor import *

asd = []
path = r'C:\\'

t = CreateObserverDir(path)
class CLineEditWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.UI()
	

	def UI(self):
		self.setWindowTitle("a")
		self.setGeometry(100,100,500,500)


		textLabel = QLabel("상태 : ", self)
		textLabel.move(20,55)
		textLabel.resize(150,20)

		self.label = QLabel("", self)
		self.label.move(55,55)
		self.label.resize(150,20)

		btnStart = QPushButton("시작", self)
		btnStart.move(20,20)
		btnStart.resize(50,30)
		btnStart.clicked.connect(self.btnStart_clicked)

		btnStop = QPushButton("정지", self)
		btnStop.move(80,20)
		btnStop.resize(50,30)
		btnStop.clicked.connect(self.btnStop_clicked)

		self.textedit = QListWidget(self)
		self.textedit.move(20,80)
		self.textedit.resize(450,400)

		


	def btnStart_clicked(self):
		
		#pass
		#with ThreadPoolExecutor(1) as executor:
		#	results = executor.submit(self.target, (lambda : path, ))

		#	a = results.done()
		#	b = results.running()
		#	print(b)
		#print(results)

		worker = threading.Thread(target=t.run, name='logger', daemon=True)
		#print(worker.is_alive())
		#print(worker.daemon)
		asd.append(worker)
		worker.start()

		#t.run()
		worker2 = threading.Thread(target=self.print, name='logg2', daemon=True)
		asd.append(worker2)
		worker2.start()
		time.sleep(0.5)
		self.status()
		#print(worker.is_alive())
		#print(worker.daemon)
		print('worker : '+ str(worker.isAlive()))

	def btnStop_clicked(self):
		t.stop()
		q.put('3')
		time.sleep(0.7)
		self.status()
		worker = asd[0]
		worker2 = asd[1]
		

		#worker.stop = True
		del asd[:]
		#worker.daemon = False

		print('worker : '+ str(worker.isAlive()))
		print('worker daemon : '+ str(worker.daemon))
		print('worker2 : '+ str(worker2.is_alive()))
		print('worker daemon2 : '+ str(worker2.daemon))

		worker.join()
		time.sleep(1)
		worker2.join()

	def print(self):
		while(True):                   
		    a = q.get()
		    self.textedit.addItem(a)
		    print('2')
		    if a == '3':
		    	break		
                

	def status(self):
		if not t.status():
			self.label.setText("중지")
		if t.status():	
			self.label.setText("실행 중")

if __name__ == "__main__":

	app = QApplication(sys.argv)

	window = CLineEditWindow()
	window.show()

	app.exec_()
