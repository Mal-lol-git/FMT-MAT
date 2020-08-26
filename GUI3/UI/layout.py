import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import threading
import time
from concurrent.futures import ThreadPoolExecutor

from observer.dir_monitor import CreateObserverDir
from observer.dir_monitor import *

asd = []
path = r'C:\\'
col = ''

item = ''
item2 = ''

t = CreateObserverDir(path)
class CLineEditWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.UI()
	

	def UI(self):
		#self.setWindowFlags(Qt.FramelessWindowHint) 
		#self.setWindowFlags(Qt.X11BypassWindowManagerHint)

		self.setWindowTitle("File Monitoring Tool")
		self.setGeometry(100,100,500,500)
		self.setWindowIcon(QIcon('D:\\pool\\FMT-MAT\\GUI3\\UI\\test.ico'))	# 아이콘
		#self.setStyleSheet('border: 1px solid black; background-color: #E1BEE7')	# 색상 


		textLabel = QLabel("Status : ", self)
		textLabel.move(20,55)
		textLabel.resize(150,20)

		self.label = QLabel("", self)
		self.label.move(55,55)
		self.label.resize(150,20)

		btnStart = QPushButton("Start", self)
		btnStart.move(20,20)
		btnStart.resize(50,30)
		btnStart.clicked.connect(self.btnStart_clicked)

		btnStop = QPushButton("Stop", self)
		btnStop.move(80,20)
		btnStop.resize(50,30)
		btnStop.clicked.connect(self.btnStop_clicked)

		self.textedit = QListWidget(self)
		self.textedit.move(20,80)
		self.textedit.resize(450,400)
		self.textedit.setFont(QFont("나눔고딕", 8, QFont.Bold))
		#self.textedit.move(20,80)
		#self.textedit.resize(90,400)
		self.textedit.setStyleSheet("background: white")

		#self.textedit.moveCursor(QTextCursor.End)


		#self.setCentralWidget(scroll)

		#self.textedit2 = QListWidget(self)
		#self.textedit2.move(90,80)
		#self.textedit2.resize(390,400)
		#self.textedit2.setStyleSheet("border: 0.1px solid black;")

		




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
		time.sleep(0.5)
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
		time.sleep(0.3)
		worker2.join()

	def print(self):
		while(True):                   
			a = q.get()

			c = a.split(' ')[0]
			b = re.search(' (.*)',a)
			self.col(c, a)
			#self.textedit.addItem(item)
			#self.textedit.setStyleSheet("Color : black")

			#if b != None:
		   	#	self.textedit.addItem(b.group(1))

			if a == '3':
		   		break	

	def col(self, c, b):
		item = QListWidgetItem(c)
		item2 = QListWidgetItem(b)

		if c == 'New':
			item2.setForeground(QColor('#60C13C'))
		if c == 'Modified':
			item2.setForeground(QColor('#30BBF6'))
		if c == 'Deleted':
			item2.setForeground(QColor('#FE9A2E'))
		if c == 'Moved':
			item2.setForeground(QColor('#C385E5'))
		item2.setSelected(True)
		self.textedit.addItem(item2)
		print(self.textedit.row(item2))
		q = self.textedit.item(self.textedit.row(item2))
		self.textedit.scrollToItem(q, QAbstractItemView.PositionAtTop)
		#self.textedit.scrollToItem(item2, QAbstractItemView.PositionAtBottom)
		


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
