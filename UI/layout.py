import sys 
import os
import time
import shutil
import threading

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from concurrent.futures import ThreadPoolExecutor
from observer.dir_monitor import CreateObserverDir
from observer.dir_monitor import *

#========================================================================================

worker_list = []


class CLineEditWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.UI()
		self.monitor = ''
	

	def UI(self):
		
		self.setWindowTitle("File Monitoring Tool")
		self.setGeometry(100,100,500,500)
		self.setWindowIcon(QIcon('D:\\pool\\FMT-MAT\\GUI3\\UI\\test.ico'))	# 아이콘
		#self.setStyleSheet('border: 1px solid black; background-color: #2f3640')	# 색상
        
		textLabel = QLabel("Status : ")
		textLabel.setMaximumWidth(150)
		textLabel.setMaximumHeight(20)

		self.checkbox = QCheckBox("CreateFile Backup")
		#self.checkbox.setMaximumWidth(20)
		#self.checkbox.setMaximumHeight(30)
		self.checkbox.stateChanged.connect(self.filebackup)

		textLabel2 = QLabel("Path : ")
		textLabel2.setMaximumWidth(50)
		textLabel2.setMaximumHeight(30)
	
		self.label = QLabel("")
		self.label.setMaximumWidth(150)
		self.label.setMaximumHeight(20)

		btnStart = QPushButton("Start")
		btnStart.setMaximumWidth(50)
		btnStart.setMaximumHeight(30)
		btnStart.clicked.connect(self.btnStart_clicked)

		btnStop = QPushButton("Stop")
		btnStop.setMaximumWidth(50)
		btnStop.setMaximumHeight(30)
		btnStop.clicked.connect(self.btnStop_clicked)

		btnOpendir = QPushButton("...")
		btnOpendir.setMaximumWidth(30)
		btnOpendir.setMaximumHeight(20)
		btnOpendir.clicked.connect(self.btnOpendir_clicked)

		self.textedit = QListWidget()
		self.textedit.setFont(QFont("나눔고딕", 8, QFont.Bold))

		self.textedit2 = QListWidget()
		self.textedit2.setMaximumWidth(290)
		self.textedit2.setMaximumHeight(20)
		self.textedit2.setFont(QFont("나눔고딕", 8, QFont.Bold))
		
		layout = QGridLayout()

		layout.setSpacing(5)
				
		layout.addWidget(textLabel, 1, 0)
		layout.addWidget(self.checkbox, 0, 4, 1, 2)
		layout.addWidget(textLabel2, 1, 3)
		layout.addWidget(self.label, 1, 1, 1, 2)
		layout.addWidget(btnStart, 0, 0)
		layout.addWidget(btnStop, 0, 1, 1, 2)
		layout.addWidget(self.textedit, 2, 0, 1, 6)
		layout.addWidget(self.textedit2, 1, 4)
		layout.addWidget(btnOpendir, 1, 5)
		
		self.setLayout(layout)
		
		self.textedit.setContextMenuPolicy(Qt.ActionsContextMenu)

		clear_action = QAction('Clear_all_log',self)
		self.textedit.addAction(clear_action)
		clear_action.triggered.connect(self.textedit.clear)

		self.textedit.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)

		self.textedit.itemDoubleClicked.connect(self.showItem)


	def filebackup(self, data):		
		if self.checkbox.isChecked():
			if not os.path.exists(BACKUP_PATH):
				os.makedirs(BACKUP_PATH)
			if str == type(data): 
				result = re.search('^(New|Deleted|Modified|Moved) (.*)',data)
				orgin_path = result.group(2)
				if os.path.isfile(orgin_path):
					shutil.copy2(orgin_path, BACKUP_PATH)


	def showItem(self, item):
		#print(self.textedit.currentItem().text())
		result = re.search('^(New|Deleted|Modified|Moved) (.*)',self.textedit.currentItem().text())
		click_path = result.group(2)

		if not os.path.isdir(click_path):
			click_path = os.path.dirname(click_path)

		if os.path.isdir(click_path):
			os.startfile(click_path)

	def btnOpendir_clicked(self):
		directory = str(QFileDialog.getExistingDirectory())
		if bool(directory) and '실행 중' != self.label.text():
			self.textedit2.clear()
			self.textedit2.addItem('{}'.format(directory))
			self.monitor = CreateObserverDir(directory)
		
	def btnStart_clicked(self):
		if '중지' == self.label.text() or (''== self.label.text() and self.textedit2.item(0) is not None):
			worker = threading.Thread(target=self.monitor.run, name='logger', daemon=True)
			worker_list.append(worker)
			worker.start()

			worker2 = threading.Thread(target=self.print, name='logg2', daemon=True)
			worker_list.append(worker2)
			worker2.start()

			time.sleep(0.5)
			self.status()
		else:
			pass

	def btnStop_clicked(self):
		if '실행 중' == self.label.text(): 
			self.monitor.stop()
			q.put(' ')

			worker = worker_list[0]
			worker2 = worker_list[1]

			del worker_list[:]

			worker.join()
			worker2.join()

			self.status()
		else:
			pass

	def print(self):
		while(True):                   
			event_data = q.get()
			if event_data == ' ':
		   		break

			event = event_data.split(' ')[0]
			#b = re.search(' (.*)',event_data)
			self.col(event, event_data)
			time.sleep(0.05)

	def col(self, event, event_data):
		#item = QListWidgetItem(event)
		data_item = QListWidgetItem(event_data)
		
		if event == 'New':
			data_item.setForeground(QColor('#60C13C'))
		if event == 'Modified':
			data_item.setForeground(QColor('#30BBF6'))
			self.filebackup(event_data)
		if event == 'Deleted':
			data_item.setForeground(QColor('#FE9A2E'))
		if event == 'Moved':
			data_item.setForeground(QColor('#C385E5'))
		
		self.textedit.addItem(data_item)

	def status(self):
		if not self.monitor.status():
			self.label.setText("중지")
		if self.monitor.status():	
			self.label.setText("실행 중")

if __name__ == "__main__":

	app = QApplication(sys.argv)

	window = CLineEditWindow()
	window.show()

	app.exec_()
